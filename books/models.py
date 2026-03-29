from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField()

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField()
    description = models.TextField()
    in_stock = models.PositiveIntegerField(default=7)
    #
    genres = models.ManyToManyField(Genre, related_name='books')
    stores = models.ManyToManyField(Store, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='books'
    )

    @property
    def reviews_count(self):
        return self.reviews.count()

    def __str__(self):
        return self.title

class Review(models.Model):
    rating = models.PositiveIntegerField(default=7)
    published_date = models.DateField()
    review = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews'
    )

    def __str__(self):
        return self.review
