# MASCed_bandits
This is a library of multi-armed bandit policies.
As of the most recent version the following policies are included:
UCB, UCB-Improved, EXP3, EXP3S, EXP4, EwS, ETC, Discounted UCB, Sliding Window UCB, e-greedy.
# Example

    from masced_bandits.bandit_options import initialize_arguments
    from masced_bandits.bandits import init_bandit
    import numpy as np

    initialize_arguments(["Arm1","Arm2"], 0)

    ucb_instance = init_bandit(name='UCB')
    for i in range(100):
        arms_chosen = []
        reward = np.random.random()
        arms_chosen.append(ucb_instance.get_next_arm(reward))