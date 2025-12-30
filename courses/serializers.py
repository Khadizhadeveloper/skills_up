from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from courses.models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password', 'password2', 'first_name', 'last_name')


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user=User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'first_name', 'last_name', 'created_at')
        read_only_fields = ('id','created_at',)


class UserProfileSerializer(serializers.ModelSerializer):
    total_courses = serializers.SerializerMethodField()
    completed_courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'first_name', 'last_name',
                  'created_at', 'total_courses', 'completed_courses')
        read_only_fields = ('id','created_at',)

    def get_total_courses(self, obj):
        return Purchase.objects.filter(user=obj, status='completed').count()

    def get_completed_courses(self, obj):
        purchases = Purchase.objects.filter(user=obj, status='completed')
        completed=0
        for purchase in purchases:
            total_lessons=Lesson.objects.filter(module__course=purchase.course).count()
            completed_lessons=UserProgress.objects.filter(
                user=obj,
                lesson__module__course=purchase.course,
                is_completed=True).count()
            if total_lessons>0 and total_lessons==completed_lessons:
                completed += 1
        return completed


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields='__all__'


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields=('id', 'title', 'duration', 'order', 'is_free')


class LessonDetailSerializer(serializers.ModelSerializer):
    user_progress=serializers.SerializerMethodField()
    class Meta:
        model = Lesson
        fields=('id', 'title', 'description', 'video_url', 'duration',
                'order', 'is_free', 'user_progress', 'materials')


    def get_user_progress(self, obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress=UserProgress.objects.get(user=request.user, lesson=obj)
                return {
                    'is_completed': progress.is_completed,
                    'last_watched_position': progress.last_watched_position,
                }
            except UserProgress.DoesNotExist:
                return None
        return None


class ModuleListSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)
    lessons_count=serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields=('id', 'title', 'description', 'order', 'lessons','lessons_count')

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class ModuleDetailSerializer(serializers.ModelSerializer):
    lessons = LessonDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields=('id', 'title', 'description', 'order', 'is_published', 'lessons')

class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    course_id=serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Review
        fields=('id', 'user', 'course', 'course_id', 'rating', 'text',
                'video_url', 'is_approved', 'created_at')

        read_only_fields = ('id','user', 'created_at','is_approved')

    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        return super().create(validated_data)

class CourseListSerializer(serializers.ModelSerializer):
    speaker=SpeakerSerializer(read_only=True)
    modules_count=serializers.SerializerMethodField()
    lessons_count=serializers.SerializerMethodField()
    students_count=serializers.SerializerMethodField()
    average_rating=serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields=('id', 'title', 'slug', 'short_description', 'price',
                'banner_image', 'speaker', 'students_count','modules_count',
                'lessons_count', 'average_rating', 'order')

    def get_modules_count(self, obj):
        return obj.modules.filter(is_published=True).count()

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(module__course=obj, module__is_published=True).count()

    def get_students_count(self, obj):
        return Purchase.objects.filter(course=obj, status='completed').count()

    def get_average_rating(self, obj):
        reviews=Review.objects.filter(course=obj, is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0


class CourseDetailSerializer(serializers.ModelSerializer):
    speaker=SpeakerSerializer(read_only=True)
    modules=ModuleListSerializer(many=True, read_only=True)
    reviews=serializers.SerializerMethodField()
    is_purchased=serializers.SerializerMethodField()
    free_lesson=serializers.SerializerMethodField()
    students_count=serializers.SerializerMethodField()
    average_rating=serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'short_description', 'full_description',
                  'price', 'preview_video_url', 'banner_image', 'target_audience',
                  'what_included', 'speaker', 'modules', 'reviews', 'is_purchased',
                  'free_lesson', 'students_count', 'average_rating')


    def get_reviews(self, obj):
        reviews=Review.objects.filter(course=obj, is_approved=True)[:5]
        return ReviewSerializer(reviews, many=True).data

    def get_is_purchased(self, obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            return Purchase.objects.filter(
                user=request.user,
                course=obj,
                status='completed',

            ).exists()
        return False

    def get_free_lesson(self, obj):
        free_lesson=Lesson.objects.filter(
            module__course=obj,
            is_free=True,

        ).order_by('module__order', 'order').first()

        if free_lesson:
            return LessonDetailSerializer(free_lesson).data
        return None

    def get_students_count(self, obj):
        return Purchase.objects.filter(course=obj, status='completed').count()


    def get_average_rating(self, obj):
        reviews=Review.objects.filter(course=obj, is_approved=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0


class PurchaseSerializer(serializers.ModelSerializer):
    course=CourseDetailSerializer(read_only=True)
    course_id=serializers.IntegerField(write_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'course', 'course_id', 'amount_paid', 'payment_method',
                  'transaction_id', 'status', 'purchased_at')
        read_only_fields = ('id', 'status', 'purchased_at', 'transaction_id')

    def create(self, validated_data):
        user=self.context['request'].user
        course_id=validated_data['course_id']

        if Purchase.objects.filter(user=user, course_id=course_id, status='completed').exists():
            raise serializers.ValidationError('Вы уже купили этот курс')

        validated_data['user']=user
        return super().create(validated_data)


class UserProgressSerializer(serializers.ModelSerializer):
    lesson=LessonListSerializer(read_only=True)
    lesson_id=serializers.IntegerField(write_only=True)

    class Meta:
        model = UserProgress
        fields = ('id', 'lesson', 'lesson_id', 'is_completed', 'completed_at',
                  'last_watched_position')
        read_only_fields = ('id', 'completed_at')


class CourseProgressSerializer(serializers.Serializer):
    course=CourseDetailSerializer(read_only=True)
    total_lessons=serializers.IntegerField()
    completed_lessons=serializers.IntegerField()
    progress_percent=serializers.FloatField()
    last_watched_lesson=LessonListSerializer(read_only=True)


class CertificateSerializer(serializers.ModelSerializer):
    course=CourseDetailSerializer(read_only=True)

    class Meta:
        model = Certificate
        fields = ('id', 'course', 'certificate_number', 'issued_at', 'certificate_file')
        read_only_fields = ('id', 'certificate_number', 'issued_at')


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'order')


class SupportSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)

    class Meta:
        model=SupportMessage
        fields = ('id', 'user', 'message', 'reply', 'status', 'created_at', 'replied_at')
        read_only_fields = ('id', 'user', 'reply', 'status', 'created_at', 'replied_at')

    def create(self, validated_data):
        validated_data['user']=self.context['request'].user
        return super().create(validated_data)


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ('id', 'author_name', 'author_photo', 'text', 'video_url', 'rating', 'created_at')


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields='__all__'





















