def get_actions_informations(actions):
    # Nombre d'action
    nb_actions = len(actions)

    # cout mini
    min_cost_action = min(actions, key=lambda action: action["cost"])
    min_cost = (round(min_cost_action["cost"], 2), min_cost_action["name"])
    # cout maxi
    max_cost_action = max(actions, key=lambda action: action["cost"])
    max_cost = (round(max_cost_action["cost"], 2), max_cost_action["name"])



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


    return{
        "nb_actions": nb_actions,
        "min_cost": min_cost,
        "max_cost": max_cost,
        "average_cost": average_cost,
        "min_profit": min_profit,
        "max_profit": max_profit,
        "average_profit": average_profit
    }


