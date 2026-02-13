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


# Calculer le bénéfice en euro de chaque action (bénéfice% * prix action)
def calculate_profit(actions):
    for action in actions:
        action["profit_euro"] = round(action["cost"] * action["profit_percent"],2)
    return actions


# trier les actions par pourcentage de bénéfice croissant (meilleurs bénéfices)
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


# # récupérer la meilleure combinaison d'action sans dépasser 500€ de budget avec récusivité
# def get_best_actions(best_actions, actions, cost):
#
#     # condition d'arret (plus aucune action)
#     if not actions:
#         return best_actions
#
#     # on stock la premiere action dans une varaible
#     best_action = actions[0]
#     # on boucle sur le nombre d'action
#     for i in range(1, len(actions)):
#         # on stock la prochaine action dans une variable
#         next_action = actions[i]
#         # si la prochaine action est mieux que la premiere on la remplace
#         if next_action["profit_percent"] > best_action["profit_percent"]:
#             best_action = actions[i]
#
#     # on copie la liste des actions
#     remaining_actions = actions[:]
#
#     # si l'action + les couts dépassent le budget alors on l'enleve de remaining actions
#     if cost + best_action["cost"] > 500:
#         remaining_actions.remove(best_action)
#         # on lance la recursivité avec les actions restantes
#         return get_best_actions(best_actions, remaining_actions, cost)
#
#     # sinon on ajoute l'action à best_actions
#     best_actions.append(best_action)
#     # on l'enleve de remaining actions
#     remaining_actions.remove(best_action)
#     # on recalcul le cout total
#     cost += best_action["cost"]
#
#     # on applique la recusivité en passant les nouvelles listes et le cout total mis à jour
#     return get_best_actions(best_actions, remaining_actions, cost)


# Afficher la liste des meilleures actions, avec le cout total et le bénéfice total aprés 2 ans.
def display_best_actions(actions):
    total_cost = 0
    total_profit = 0
    print("Liste de la combinaison d'actions apportant le meilleur bénfice avec un budget de 500€ :")
    print()
    for action in actions:
        print(f"{action['name']}  ->  Coût : {action['cost']}€ - Bénéfice : {action['profit_euro']}€")
        total_cost += action["cost"]
        total_profit += action["profit_euro"]
    print()
    print(f"Coût total : {total_cost}€ - Bénéfice total : {round(total_profit, 2)}€")




def main():
    raw_actions = get_data_from_csv("data_actions.csv")
    cleaned_actions = clean_data(raw_actions)
    actions_with_profits = calculate_profit(cleaned_actions)
    actions_sorted = sort_actions_by_profit(actions_with_profits)
    best_actions = get_best_actions(actions_sorted)

    # best_actions = get_best_actions([], actions_with_profits, 0)

    display_best_actions(best_actions)






main()