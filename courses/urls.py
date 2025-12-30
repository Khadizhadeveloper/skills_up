from django.contrib.auth.views import LoginView
from django.urls import path, include
from .views import (RegisterView, UserProfileView, CourseListView, CourseDetailView,
                    CourseFreeLessonView, CourseProgressView, ModuleDetailView, ModuleListView,
                    LessonDetailView, LessonUpdateProgressView, MyCoursesView, MyCertificatesView, MyReviewsView,
                    PurchaseListView, PurchaseCreateView, ReviewListView, ReviewCreateView, GenerateCertificateView,
                    SupportMessageListView, SupportMessageDetailView, SupportMessageCreateView, FAQListView,
                    TestimonialListView, SiteSettingsView, SpeakerListView, SpeakerDetailView)

app_name = "courses"

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<slug:slug>/free/', CourseFreeLessonView.as_view(), name='course-free-lesson'),
    path('courses/<slug:course_slug>/modules/', ModuleListView.as_view(), name='module-list'),
    path('modules/<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/progress/', LessonUpdateProgressView.as_view(), name='lesson-progress'),
    path('my-courses/', MyCoursesView.as_view(), name='my-courses'),
    path('my-courses<int:course_id>/progress/', CourseProgressView.as_view(), name='my-courses-progress' ),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('purchases/create/', PurchaseCreateView.as_view(), name='purchase-create'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('my-reviews/', MyReviewsView.as_view(), name='my-reviews'),
    path('certificates/', MyCertificatesView.as_view(), name='my-certificates'),
    path('certificates/generate/<int:course_id>/', GenerateCertificateView.as_view(), name='generate-certificate'),
    path('support/', SupportMessageListView.as_view(), name='support-list'),
    path('support/create/', SupportMessageCreateView.as_view(), name='support-create'),
    path('support/<int:pk>/', SupportMessageDetailView.as_view(), name='support-detail'),
    path('faq/', FAQListView.as_view(), name='faq-list'),
    path('testimonial/', TestimonialListView.as_view(), name='testimonial-list'),
    path('settings/', SiteSettingsView.as_view(), name='site-settings'),
    path('speakers/', SpeakerListView.as_view(), name='speaker-list'),
    path('speakers/<int:pk>/', SpeakerDetailView.as_view(), name='speaker-detail'),



]