import csv
from pathlib import Path
# from pprint import pprint

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

        # # Nettoyage pour la section 3
        # if action['price'] == "0.0":
        #     continue
        # cleaned_action = {
        #     "name": action["name"],
        #     "cost": float(action["price"]),
        #     "profit_percent": float(action["profit"]) / float(action["price"])
        # }

        cleaned_actions.append(cleaned_action)
    return cleaned_actions


# Calculer le bénéfice en euro de chaque action (bénéfice% * prix action)
def calculate_profit(actions):
    for action in actions:
        action["profit_euro"] = round(action["cost"] * action["profit_percent"],2)
    return actions




# obtenir la meilleure combinaison d'action selon l'algorithme knapsack dynamique
def get_best_actions(actions, max_budget=500):

    # on définit le nombre d'actions
    nb_actions = len(actions)


    # on crée une liste de 501 zéros, chaque zéro sera remplacé par le meilleur benef pour un budget : budget[50] = meilleurs bénéfices des actions (ayant un cout total de 50€).
    profits_table = []
    for i in range(max_budget + 1): # de 0 à max_budget inclus
        profits_table.append(0)


    # on crée un tableau pour mémoriser quelles actions ont étés utilisés pour obtenir le meilleur benef selon un budget donné
    actions_table = []
    # on crée une rangée pour chaque action
    for i in range(nb_actions):
        row = []
        # on ajoute False autant de fois qu'il y a de possiblité de budget dans chaque rangée (501 fois par rangée), false deviendra true si une des actions est retenue
        for j in range(max_budget + 1): # de 0 à max_budget inclus
            row.append(False)
        # on ajoute chaques rangées au tableau
        actions_table.append(row)


    # on remplit progressivement le tableau des bénéfices,
    # on parcourt toutes les actions
    for i in range(nb_actions):
        # on récupère le cout et le benef de l'action courante
        cost = actions[i]["cost"]
        profit = actions[i]["profit_euro"]

        # on parcourt les budgets possibles à l'envers (pour ne pas utiliser plusieurs fois une action) :
        # on part de 500 et on va jusqu'au budget correspondant au cout de l'action, jusqu'à arriver au cout de l'action.
        for budget in range(max_budget, cost - 1 , -1):

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
                # on passe la case (rangée = action courante, colonne = budget courant) correspondante à true dans le tableau des actions pour mémoriser son utilisation
                actions_table[i][budget] = True


    # on construit la liste des meilleures actions
    best_actions = []
    budget = max_budget

    # on parcourt la liste des actions en commencant par la dernière
    for i in range(nb_actions-1, -1, -1):

        # si l'action courante a été utilisée
        if actions_table[i][budget]:
            # on l'ajoute à la liste best_actions
            best_actions.append(actions[i])
            # on met à jour le budget
            budget = budget - actions[i]["cost"]

    return best_actions



# Afficher la liste des meilleures actions, avec le cout total et le bénéfice total aprés 2 ans.
def display_best_actions(actions):
    total_cost = 0
    total_profit = 0
    print("Liste de la combinaison d'actions apportant le meilleur bénéfice avec un budget de 500€ :")
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

    get_best_actions(actions_with_profits, max_budget=500)



    # best_actions = get_best_actions(actions_with_profits, max_budget=500)
    #
    # display_best_actions(best_actions)


if __name__ == "__main__":

    main()
