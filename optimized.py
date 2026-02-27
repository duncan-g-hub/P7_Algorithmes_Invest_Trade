import csv
from pathlib import Path
# from pprint import pprint
import time

from data_exploration import get_actions_informations

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
            "cost": int(float(action["price"]) * 100),  # *100 pour avoir en centime
            "profit_percent": float(action["profit"]) / 100  # / float(action["price"])
        }
        formated_actions.append(formated_action)
    return formated_actions


# Calculer le bénéfice en euro de chaque action (bénéfice% * prix action)
def calculate_profit(actions):
    for action in actions:
        action["profit_euro"] = action["cost"] * action["profit_percent"]
    return actions


# obtenir la meilleure combinaison d'action selon l'algorithme knapsack dynamique
def get_best_actions(actions, max_budget=500):
    max_budget = max_budget * 100  # en centimes

    # on définit le nombre d'actions
    nb_actions = len(actions)

    # on crée une liste de 50 001 zéros, chaque zéro sera remplacé par le meilleur benef pour un budget : budget[5000] = meilleurs bénéfices des actions (ayant un cout total de 50€).
    profits_table = []
    for i in range(max_budget + 1):  # de 0 à max_budget inclus
        profits_table.append(0)

    # on crée un tableau pour mémoriser quelles actions ont étés utilisés pour obtenir le meilleur benef selon un budget donné
    actions_table = []
    # on crée une rangée pour chaque action
    for i in range(nb_actions):
        row = []
        # on ajoute False autant de fois qu'il y a de possiblité de budget dans chaque rangée (50 001 fois par rangée), false deviendra true si une des actions est retenue
        for j in range(max_budget + 1):  # de 0 à max_budget inclus
            row.append(False)
        # on ajoute chaques rangées au tableau
        actions_table.append(row)

    # on remplit progressivement le tableau des bénéfices,
    # on parcourt toutes les actions
    for i in range(nb_actions):
        # on récupère le cout et le benef de l'action courante
        cost = actions[i]["cost"]
        profit = actions[i]["profit_euro"]

        # on parcourt les budgets possibles à l'envers (pour ne pas utiliser plusieurs fois une meme action) :
        # on part de 500 et on va jusqu'au budget correspondant au cout de l'action, jusqu'à arriver au cout de l'action.
        for budget in range(max_budget, cost - 1, -1):  # de max_budget à (0 + cout de l'action)

            # pour chaque budget, on calcule le benef si on prend l'action ou non

            # si on prend l'action :
            # on regarde le meilleur benef possible avec le budget restant (budget - cost) : correspond au benef avant de prendre l'action courante,
            # puis on ajoute le benef de l'action courante
            profit_if_taken = profits_table[budget - cost] + profit

            # si on ne prend pas l'action :
            # on récupère le benef déja stocké dans la liste des benefs correspondant au budget courant
            profit_if_not_taken = profits_table[budget]

            # on compare les 2 valeurs, si le bénéf avant ajout de l'action + le benef de l'action courante > benef déja stocké dans la liste profits_table
            if profit_if_taken > profit_if_not_taken:
                # on met à jour le meilleur profit pour ce budget
                profits_table[budget] = profit_if_taken
                # on passe la case correspondante (rangée = action courante, colonne = budget courant) à true dans le tableau des actions pour mémoriser son utilisation
                actions_table[i][budget] = True

    # on construit la liste des meilleures actions
    best_actions = []
    budget = max_budget

    # on parcourt la liste des actions en commencant par la dernière
    for i in range(nb_actions - 1, -1, -1):  # de nb_actions -1 à -1 (19 à 0)

        # si l'action courante a été utilisée (= true).
        if actions_table[i][budget]:
            # on l'ajoute à la liste best_actions
            best_actions.append(actions[i])
            # on met à jour le budget
            budget = budget - int(actions[i]["cost"])

    return best_actions


# Afficher la liste des meilleures actions, avec le cout total et le bénéfice total aprés 2 ans.
def display_best_actions(actions):
    total_cost = 0
    total_profit = 0
    print("Liste de la combinaison d'actions apportant le meilleur bénéfice avec un budget de 500€ :")
    print()
    for action in actions:
        print(f"{action['name']}  ->  Coût : {action['cost'] / 100}€ - Bénéfice : {round(action['profit_euro'] / 100, 2)}€")
        total_cost += action["cost"]
        total_profit += action["profit_euro"]
    print()
    print(f"Coût total : {total_cost / 100}€ - Bénéfice total : {round(total_profit / 100, 2)}€ sur {len(actions)} actions.")


def display_data_report(data):
    print()
    print(f"La liste d'actions comporte {data['nb_actions']} actions : ")
    print()
    print(f"L'action ayant le plus petit coût est : {data['min_cost'][1]} avec : {round(data['min_cost'][0] / 100, 2)}€.")
    print(f"L'action ayant le coût le plus élevé est : {data['max_cost'][1]} avec : {round(data['max_cost'][0] / 100, 2)}€.")
    print(f"La moyenne des coûts des actions est de : {round(data['average_cost'] / 100, 2)}€.")
    print()
    print(f"L'action ayant le plus petit bénéfice est : {data['min_profit'][1]} avec : {round(data['min_profit'][0] / 100, 2)}€.")
    print(f"L'action ayant le bénéfice le plus élevé est : {data['max_profit'][1]} avec : {round(data['max_profit'][0] / 100, 2)}€.")
    print(f"La moyenne des bénéfice des actions est de : {round(data['average_profit'] / 100, 2)}€.")
    print()


def main():
    raw_actions = get_data_from_csv("dataset2.csv")
    formated_actions = format_data(raw_actions)
    actions_with_profits = calculate_profit(formated_actions)

    data_actions = get_actions_informations(actions_with_profits)
    display_data_report(data_actions)

    best_actions = get_best_actions(actions_with_profits, max_budget=500)

    display_best_actions(best_actions)


if __name__ == "__main__":
    start_time = time.time()
    main()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Temps écoulé : {elapsed_time} secondes")
