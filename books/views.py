# books/views.py
from django.shortcuts import render
from django.http import JsonResponse
from . import models

def start_page(request):
    data = models.Book.objects.all()
    return render(request, 'index.html', context={'data': data})

def get_reviews(request, book_id):
    try:
        book = models.Book.objects.get(id=book_id)
        reviews = book.reviews.all()  # ← теперь работает!
        data = []
        for review in reviews:
            data.append({
                'id': review.id,
                'rating': review.rating,
                'published_date': review.published_date.isoformat(),
                'review': review.review
            })
        return JsonResponse(data, safe=False)
    except models.Book.DoesNotExist:
        return JsonResponse({'error': 'Книга не найдена'}, status=404)