import ast
import secrets

import numpy as np
from core.util import format_number


def roll_asset_random(asset_list):
    return asset_list[secrets.randbelow(len(asset_list))]


def lucky_item_pool_roll(chance, asset_list, probabilites):
    dec = format_number(str(chance)).split(".")
    if len(dec) != 1:
        scale = int(10 ** len(dec[-1]))
    else:
        scale = 1
    if secrets.randbelow(scale) / scale <= chance:
        return probability_roll(asset_list, probabilites)
    else:
        return ""


def probability_roll(asset_list, probabilites):
    if probabilites == "Evens":
        return [roll_asset_random(asset_list), 1 / len(asset_list)]
    else:
        if isinstance(probabilites, str) == True:
            probabilites = ast.literal_eval(probabilites)
        roll = np.random.choice(np.arange(0, len(asset_list)), p=probabilites)
        return [asset_list[roll], probabilites[roll]]
