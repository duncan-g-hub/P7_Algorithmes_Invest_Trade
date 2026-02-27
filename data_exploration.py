def get_actions_informations(actions):
    # Nombre d'action
    nb_actions = len(actions)

    # cout mini
    min_cost = (round(min(actions, key=lambda action: action["cost"])["cost"], 2),
                min(actions, key=lambda action: action["cost"])["name"])
    # cout maxi
    max_cost = (round(max(actions, key=lambda action: action["cost"])["cost"], 2),
                max(actions, key=lambda action: action["cost"])["name"])



    # cout moyen
    total_cost = sum(action["cost"] for action in actions)
    average_cost = round(total_cost / nb_actions, 2)


    # benef mini
    min_profit = (round(min(actions, key=lambda action: action["profit_euro"])["profit_euro"], 3),
                  min(actions, key=lambda action: action["profit_euro"])["name"])
    # benef maxi
    max_profit = (round(max(actions, key=lambda action: action["profit_euro"])["profit_euro"], 3),
                  max(actions, key=lambda action: action["profit_euro"])["name"])
    # benef moyen
    total_profit = sum(action["profit_euro"] for action in actions)
    average_profit = round(total_profit / nb_actions, 2)


    display_data_report({
        "nb_actions": nb_actions,
        "min_cost": min_cost,
        "max_cost": max_cost,
        "average_cost": average_cost,
        "min_profit": min_profit,
        "max_profit": max_profit,
        "average_profit": average_profit
    })


def display_data_report(data):
    print()
    print(f"La liste d'actions comporte {data['nb_actions']} actions : ")
    print()
    print(f"L'action ayant le plus petit coût est : {data['min_cost'][1]} avec : {data['min_cost'][0]}€.")
    print(f"L'action ayant le coût le plus élevé est : {data['max_cost'][1]} avec : {data['max_cost'][0]}€.")
    print(f"La moyenne des coûts des actions est de : {data['average_cost']}€.")
    print()
    print(f"L'action ayant le plus petit bénéfice est : {data['min_profit'][1]} avec : {data['min_profit'][0]}€.")
    print(f"L'action ayant le bénéfice le plus élevé est : {data['max_profit'][1]} avec : {data['max_profit'][0]}€.")
    print(f"La moyenne des bénéfice des actions est de : {data['average_profit']}€.")
    print()