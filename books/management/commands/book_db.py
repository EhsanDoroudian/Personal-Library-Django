import random
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Book, Category


class Command(BaseCommand):
    help = "Import books from an ODS file with random categories"

    def add_arguments(self, parser):
        parser.add_argument("ods_file", type=str, help="Path to the ODS file")
        parser.add_argument("--user-id", type=int, required=True, help="User ID to assign books to")

    def handle(self, *args, **options):
        ods_file = options["ods_file"]
        user_id = options["user_id"]

        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"User with ID {user_id} does not exist"))
            return

        # Load ODS file
        df = pd.read_excel(ods_file, engine="odf")

        # Get all categories
        categories = list(Category.objects.all())
        if not categories:
            self.stderr.write(self.style.ERROR("No categories found in database. Please add categories first."))
            return

        for _, row in df.iterrows():
            random_category = random.choice(categories)

            book, created = Book.objects.get_or_create(
                title=row["title"].strip(),
                author=row["author"].strip(),
                user=user,
                defaults={
                    "description": row.get("description", ""),
                    "translator": row.get("translator", ""),
                    "publisher": row.get("publisher", ""),
                    "price": row.get("price"),
                    "year": row.get("year"),
                    "shabak_number": str(row.get("shabak_number", "")).strip(),
                    "page_number": row.get("page_number"),
                    "category": random_category,
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added book: {book.title} → {random_category.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Book already exists: {book.title}"))
