from exrex import getone

def regex2text(regex):
    return getone(regex)

regex = "\w{2}[*]\d{2}"
print(regex2text(regex))