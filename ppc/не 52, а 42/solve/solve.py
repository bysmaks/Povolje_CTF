import os
import pyminizip

def encode():
    for i in range(1, 2345 + 1):
        zip_file_name = f'task{2345 + 1 - i}.zip'
        # Распаковка архива
        pyminizip.uncompress(zip_file_name, None, None, 0)

        if i < 2345:
            # Удаление архива после распаковки
            os.remove(zip_file_name)

if __name__ == '__main__':
    encode()
