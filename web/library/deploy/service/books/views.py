import os

from rest_framework import permissions, mixins, serializers
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from books.permissions import IsOwner
from books.serializers import BookSerializer, BookCreateSerializer
from books.utils import CreateDiffrentMixin
from service.book_config import BOOK_STORE, MAX_BOOKS_SIZE

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)

class IsAdminUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.username == 'admin'

class BookViewSet(CreateDiffrentMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
#    permission_classes = [permissions.IsAuthenticated ]
    permission_classes = [IsAdminUserOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    create_output_serializer = BookSerializer

    def perform_create(self, serializer):
        if self.request.user.username != 'admin':
            raise serializers.ValidationError("Только администратор может добавлять книги.")
        book_text = serializer.validated_data.pop('text')
        if book_text.size > MAX_BOOKS_SIZE:
            raise serializers.ValidationError("Book is too big")
        if book_text.content_type != 'text/plain':
            raise serializers.ValidationError("File is not a text")
        instance = serializer.save(owner=self.request.user)
        logger.info(f"Book created with UID: {instance.uid}")
        description_filename = os.path.join(BOOK_STORE, f"{instance.uid}.txt")

        with open(description_filename, 'wb+') as f:
            for chunk in book_text.chunks():
                f.write(chunk)


    def get_queryset(self):
        return Book.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer

        return BookSerializer

