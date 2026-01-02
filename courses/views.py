from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
import uuid
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes
from .models import (
    User, Speaker, Course, Module, Lesson,
    Purchase, UserProgress, Review, Certificate,
    FAQ, SupportMessage, Testimonial, SiteSettings
)
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileSerializer,
    SpeakerSerializer, CourseListSerializer, CourseDetailSerializer,
    ModuleListSerializer, ModuleDetailSerializer,
    LessonListSerializer, LessonDetailSerializer,
    PurchaseSerializer, UserProgressSerializer,
    ReviewSerializer, CertificateSerializer,
    FAQSerializer, SupportSerializer, TestimonialSerializer, SiteSettingsSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])

def login_view(request):
    print("LOGIN VIEW CALLED")
    identifier=request.data.get('login')
    password=request.data.get('password')

    if not identifier or not password:
        return Response(
            {'error': 'Укажите логин и пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user=None

    try:
        user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        pass

    if not user:
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            pass

    if not user:
        try:
            user=User.objects.get(phone=identifier)
        except User.DoesNotExist:
            pass

    if not user:
        return Response(
            {'error': 'Пользователь не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    if not user.check_password(password):
        return Response(
            {'error': 'Неверный пароль'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'Аккаунт деактивирован'},
            status=status.HTTP_403_FORBIDDEN
        )

    login(request, user)
    return Response(
        {
            'message': 'Успешный вход',
            'user': UserSerializer(user).data,
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])

def logout_view(request):
    logout(request)
    return Response(
        {'message': 'Вы вышли из системы'},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def check_auth_view(request):
    return Response({
        'authenticated':True,
        'user': UserSerializer(request.user).data,
    })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {'error': 'Укажите старый и новый пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {'error': 'Неверный текущий пароль'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password, user)
        except DjangoValidationError as e:
            return Response(
                {'error': list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {'message': 'Пароль успешно изменен'}
        )





class CourseListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('speaker').order_by('order')


class CourseDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('speaker').prefetch_related('modules')


class CourseFreeLessonView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_published=True)

        free_lesson = Lesson.objects.filter(
            module__course=course,
            is_free=True
        ).order_by('module__order', 'order').first()

        if not free_lesson:
            return Response(
                {'detail': 'Бесплатный урок не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LessonDetailSerializer(free_lesson, context={'request': request})
        return Response(serializer.data)


class ModuleListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ModuleListSerializer

    def get_queryset(self):
        course_slug = self.kwargs.get('course_slug')
        return Module.objects.filter(
            course__slug=course_slug,
            is_published=True
        ).prefetch_related('lessons').order_by('order')


class ModuleDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ModuleDetailSerializer

    def get_queryset(self):
        return Module.objects.filter(is_published=True).prefetch_related('lessons')


class LessonDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonDetailSerializer

    def get_queryset(self):
        user = self.request.user
        purchased_courses = Purchase.objects.filter(
            user=user,
            status='completed'
        ).values_list('course_id', flat=True)

        return Lesson.objects.filter(
            Q(is_free=True) | Q(module__course_id__in=purchased_courses)
        ).select_related('module__course')

    def retrieve(self, request, *args, **kwargs):
        lesson = self.get_object()


        if not lesson.is_free:
            has_access = Purchase.objects.filter(
                user=request.user,
                course=lesson.module.course,
                status='completed'
            ).exists()

            if not has_access:
                return Response(
                    {'detail': 'У вас нет доступа к этому уроку. Купите курс.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(lesson)
        return Response(serializer.data)


class LessonUpdateProgressView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        user = request.user

        if not lesson.is_free:
            has_access = Purchase.objects.filter(
                user=user,
                course=lesson.module.course,
                status='completed'
            ).exists()

            if not has_access:
                return Response(
                    {'detail': 'У вас нет доступа к этому уроку'},
                    status=status.HTTP_403_FORBIDDEN
                )

        progress, created = UserProgress.objects.get_or_create(
            user=user,
            lesson=lesson
        )

        progress.last_watched_position = request.data.get('last_watched_position', progress.last_watched_position)

        if request.data.get('is_completed'):
            progress.is_completed = True
            progress.completed_at = timezone.now()

        progress.save()

        serializer = UserProgressSerializer(progress)
        return Response(serializer.data)


class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        purchases = Purchase.objects.filter(
            user=request.user,
            status='completed'
        ).select_related('course')

        courses_data = []
        for purchase in purchases:
            course = purchase.course

            total_lessons = Lesson.objects.filter(module__course=course).count()
            completed_lessons = UserProgress.objects.filter(
                user=request.user,
                lesson__module__course=course,
                is_completed=True
            ).count()

            progress_percent = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

            last_progress = UserProgress.objects.filter(
                user=request.user,
                lesson__module__course=course
            ).order_by('-completed_at', '-id').first()

            courses_data.append({
                'id': course.id,
                'title': course.title,
                'slug': course.slug,
                'banner_image': course.banner_image.url if course.banner_image else None,
                'progress_percent': round(progress_percent, 1),
                'total_lessons': total_lessons,
                'completed_lessons': completed_lessons,
                'purchased_at': purchase.purchased_at,
                'last_watched_lesson': LessonListSerializer(last_progress.lesson).data if last_progress else None
            })

        return Response({'courses': courses_data})


class CourseProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)

        if not Purchase.objects.filter(user=request.user, course=course, status='completed').exists():
            return Response(
                {'detail': 'У вас нет доступа к этому курсу'},
                status=status.HTTP_403_FORBIDDEN
            )

        lessons = Lesson.objects.filter(module__course=course).select_related('module')
        user_progress = UserProgress.objects.filter(
            user=request.user,
            lesson__module__course=course
        ).select_related('lesson')

        modules_data = []
        for module in course.modules.filter(is_published=True).order_by('order'):
            module_lessons = lessons.filter(module=module)

            lessons_data = []
            for lesson in module_lessons:
                progress = user_progress.filter(lesson=lesson).first()
                lessons_data.append({
                    'id': lesson.id,
                    'title': lesson.title,
                    'duration': lesson.duration,
                    'order': lesson.order,
                    'is_completed': progress.is_completed if progress else False,
                    'last_watched_position': progress.last_watched_position if progress else 0
                })

            modules_data.append({
                'id': module.id,
                'title': module.title,
                'order': module.order,
                'lessons': lessons_data
            })

        total_lessons = lessons.count()
        completed_lessons = user_progress.filter(is_completed=True).count()
        progress_percent = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

        return Response({
            'course': CourseListSerializer(course).data,
            'modules': modules_data,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': round(progress_percent, 1)
        })


class PurchaseCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        purchase = serializer.save()

        purchase.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        purchase.save()

        return Response({
            'purchase_id': purchase.id,
            'transaction_id': purchase.transaction_id,
            'amount': purchase.amount_paid,
            'payment_url': f'/payment/{purchase.transaction_id}/',
            'message': 'Покупка создана. Перейдите к оплате.'
        }, status=status.HTTP_201_CREATED)


class PurchaseListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user).select_related('course').order_by('-purchased_at')


class ReviewListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        queryset = Review.objects.filter(is_approved=True).select_related('user', 'course')

        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset.order_by('-created_at')


class ReviewCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        course_id = self.request.data.get('course_id')
        if not Purchase.objects.filter(
                user=self.request.user,
                course_id=course_id,
                status='completed'
        ).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Вы можете оставить отзыв только на купленные курсы')

        serializer.save()


class MyReviewsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('course').order_by('-created_at')


class MyCertificatesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user).select_related('course')


class GenerateCertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user


        if not Purchase.objects.filter(user=user, course=course, status='completed').exists():
            return Response(
                {'detail': 'Вы не купили этот курс'},
                status=status.HTTP_403_FORBIDDEN
            )


        total_lessons = Lesson.objects.filter(module__course=course).count()
        completed_lessons = UserProgress.objects.filter(
            user=user,
            lesson__module__course=course,
            is_completed=True
        ).count()

        if completed_lessons < total_lessons:
            return Response(
                {'detail': f'Завершите все уроки. Прогресс: {completed_lessons}/{total_lessons}'},
                status=status.HTTP_400_BAD_REQUEST
            )


        certificate, created = Certificate.objects.get_or_create(
            user=user,
            course=course
        )

        serializer = CertificateSerializer(certificate)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class SupportMessageListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = SupportSerializer

    def get_queryset(self):
        return SupportMessage.objects.filter(user=self.request.user).order_by('-created_at')


class SupportMessageCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = SupportSerializer


class SupportMessageDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = SupportSerializer

    def get_queryset(self):
        return SupportMessage.objects.filter(user=self.request.user)


class FAQListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = FAQSerializer
    queryset = FAQ.objects.filter(is_published=True).order_by('order')


class TestimonialListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.filter(is_featured=True).order_by('order')


class SiteSettingsView(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        settings = SiteSettings.get_settings()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)


class SpeakerListView(generics.ListAPIView):

    permission_classes = [AllowAny]
    serializer_class = SpeakerSerializer
    queryset = Speaker.objects.all()


class SpeakerDetailView(generics.RetrieveAPIView):

    permission_classes = [AllowAny]
    serializer_class = SpeakerSerializer
    queryset = Speaker.objects.all()