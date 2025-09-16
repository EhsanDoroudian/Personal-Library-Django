from django.core.management.base import BaseCommand
from books.models import Category


categories_for_migration = [
    {"title": "ادبیات"},
    {"title": "شعر"},
    {"title": "رمان"},
    {"title": "داستان کوتاه"},
    {"title": "تاریخ"},
    {"title": "فلسفه"},
    {"title": "ورزشی"},
    {"title": "علوم اجتماعی"},
    {"title": "روانشناسی"},
    {"title": "هنر"},
    {"title": "سینما"},
    {"title": "موسیقی"},
    {"title": "کودک و نوجوان"},
    {"title": "علوم پزشکی"},
    {"title": "فنی و مهندسی"},
    {"title": "کتاب‌های دانشگاهی"},
    {"title": "مذهبی"},
    {"title": "سفرنامه"},
    {"title": "بیوگرافی"},
    {"title": "علمی تخیلی"}
]

class Command(BaseCommand):
    help = 'Populate categories'

    def handle(self, *args, **options):
        for category_data in categories_for_migration:
            Category.objects.get_or_create(**category_data)
        self.stdout.write(self.style.SUCCESS('Successfully populated categories'))
