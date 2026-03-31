# books/management/commands/query.py
from django.core.management.base import BaseCommand
from books.models import Book, Publisher, Store, Review
from datetime import date
from django.db.models import Avg, Count

class Command(BaseCommand):
    help = 'Выполняет сложные запросы к базе данных'

    def handle(self, *args, **options):
        self.stdout.write("="*60)
        self.stdout.write("📊 СЛОЖНЫЕ ЗАПРОСЫ В DJANGO")
        self.stdout.write("="*60)

        # 1. Книги издательств из Новосибирска
        books_from_nsk = Book.objects.filter(publisher__location='Новосибирск')
        self.stdout.write("📚 Книги издательств из Новосибирска:")
        for book in books_from_nsk:
            self.stdout.write(f"  • {book.title} ({book.publisher.name})")

        self.stdout.write("\n1️⃣ Книги издательств из Новосибирска (оптимизированный):")
        books_nsk = Book.objects.select_related('publisher').filter(publisher__location='Новосибирск')
        for b in books_nsk:
            self.stdout.write(f"   📖 {b.title} — {b.publisher.name}")

        # 2. Книги в магазинах Москвы
        books_in_moscow = Book.objects.filter(stores__city='Москва').distinct()
        self.stdout.write("📚 Книги, продающиеся в магазинах Москвы:")
        for book in books_in_moscow:
            stores_list = ', '.join([store.name for store in book.stores.filter(city='Москва')])
            self.stdout.write(f"  • {book.title} - продаётся в: {stores_list}")

        self.stdout.write("\n2️⃣ Книги в магазинах Москвы (оптимизирован для многие ко многим):")
        books_msk = Book.objects.filter(stores__city='Москва').distinct().prefetch_related('stores')
        for b in books_msk:
            stores = ', '.join([s.name for s in b.stores.all()])
            self.stdout.write(f"   📖 {b.title} — {stores}")

        # 3. Книги с рейтингом > 7.5
        self.stdout.write("\n3️⃣ Книги со средним рейтингом > 7.5:")
        high_rated = Book.objects.annotate(avg=Avg('reviews__rating')).filter(avg__gt=7.5)
        for b in high_rated:
            self.stdout.write(f"   ⭐ {b.title} — {b.avg:.1f}★")

        # 4. Количество книг в магазинах
        self.stdout.write("\n4️⃣ Количество книг в магазинах:")
        stores_cnt = Store.objects.annotate(cnt=Count('books')).order_by('-cnt')
        for s in stores_cnt:
            self.stdout.write(f"   🏪 {s.name} ({s.city}) — {s.cnt} книг")

        # 5. Магазины с книгами после 1920 года
        self.stdout.write("\n5️⃣ Магазины с книгами после 1920 года (сортировка по убыванию количества):")
        stores_1920 = Store.objects.filter(
            books__published_date__gt=date(1920, 1, 1)
        ).annotate(cnt=Count('books')).distinct().order_by('-cnt') # -cnt убывание
        for s in stores_1920:
            self.stdout.write(f"   🏪 {s.name} — {s.cnt} книг")

        self.stdout.write("\n" + "="*60)