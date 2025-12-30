from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):

    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Speaker(models.Model):

    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(verbose_name='Биография спикера', null=True, blank=True)
    photo = models.ImageField(upload_to='speakers/', verbose_name='Фото спикера', null=True, blank=True)


class Course(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    speaker=models.ForeignKey(Speaker, on_delete=models.CASCADE, verbose_name='Спикер', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    preview_video_url = models.URLField(blank=True, verbose_name='Превью видео')
    banner_image = models.ImageField(upload_to='courses/banners/', blank=True, verbose_name='Баннер')
    target_audience = models.TextField(verbose_name='Кому подходит')
    what_included = models.TextField(verbose_name='Что входит')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title





class Module(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name='Курс')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name='Модуль')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    video_url = models.URLField(verbose_name='URL видео')
    duration = models.IntegerField(help_text='Длительность в минутах', verbose_name='Длительность')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_free = models.BooleanField(default=False, verbose_name='Бесплатный урок')
    materials = models.FileField(upload_to='lessons/materials/', blank=True, verbose_name='Материалы')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Purchase(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('completed', 'Завершена'),
        ('failed', 'Отклонена'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Банковская карта'),
        ('elsom', 'Элсом'),
        ('balance', 'Balance'),
        ('mbank', 'MBank'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='purchases', verbose_name='Курс')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')
    transaction_id = models.CharField(max_length=255, unique=True, verbose_name='ID транзакции')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class UserProgress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress', verbose_name='Пользователь')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='user_progress', verbose_name='Урок')
    is_completed = models.BooleanField(default=False, verbose_name='Завершен')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения')
    last_watched_position = models.IntegerField(default=0, help_text='Позиция в секундах',
                                                verbose_name='Последняя позиция')

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс пользователей'
        unique_together = ['user', 'lesson']

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class Review(models.Model):#отзыв к определенному курсу

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews', verbose_name='Курс')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Рейтинг'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    video_url = models.URLField(blank=True, verbose_name='URL видео-отзыва')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.rating}★)"


class Testimonial(models.Model):#отзыв на главной странице

    author_name = models.CharField(max_length=255)
    author_photo = models.ImageField(upload_to='testimonials/', blank=True)
    text = models.TextField()
    video_url = models.URLField(blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class FAQ(models.Model):

    question = models.CharField(max_length=500, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order']

    def __str__(self):
        return self.question


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates', verbose_name='Курс')
    certificate_number = models.CharField(max_length=50, unique=True, verbose_name='Номер сертификата')  # ← Добавить
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата выдачи')
    certificate_file = models.FileField(upload_to='certificates/', blank=True, verbose_name='Файл сертификата')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        unique_together = ['user', 'course']

    def save(self, *args, **kwargs):
        if not self.certificate_number:
            # Генерация номера: CERT-2025-ABC123
            import uuid
            self.certificate_number = f"CERT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class SupportMessage(models.Model):

    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('closed', 'Закрыто'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_messages',
                             verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    reply = models.TextField(blank=True, verbose_name='Ответ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата ответа')

    class Meta:
        verbose_name = 'Сообщение в поддержку'
        verbose_name_plural = 'Сообщения в поддержку'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%d.%m.%Y')}"


class SiteSettings(models.Model):

    site_name = models.CharField(max_length=255, default='Название школы')
    about_text = models.TextField(help_text='Блок О компании на главной')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'