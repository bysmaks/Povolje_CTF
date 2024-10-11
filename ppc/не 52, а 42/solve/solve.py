import os
import zipfile


def encode():
    for i in range(1, 2345+1):
        zip_file_name = f'task{2345+1 - i}.zip'
        with zipfile.ZipFile(zip_file_name) as zip:
            zip.extractall()

        if i < 2345:
            os.remove(zip_file_name)


if __name__ == '__main__':
    encode()
