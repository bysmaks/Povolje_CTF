import os
import pyminizip


def encrypted_zip(zip_path, password, extract_path=None):
    pyminizip.uncompress(zip_path, password, extract_path, 0)


def main():
    for i in range(1,
                   2345+1
                   ):

        with open(f'pass{2345+1 - i}.txt', mode='r') as pws:
            passwd = pws.readline()

        encrypted_zip(f'task{2345+1 - i}.zip', passwd)

        # if i < 4:
        os.remove(f'task{2345+1 - i}.zip')
        os.remove(f'pass{2345+1 - i}.txt')


if __name__ == '__main__':
    main()
