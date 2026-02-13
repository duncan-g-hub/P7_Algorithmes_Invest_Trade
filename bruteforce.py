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


# Calculer le gain en euro de chaque action (gain% * prix action)
def calculate_profit(actions):
    for action in actions:
        action["profit_euro"] = round(action["cost"] * action["profit_percent"],2)
    return actions


# trier les actions par pourcentage de profit croissant (meilleurs bénéfices)
def sort_actions_by_profit(actions):
    return sorted(actions, key=lambda action: action["profit_percent"])


# récupérer la meilleure combinaison d'action sans dépasser 500€ de budget
def get_best_actions(actions):
    best_actions = []
    total_cost = 0
    i = 1
    while i <= len(actions) :
        if total_cost + actions[-i]["cost"] <= 500:
            best_actions.append(actions[-i])
            total_cost += actions[-i]["cost"]
        i += 1
    return best_actions



def main():
    raw_actions = get_data_from_csv("data_actions.csv")
    cleaned_actions = clean_data(raw_actions)
    actions_with_profits = calculate_profit(cleaned_actions)
    actions_sorted = sort_actions_by_profit(actions_with_profits)
    best_actions = get_best_actions(actions_sorted)

    print(actions_sorted)
    print(best_actions)

    total_cost = 0
    for action in best_actions:
        total_cost += action["cost"]
    print(total_cost)

    total_profit = 0
    for action in best_actions:
        total_profit += action["profit_euro"]
    print(total_profit)


main()