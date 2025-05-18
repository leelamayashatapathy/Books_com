import json
from django.core.management.base import BaseCommand
from books.models import Book, Category
from vendors.models import Vendor
from django.contrib.auth import get_user_model
from taggit.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Load demo books data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r') as file:
            data = json.load(file)

        created, skipped = 0, 0

        for item in data:
            try:
                vendor_user = User.objects.get(email=item['vendor_email'])
                vendor = Vendor.objects.get(user=vendor_user)

                category, _ = Category.objects.get_or_create(
                    slug=item['category_slug'],
                    defaults={'name': item['category_slug'].replace('-', ' ').title()}
                )

                book, created_book = Book.objects.get_or_create(
                    title=item['title'],
                    defaults={
                        'author': item['author'],
                        'description': item['description'],
                        'isbn': item['isbn'],
                        'price': item['price'],
                        'stock': item['stock'],
                        'category': category,
                        'vendor': vendor
                    }
                )

                if created_book:
                    book.tags.set(item.get('tags', []))
                    book.save()
                    created += 1
                else:
                    skipped += 1

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Books created: {created}"))
        self.stdout.write(self.style.WARNING(f"Books skipped (already exist): {skipped}"))
