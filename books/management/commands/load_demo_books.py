import os
import json
from django.core.management.base import BaseCommand
from books.models import Book, Category
from vendors.models import Vendor
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Command(BaseCommand):
    help = 'Load demo books data from dummy_books.json'

    def handle(self, *args, **kwargs):
        # Auto-locate dummy_books.json relative to this script file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, 'dummy_books.json')

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"JSON file not found at {file_path}"))
            return

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                self.stderr.write(self.style.ERROR(f"JSON decoding error: {e}"))
                return

        created, skipped = 0, 0

        for item in data:
            try:
                vendor = Vendor.objects.get(id=item['vendor'])
                category = Category.objects.get(id=item['category'])

                book, created_book = Book.objects.get_or_create(
                    isbn=item['isbn'],  # Unique constraint
                    defaults={
                        'title': item['title'],
                        'slug': slugify(item['title']),
                        'author': item['author'],
                        'description': item['description'],
                        'price': item['price'],
                        'stock': item['stock'],
                        'vendor': vendor,
                        'category': category,
                        'published_date': item.get('published_date', None),
                    }
                )

                if created_book:
                    book.tags.set(item.get('tags', []))
                    book.save()
                    created += 1
                else:
                    skipped += 1

            except Vendor.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Vendor ID {item['vendor']} not found"))
            except Category.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Category ID {item['category']} not found"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Books created: {created}"))
        self.stdout.write(self.style.WARNING(f"⚠️ Books skipped (already exist): {skipped}"))
