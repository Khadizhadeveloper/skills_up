# courses/management/commands/test_data.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import (
    Speaker, Course, Module, Lesson,
    FAQ, Testimonial, SiteSettings
)
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт тестовые данные для платформы онлайн-курсов'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Начинаем создание тестовых данных...'))

        # Очистить старые данные (опционально)
        self.stdout.write('Очистка старых данных...')
        Speaker.objects.all().delete()
        Course.objects.all().delete()
        FAQ.objects.all().delete()
        Testimonial.objects.all().delete()
        SiteSettings.objects.all().delete()

        # 1. Создать пользователей
        self.stdout.write('Создание пользователей...')

        # Суперпользователь (если нет)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Админ',
                last_name='Админов'
            )

        # Тестовые студенты
        student1, _ = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@example.com',
                'first_name': 'Айгуль',
                'last_name': 'Токтомова',
                'phone': '+996700123456'
            }
        )
        student1.set_password('student123')
        student1.save()

        student2, _ = User.objects.get_or_create(
            username='student2',
            defaults={
                'email': 'student2@example.com',
                'first_name': 'Бекзат',
                'last_name': 'Алимов',
                'phone': '+996700987654'
            }
        )
        student2.set_password('student123')
        student2.save()

        self.stdout.write(self.style.SUCCESS('✓ Пользователи созданы'))

        # 2. Создать спикеров
        self.stdout.write('Создание спикеров...')

        speaker1 = Speaker.objects.create(
            name='Алия Асанова',
            bio='Эксперт по таргетированной рекламе с 5-летним опытом. Запустила более 200 успешных рекламных кампаний.',
            phone='+996555111222',
            photo='',
            video_intro='',
            telegram='@aliya_ads',
            instagram='aliya.targeting',
            youtube='AliyaTargeting'
        )

        speaker2 = Speaker.objects.create(
            name='Эмиль Садыков',
            bio='SMM-специалист и контент-маркетолог. Помог вырастить аудиторию более 50 брендов.',
            phone='+996555333444',
            photo='',
            telegram='@emil_smm',
            instagram='emil.smm',
            youtube='EmilSMM'
        )

        speaker3 = Speaker.objects.create(
            name='Нургуль Бакирова',
            bio='Профессиональный фотограф и эксперт по мобильной фотографии. Преподаватель с 3-летним стажем.',
            phone='+996555555666',
            telegram='@nurgul_photo',
            instagram='nurgul.mobilephoto'
        )

        self.stdout.write(self.style.SUCCESS('✓ Спикеры созданы'))

        # 3. Создать курсы с модулями и уроками
        self.stdout.write('Создание курсов...')

        # Курс 1: Таргетированная реклама
        course1 = Course.objects.create(
            title='Таргетированная реклама для начинающих',
            slug='targetirovannaya-reklama',
            short_description='Научитесь запускать эффективную рекламу в социальных сетях и привлекать целевых клиентов.',
            full_description='На этом курсе вы освоите все основы таргетированной рекламы: от настройки аудиторий до анализа результатов. Вы научитесь создавать рекламные кампании в Facebook, Instagram и TikTok, которые будут приносить реальные продажи.',
            price=Decimal('4999.00'),
            preview_video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            target_audience='Предприниматели, маркетологи, фрилансеры, владельцы малого бизнеса',
            what_included='24 видеоурока, практические задания, шаблоны объявлений, сертификат, доступ навсегда, поддержка в чате',
            speaker=speaker1,
            is_published=True,
            order=1
        )

        # Модули курса 1
        module1_1 = Module.objects.create(
            course=course1,
            title='Введение в таргетированную рекламу',
            description='Основы таргетинга и подготовка к запуску первой кампании',
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module1_1,
            title='Что такое таргетированная реклама',
            description='Узнаете основные понятия и преимущества таргетинга',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=15,
            order=1,
            is_free=True  # Бесплатный урок
        )

        Lesson.objects.create(
            module=module1_1,
            title='Настройка рекламного кабинета',
            description='Пошаговая настройка Facebook Business Manager',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=20,
            order=2,
            is_free=False
        )

        Lesson.objects.create(
            module=module1_1,
            title='Выбор целевой аудитории',
            description='Как правильно определить свою ЦА',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=25,
            order=3,
            is_free=False
        )

        module1_2 = Module.objects.create(
            course=course1,
            title='Создание эффективных объявлений',
            description='Учимся создавать креативы, которые продают',
            order=2,
            is_published=True
        )

        Lesson.objects.create(
            module=module1_2,
            title='Виды рекламных форматов',
            description='Обзор всех доступных форматов рекламы',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=18,
            order=1,
            is_free=False
        )

        Lesson.objects.create(
            module=module1_2,
            title='Написание продающих текстов',
            description='Формулы и примеры эффективных текстов',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=22,
            order=2,
            is_free=False
        )

        # Курс 2: SMM
        course2 = Course.objects.create(
            title='SMM-специалист с нуля до PRO',
            slug='smm-specialist',
            short_description='Полный курс по продвижению в социальных сетях. Освойте профессию SMM-менеджера.',
            full_description='Комплексный курс по SMM, который научит вас создавать контент-стратегию, вести аккаунты брендов, запускать рекламу и анализировать результаты. После курса вы сможете работать SMM-специалистом или продвигать свой бизнес.',
            price=Decimal('7999.00'),
            preview_video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            target_audience='Начинающие маркетологи, предприниматели, студенты, фрилансеры',
            what_included='36 видеоуроков, практические задания, чек-листы, шаблоны постов, сертификат',
            speaker=speaker2,
            is_published=True,
            order=2
        )

        module2_1 = Module.objects.create(
            course=course2,
            title='Основы SMM',
            description='Что такое SMM и как начать работать',
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module2_1,
            title='Введение в SMM',
            description='Обзор профессии и основных задач',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=12,
            order=1,
            is_free=True  # Бесплатный урок
        )

        Lesson.objects.create(
            module=module2_1,
            title='Выбор платформ для продвижения',
            description='Instagram, Facebook, TikTok, YouTube - где продвигаться',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=17,
            order=2,
            is_free=False
        )

        # Курс 3: Мобилография
        course3 = Course.objects.create(
            title='Мобильная фотография: от любителя до профи',
            slug='mobilnaya-fotografiya',
            short_description='Научитесь делать профессиональные фото на смартфон и зарабатывать на этом.',
            full_description='Вы узнаете все секреты мобильной фотографии: композиция, свет, обработка. Научитесь снимать предметы, людей, еду и пейзажи. Получите навыки, которые помогут вам создавать контент для соцсетей или работать фотографом.',
            price=Decimal('3999.00'),
            preview_video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            target_audience='Блогеры, предприниматели, фотолюбители, начинающие фотографы',
            what_included='20 видеоуроков, практические задания, пресеты для обработки, сертификат',
            speaker=speaker3,
            is_published=True,
            order=3
        )

        module3_1 = Module.objects.create(
            course=course3,
            title='Основы мобильной фотографии',
            description='Начинаем снимать правильно',
            order=1,
            is_published=True
        )

        Lesson.objects.create(
            module=module3_1,
            title='Настройки камеры смартфона',
            description='Как использовать камеру на максимум',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=14,
            order=1,
            is_free=True  # Бесплатный урок
        )

        Lesson.objects.create(
            module=module3_1,
            title='Композиция в фотографии',
            description='Правило третей, ракурсы, перспектива',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            duration=19,
            order=2,
            is_free=False
        )

        self.stdout.write(self.style.SUCCESS('✓ Курсы созданы'))

        # 4. Создать FAQ
        self.stdout.write('Создание FAQ...')

        FAQ.objects.create(
            question='Как проходит обучение?',
            answer='Обучение проходит в формате видеоуроков, которые доступны 24/7. Вы можете учиться в удобное время и в своём темпе.',
            order=1,
            is_published=True
        )

        FAQ.objects.create(
            question='Сколько длится курс?',
            answer='Длительность зависит от курса. В среднем 3-6 недель при занятиях по 1-2 часа в день. Доступ к материалам остаётся навсегда.',
            order=2,
            is_published=True
        )

        FAQ.objects.create(
            question='Нужен ли опыт для прохождения курсов?',
            answer='Нет, большинство наших курсов рассчитаны на новичков. Мы объясняем всё с нуля.',
            order=3,
            is_published=True
        )

        FAQ.objects.create(
            question='Выдаётся ли сертификат?',
            answer='Да, после успешного завершения курса вы получаете сертификат о прохождении обучения.',
            order=4,
            is_published=True
        )

        FAQ.objects.create(
            question='Какие способы оплаты доступны?',
            answer='Мы принимаем банковские карты, Элсом, Balance, MBank Pay и другие популярные платёжные системы Кыргызстана.',
            order=5,
            is_published=True
        )

        self.stdout.write(self.style.SUCCESS('✓ FAQ созданы'))

        # 5. Создать отзывы для главной
        self.stdout.write('Создание отзывов...')

        Testimonial.objects.create(
            author_name='Айгуль Токтомова',
            text='Прошла курс по таргетированной рекламе. Всё очень понятно объяснено! Уже через неделю запустила свою первую рекламную кампанию и получила заказы. Спасибо!',
            rating=5,
            is_featured=True,
            order=1
        )

        Testimonial.objects.create(
            author_name='Бекзат Алимов',
            text='Курс по SMM превзошёл все ожидания. Много практики, реальные кейсы. Теперь работаю SMM-менеджером в крупной компании.',
            rating=5,
            is_featured=True,
            order=2
        )

        Testimonial.objects.create(
            author_name='Мээрим Исакова',
            text='Мобильная фотография - это находка! Научилась делать красивые фото для своего магазина. Продажи выросли в 2 раза!',
            rating=5,
            is_featured=True,
            order=3
        )

        self.stdout.write(self.style.SUCCESS('✓ Отзывы созданы'))

        # 6. Создать настройки сайта
        self.stdout.write('Создание настроек сайта...')

        SiteSettings.objects.create(
            phone='+996 700 123 456',
            email='info@onlineschool.kg',
            whatsapp='+996700123456',
            telegram='@online_school_kg',
            instagram='https://instagram.com/online_school_kg',
            youtube='https://youtube.com/@onlineschool',
            facebook='https://facebook.com/onlineschoolkg',
            about_text='Мы — онлайн-школа современных цифровых профессий. Наша миссия — сделать качественное образование доступным для каждого. Учитесь у лучших практиков, получайте реальные навыки и начинайте зарабатывать уже в процессе обучения.'
        )

        self.stdout.write(self.style.SUCCESS('✓ Настройки сайта созданы'))

        # Итоговая статистика
        self.stdout.write(self.style.SUCCESS('\n=== ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО СОЗДАНЫ ==='))
        self.stdout.write(f'Пользователей: {User.objects.count()}')
        self.stdout.write(f'Спикеров: {Speaker.objects.count()}')
        self.stdout.write(f'Курсов: {Course.objects.count()}')
        self.stdout.write(f'Модулей: {Module.objects.count()}')
        self.stdout.write(f'Уроков: {Lesson.objects.count()}')
        self.stdout.write(f'FAQ: {FAQ.objects.count()}')
        self.stdout.write(f'Отзывов: {Testimonial.objects.count()}')
        self.stdout.write('\nДанные для входа:')
        self.stdout.write('Админ: username=admin, password=admin123')
        self.stdout.write('Студент 1: username=student1, password=student123')
        self.stdout.write('Студент 2: username=student2, password=student123')