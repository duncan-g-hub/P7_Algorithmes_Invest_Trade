import csv
from pathlib import Path


CUR_DIR = Path(__file__).resolve().parent
DATA_DIR = CUR_DIR / 'data'


# Extraire les données du csv : cout et bénéfice
def get_data_from_csv(csv_file):
    with open(DATA_DIR / csv_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return list(reader)