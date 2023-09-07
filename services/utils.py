from unidecode import unidecode

def normalize (text):
    return unidecode(text).replace(' ', '-').lower()

def checkIdPost (header):
    if header.find('?p=') != -1:
        return header.split('?p=')[1].split('&')[0].split('>')[0]
    else:
        return False

def porcentage (current, total):
    calcule = (current / total) * 100
    print(f'{calcule}%')