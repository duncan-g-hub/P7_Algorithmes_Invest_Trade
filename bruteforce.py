import csv
from pathlib import Path


CUR_DIR = Path(__file__).resolve().parent
DATA_DIR = CUR_DIR / 'data'


# Extraire les données du csv : cout et bénéfice
def get_data_from_csv(csv_file):
    with open(DATA_DIR / csv_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return list(reader)


#Nettoyer la liste des actions
def clean_data(actions):
    cleaned_actions = []
    for action in actions:
        cleaned_action = {
            "name": action["Actions #"],
            "cost": int(action["Coût par action (en euros)"]),
            "profit_percent" : float(action["Bénéfice (après 2 ans)"].replace("%",""))/100
        }
        cleaned_actions.append(cleaned_action)
    return cleaned_actions
