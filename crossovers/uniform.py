from random import random, choice
from typing import List


def uniform_crossover(group1: List[int], group2: List[int], *, bias: float = 0) -> List[int]:
    """
    Performs uniform crossover between the two groups, and chooses one of the offspring based on a bias.
    :param List[int] group1: A list of position numbers.
    :param List[int] group2: A list of position numbers.
    :param float bias: The amount of bias either of the group have. The range of values is [-0.5, 0.5], wherein the bias
    is toward group1 and group2 respectively. So the closer to -0.5, greater than chance for
    :return: List[int]
    """

    for i in range(len(group1)):
        if random() > .5 + bias:
            group1[i], group2[i] = group2[i], group1[i]  # group2 will be swapped into group1 and vice versa

    if bias != 0:
        # if bias is > 0, more of group2 will be retained, if bias is < 0, more of group1 values would be swapped into group2.
        return group2

    return choice((group1, group2))


if __name__ == "__main__":
    g1, g2 = list(range(10)), list(range(10, 20))

    ux1 = uniform_crossover(g1.copy(), g2.copy())
    ux2 = uniform_crossover(g1.copy(), g2.copy(), bias=.4)
    ux3 = uniform_crossover(g1.copy(), g2.copy(), bias=-.4)

    print(
        f"Groups being crossover:\n"
        f"\t\033[4mGroup1\033[0m: \033[1m{g1}\033[0m\n"
        f"\t\033[4mGroup2\033[0m: \033[1m{g2}\033[0m\n\n"
        f"Bias: \033[1m0.5\033[0m:\t{ux1}\n"
        f"Bias: \033[1m0.4\033[0m:\t{ux2}\n"
        f"Bias: \033[1m-0.4\033[0m:\t{ux3}\n"
    )
