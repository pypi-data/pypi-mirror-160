from masced_bandits.bandits.egreedy import egreedy
from masced_bandits.bandits.EXP3 import EXP3
from masced_bandits.bandits.EXP4 import EXP4
from masced_bandits.bandits.UCB import UCB
from masced_bandits.bandits.UCBImproved import UCBImproved
from masced_bandits.bandits.SWUCB import SWUCB
from masced_bandits.bandits.EwS import EwS
from masced_bandits.bandits.EXP3S import EXP3S
from masced_bandits.bandits.DUCB import DUCB
from masced_bandits.bandits.ETC import ETC

import numpy as np


def init_bandit(**kwargs):
    chosen_bandit = {
        "egreedy": egreedy,
        "UCB": UCB,
        "EXP3": EXP3,
        "UCBImproved": UCBImproved,
        "SWUCB": SWUCB,
        "EwS": EwS,
        "EXP3S": EXP3S,
        "EXP4": EXP4,
        "DUCB": DUCB,
        "ETC": ETC

    }.get(kwargs["name"], None)

    if(chosen_bandit):
        return chosen_bandit(**kwargs)
    else:
        raise RuntimeError("Specified Bandit " + str(chosen_bandit) + " did not exist")
