from books.models import Book, Author, Publisher, Store, Review
from datetime import date
from django.db.models import Avg, Count, Q

# Создадим издательства в разных городах
publisher_moscow = Publisher.objects.create(name='Московский Дом Книги', location='Москва')
publisher_spb = Publisher.objects.create(name='Питерское Издательство', location='Санкт-Петербург')
publisher_nsk = Publisher.objects.create(name='Сибирский Печатник', location='Новосибирск')

# Создадим магазины в разных городах
store_moscow = Store.objects.create(name='Дом Книги на Арбате', city='Москва')
store_spb = Store.objects.create(name='Дом Книги на Невском', city='Санкт-Петербург')
store_nsk = Store.objects.create(name='Сибирский Книжный', city='Новосибирск')

# Создадим книги и свяжем с издательствами
book1 = Book.objects.create(
    title='Война и мир',
    author=Author.objects.get(name='Лев Толстой'),
    published_date=date(1869, 1, 1),
    description='Роман-эпопея',
    publisher=publisher_moscow
)

book2 = Book.objects.create(
    title='1984',
    author=Author.objects.get(name='Джордж Оруэлл'),
    published_date=date(1949, 6, 8),
    description='Роман-антиутопия',
    publisher=publisher_moscow
)

book3 = Book.objects.create(
    title='Улисс',
    author=Author.objects.get(name='Джеймс Джойс'),
    published_date=date(1922, 2, 2),
    description='Модернистский роман',
    publisher=publisher_nsk
)

# Связываем книги с магазинами
book1.stores.add(store_moscow, store_nsk)
book2.stores.add(store_moscow, store_spb)
book3.stores.add(store_nsk, store_spb)

# Добавляем отзывы с оценками
Review.objects.create(
    rating='8',
    published_date=date(2025, 1, 1),
    review='Великая книга!',
    book=book1
)
Review.objects.create(
    rating='9',
    published_date=date(2025, 1, 2),
    review='Шедевр',
    book=book1
)
Review.objects.create(
    rating='10',
    published_date=date(2025, 1, 3),
    review='Лучшая антиутопия',
    book=book2
)
Review.objects.create(
    rating='7',
    published_date=date(2025, 1, 4),
    review='Сложно читать',
    book=book3
)