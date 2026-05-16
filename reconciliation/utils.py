import random


def simulate_random_failure():

    if random.randint(1, 4) == 1:
        raise Exception(
            "Random stage failure"
        )