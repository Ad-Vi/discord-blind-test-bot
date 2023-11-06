from unidecode import unidecode
import textdistance
def compare(answers,song):
    return textdistance.sorensen(unidecode(answers).lower(), unidecode(song).lower()) >= 0.9