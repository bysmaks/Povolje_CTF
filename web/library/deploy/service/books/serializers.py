from rest_framework import serializers

from books.models import Book
from service.book_config import MAX_BOOKS_SIZE


class BookSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)  # Получаем email через отношение owner
    class Meta:
        model = Book
        fields = ('uid','title', 'text','owner_email')


class BookCreateSerializer(serializers.ModelSerializer):
    text = serializers.FileField()
    class Meta:
        model = Book
        fields = ('title','text')
