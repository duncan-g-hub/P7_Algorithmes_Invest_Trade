import csv
from pathlib import Path
import time

CUR_DIR = Path(__file__).resolve().parent
DATA_DIR = CUR_DIR / 'data'


# Extraire les données du csv : cout et bénéfice
def get_data_from_csv(csv_file):
    with open(DATA_DIR / csv_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return list(reader)


# Formater la liste des actions
def format_data(actions):
    formated_actions = []
    for action in actions:
        # formated_action = {
        #     "name": action["Actions #"],
        #     "cost": int(action["Coût par action (en euros)"]),
        #     "profit_percent" : float(action["Bénéfice (après 2 ans)"].replace("%",""))/100
        # }

        # Nettoyage pour la section 3
        if action['price'] == "0.0" or "-" in action['price'] or action['profit'] == "0.0":
            continue
        formated_action = {
            "name": action["name"],
            "cost": float(action["price"]),
            "profit_percent": float(action["profit"]) / 100  # / float(action["price"])
        }

        formated_actions.append(formated_action)
    return formated_actions


# Calculer le bénéfice en euro de chaque action (bénéfice% * prix action)
def calculate_profit(actions):
    for action in actions:
        action["profit_euro"] = float(action["cost"] * action["profit_percent"])
    return actions


# trier les actions par pourcentage de bénéf croissant
def sort_actions_by_profit_percent(actions):
    return sorted(actions, key=lambda action: action["profit_percent"])


# obtenir la meilleure combinaison d'action selon l'algorithme glouton
def get_best_actions(actions, max_budget=500):
    budget = 0
    best_actions = []
    for action in reversed(actions):
        if budget + action["cost"] <= max_budget:
            budget += action["cost"]
            best_actions.append(action)
    return best_actions


# Afficher la liste des meilleures actions, avec le cout total et le bénéfice total aprés 2 ans.
def display_best_actions(actions):
    total_cost = 0
    total_profit = 0
    print("Liste de la combinaison d'actions apportant le meilleur bénéfice avec un budget de 500€ :")
    print()
    for action in actions:
        print(f"{action['name']}  ->  Coût : {action['cost']}€ - Bénéfice : {round(action['profit_euro'],3)}€")
        total_cost += action["cost"]
        total_profit += action["profit_euro"]
    print()
    print(f"Coût total : {total_cost}€ - Bénéfice total : {round(total_profit, 2)}€ sur {len(actions)} actions.")


def main():
    raw_actions = get_data_from_csv("dataset1.csv")
    formated_actions = format_data(raw_actions)
    actions_with_profits = calculate_profit(formated_actions)

    sorted_actions = sort_actions_by_profit_percent(formated_actions)

    best_actions = get_best_actions(sorted_actions, max_budget=500)

    display_best_actions(best_actions)


if __name__ == "__main__":
    start_time = time.time()
    main()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Temps écoulé : {elapsed_time} secondes")
