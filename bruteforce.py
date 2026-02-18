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


# # trier les actions par pourcentage de bénéfice croissant (meilleurs bénéfices)
# def sort_actions_by_profit(actions):
#     return sorted(actions, key=lambda action: action["profit_percent"])
#
#
# # récupérer la meilleure combinaison d'action sans dépasser 500€ de budget
# def get_best_actions(actions):
#     best_actions = []
#     total_cost = 0
#     i = 1
#     while i <= len(actions) :
#         if total_cost + actions[-i]["cost"] <= 500:
#             best_actions.append(actions[-i])
#             total_cost += actions[-i]["cost"]
#         i += 1
#     return best_actions



# récupérer la meilleure combinaison d'action en testant toutes les combinaisons sans dépasser 500€ de budget avec récusivité
# la fonction combinations du module itertools permet de faire la meme chose plus simplement (recursivité pour comprendre)
def get_best_actions(actions, max_budget=500):

    # on test toutes les combinaison possibles
    def test_best_actions(index, current_combination, current_cost, current_profit):
        # On définit les variables meilleure combinaison et meilleur benef = combinaison et benef courrant.
        # Ce sont des valeurs de référence avec d'explorer la branche de recusivité courante.
        best_profit = current_profit
        best_combination = current_combination

        # condition d'arret (si on dépasse le budget)
        if current_cost > max_budget:
            return 0, []

        # on explore toutes les combinaisons uniques
        # On boucle sur toutes les actions à partir de l'index courant (evite les doublons et les combinaisons inversées).
        for i in range(index, len(actions)):
            action = actions[i] # on stock l'action courrante

            # on récupère la combinaison d'actions et le profit correspondant via la recursivité
            profit, combination = test_best_actions(
                i+1, # index correspondant à l'action d'aprés (permet de récupérer toutes les combinaisons en excluant l'action courrante)
                current_combination + [action], # combinaison d'action à laquelle on ajoute l'action courrante, on construit progressivement la combinaison
                current_cost + action["cost"], # Mise à jour du cout
                current_profit + action["profit_euro"]) # Mise à jour des benefs

            # si le benef total de la combinaison est > au meilleur benef, on met à jour le best benef et la best combinaison
            if profit > best_profit:
                best_profit = profit
                best_combination = combination

        # on retourne la meilleure combinaison avec le benef total correspondant
        return best_profit, best_combination

    _, best_actions = test_best_actions(0, [], 0, 0)

    return best_actions



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

    # actions_sorted = sort_actions_by_profit(actions_with_profits)
    # best_actions = get_best_actions(actions_sorted)

    best_actions = get_best_actions(actions_with_profits, max_budget=500)


    display_best_actions(best_actions)






main()