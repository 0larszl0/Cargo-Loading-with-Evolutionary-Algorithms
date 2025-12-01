from random import sample, choice, shuffle
from typing import List


def davis_order_crossover(group1: List[int], group2: List[int]) -> List[int]:
    """
    Performs Davis-Order Crossover (OX1) across both groups. OX1 is modified in this case to handle groups that don't
    contain the same elements in different orders. However, this means that there is a chance to lose some potentially
    valuable data.
    :param List[int] group1: A list of position numbers.
    :param List[int] group2: A list of position numbers.
    :return: List[int]
    """
    # Create two random crossover points
    low_point, high_point = sorted(sample(range(len(group1)), k=2))

    # Get length of group and the crossover values for each group
    group_len = len(group1)  # length of group1 and group2 should be identical
    group1_cx, group2_cx = group1[low_point: high_point], group2[low_point: high_point]

    # Create child instances, and add the crossover values into each respectively.
    child1, child2 = [None] * group_len, [None] * group_len
    child1[low_point:high_point], child2[low_point:high_point] = group1_cx, group2_cx

    # Gathers all the possible values each group can contain of the other.
    g1_possible = [position for position in group2_cx + group2[:low_point] + group2[high_point:] if position not in group1_cx]
    g2_possible = [position for position in group1_cx + group1[:low_point] + group1[high_point:] if position not in group2_cx]

    # Inserts the values that match the missing spaces
    child1[:low_point], child1[high_point:] = g1_possible[:low_point], g1_possible[low_point:low_point + (group_len - high_point)]
    child2[:low_point], child2[high_point:] = g2_possible[:low_point], g2_possible[low_point:low_point + (group_len - high_point)]

    return choice((child1, child2))


if __name__ == "__main__":
    g1, g2 = list(range(10)), list(range(10))
    shuffle(g1), shuffle(g2)

    g3 = sample(range(20), k=10)

    ox1 = davis_order_crossover(g1, g2)
    ox2 = davis_order_crossover(g1, g3)

    lost_values = (set(g1) | set(g3)).difference(ox2)

    print(
        f"Groups being crossed:\n"
        f"\t\033[4mGroup1\033[0m: \033[1m{g1}\033[0m\n"
        f"\t\033[4mGroup2\033[0m: \033[1m{g2}\033[0m\n"
        f"\t\033[4mGroup3\033[0m: \033[1m{g3}\033[0m\n\n"
        f"Output between groups containing similar items (g1 & g2): {ox1}\n"
        f"Output between groups containing differing items (g1 & g3): {ox2}\n"
        f"\t|__ Lost values: \033[1m{lost_values}\033[0m"
    )
