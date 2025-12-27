from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from .models import (User, Course, Module, Lesson, Purchase,
                     UserProgress, Review, Certificate, FAQ,
                     SupportMessage, Testimonial, SiteSettings, Speaker, )

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email','phone', 'is_staff','created_at' )
    list_filter=('is_staff', 'is_active', 'created_at')
    search_fields=('username', 'email', 'phone')
    ordering = ('-created_at',)

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio', 'phone')
    search_fields = ('name',)

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ('title', 'order', 'is_published')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'price', 'is_published', 'order', 'created_at')
    search_fields=('title', 'short_description', 'speaker')
    list_filter=('is_published', 'created_at', 'speaker')
    prepopulated_fields={'slug':('title',)}
    list_editable=['is_published', 'price', 'order',]
    ordering = ['-created_at',]
    inlines=[ModuleInline]

    fieldsets = (
        ('Основная информация: ', {
            'fields': ('title', 'slug', 'speaker', 'price', 'is_published', 'order',),
        }),
        ('Описание: ', {
            'fields': ('short_description', 'full_description',  'target_audience', 'what_included', ),
        }),
        ('Медиа: ', {
            'fields': ('preview_video_url', 'banner_image'),
        })

    )

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'duration', 'order', 'is_free')


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title','course', 'order', 'is_published')
    search_fields=('title','course__title')
    list_filter=('course', 'is_published')
    list_editable=('is_published', 'order',)
    inlines=[LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'duration','order', 'is_free')
    list_filter=('module__course', 'is_free')
    search_fields=('title', 'module__title')
    list_editable=('is_free', 'order',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount_paid','payment_method', 'status', 'purchased_at' )
    list_filter=('status', 'payment_method', 'purchased_at')
    search_fields=('user__username', 'user__email', 'course__title', 'transaction_id')
    readonly_fields=( 'transaction_id', 'purchased_at')
    list_editable=('status',)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status=='completed':
            return False
        return super().has_delete_permission(request, obj)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'is_completed', 'completed_at', 'last_watched_position')
    list_filter=('is_completed', 'lesson__module__course')
    search_fields=('user__username',  'lesson__title')
    readonly_fields=('completed_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'is_approved', 'created_at')
    list_filter=('rating', 'is_approved', 'created_at', 'course')
    search_fields=('user__username', 'course__title', 'text')
    list_editable=('is_approved',)
    readonly_fields = ('created_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'rating', 'created_at')
    search_fields = ('author_name', 'text')
    list_editable = ('is_featured', 'order')
    readonly_fields = ('created_at',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display=('user', 'course', 'certificate_number', 'issued_at')
    list_filter=('issued_at', 'course')
    search_fields=('user__username', 'course__title', 'certificate_number')
    readonly_fields=('issued_at', 'certificate_number')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display=('question', 'order', 'is_published')
    list_filter=('is_published',)
    search_fields=('question','answer',)
    list_editable=('is_published', 'order',)


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display=('user', 'status', 'created_at', 'replied_at')
    list_filter=('status', 'created_at')
    search_fields=('user__username', 'message', 'reply')
    readonly_fields=('created_at',)

    fieldsets=(
        ('Информация: ', {
            'fields': ('user', 'status', 'created_at'),
        }),
        ('Сообщение: ', {
            'fields': ('message',),
        }),
        ('Ответ: ', {
            'fields': ('reply', 'replied_at',),
        }),
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


    fieldsets=(
        ('Контакты: ', {
            'fields': ('phone', 'email', 'whatsapp', 'telegram'),
        }),
        ('Социальная сеть: ', {
            'fields': ('instagram', 'youtube', 'facebook'),
        }),
        ('О компании: ', {
            'fields': ('about_text',),
        })
    )





