import sys


if 2 >= len(sys.argv):
    print("1º argument:\tCSV file https://www.dwds.de/d/api#wb-list-goethe ")
    print(
        "2º argument:\tLanguage destination https://developers.deepl.com/docs/resources/supported-languages#target-languages ")
    print("Example:\t\tpython3 1000Worts-deutsch.py A1.csv ES")
    exit(2)

ZIELSPRACHE = sys.argv[2]
ROOT_FOLDER = "000Wortlisten"
VORHERIG_AUSSPRACHE = "audio"
AUSSPRACHE_FORMAT = ".mp3"
ENDE_DIV = "</div>"
