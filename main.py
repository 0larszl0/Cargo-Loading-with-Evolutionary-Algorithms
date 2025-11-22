from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, ArrowStyle
import matplotlib.pyplot as plt
from typing import List
from math import dist
from utils import *
import random

random.seed(42)

# -- Initialise container types -- #
# Define unit container size
CONTAINER_WIDTH, CONTAINER_HEIGHT = (20., 15.)

# Define the number of sides a cylinder will have
CYLINDER_SIDES = 8

# Define cylinder containers: [(Weight, Diameter)]
CYLINDERS = [
    (2500, 2.),  # Heavy tank
    (800, 1.5),  # Medium drum
    (300, 1.2)   # Light barrel
]


class Cylinder:
    """Represents a cylinder of a particular type."""

    def __init__(self, sides: int, radius: float, weight: int):
        self.__sides = sides
        self.__radius = radius
        self.__weight = weight

        self.__centre = (0., 0.)

    @property
    def centre(self) -> Tuple[float, float]:
        return self.__centre

    @centre.setter
    def centre(self, new_centre: Tuple[float, float]) -> None:
        self.__centre = new_centre

    @property
    def radius(self) -> float:
        return self.__radius

    @property
    def weight(self) -> int:
        return self.__weight

    def left(self) -> float:
        return self.__centre[0] - self.__radius

    def right(self) -> float:
        return self.__centre[0] + self.__radius

    def top(self) -> float:
        return self.__centre[1] + self.__radius

    def bottom(self) -> float:
        return self.__centre[1] - self.__radius


class CylinderGroup:
    """Contains cylinders in a particular grouping."""

    def __init__(self, cylinders: List[Cylinder], num_cylinders: int, cylinder_sides: int, max_weight: int):
        self.__cylinders = cylinders
        self.__num_cylinders = num_cylinders
        self.__cylinder_sides = cylinder_sides
        self.__max_weight = max_weight

        self.__weight = cylinders[0].weight
        self.__generation = 0

        # A group will contain a list of random position numbers for each cylinder, apart from the first as that is
        # to be placed in the centre of the container.
        self.__group = random.sample(range(num_cylinders * cylinder_sides), k=num_cylinders - 1)

    def recycle(self, cylinders: List[Cylinder], grouping: List[int]) -> None:
        """
        Reuses the cylinder group by resetting several properties like weight and to contain a new grouping.
        :param List[Cylinder] cylinders: The original cylinder list, this is in case that some cylinders were previously
        removed during the decoding process.
        :param List[int] grouping: The new group this group will contain.
        :return: None
        """
        # Increment internal generation in here
        ...

    def decode(self, debug: bool = False) -> None:
        """
        Decodes the position numbers within the group.
        :param bool debug: Whether to show debug messages or not.
        :return: None
        """
        cprint(debug, f"Outputting decoding process for: {self.__group}")

        for i in range(self.__num_cylinders - 1):
            # Check if the position number is greater than the maximum position number for the ith circle being seen.
            max_positions = (i + 1) * self.__cylinder_sides
            if self.__group[i] > max_positions:
                # if it is reset the position number to 0
                self.__group[i] = 0

            cprint(debug, f"+----\tWorking on cylinder: {i + 1}/{self.__num_cylinders - 1}\t----+")
            self.__group[i] = self.check_feasibility(self.__group[i], self.__cylinders[i + 1], max_positions, max_positions, debug)
            cprint(debug, f"Final position: {self.__group[i]}, with position: {self.__cylinders[i + 1].centre}\n")

            if self.__group[i] != -1:
                self.__weight += self.__cylinders[i + 1].weight
                continue

            # reduce the number of cylinders if a position had failed.
            self.__num_cylinders -= 1

        print(self.__group)

        # --- Filter any -1 positions and any cylinders at those positions --- #
        # 1. Zip the group and all the cylinders (apart from the first) together
        # 2. Filter out any pair that has a -1 position number
        filtered_pairs = list(filter(lambda x: x[0] != -1, zip(self.__group, self.__cylinders[1:])))

        self.__group, self.__cylinders = [], self.__cylinders[:1]  # set values in case there are no successful pairs
        if filtered_pairs:  # check if there are successful pairs
            # 2a. Unpair the results, convert them to lists, and assign appropriately
            self.__group, filtered_cylinders = map(lambda x: list(x), zip(*filtered_pairs))

            # 2b. Add the filtered cylinders after it.
            self.__cylinders += filtered_cylinders

    def check_feasibility(self, position: int, cylinder: Cylinder, total_positions: int, positions_left: int, debug: bool = False) -> int:
        """
        Checks whether a cylinder will be placed at a feasible position.
        :param int position: The position that is being checked.
        :param Individual cylinder: The cylinder that is being evaluated.
        :param int total_positions: The total number of possible positions at the position index.
        :param int positions_left: The number of positions left to check
        :param bool debug: Whether the function should output the decoding process.
        :return: int, A feasible position. This would be the passed argument if it succeeded, or -1 if the cylinder
        should be discarded.
        """
        cprint(debug, f"Evaluating Position:\t{position}")

        # - Recursion terminator - #
        if positions_left == 0:  # if we have looped through all possible positions and are back to the original position.
            return -1

        # -- Weight -- #
        if cylinder.weight + self.__weight > self.__max_weight:
            return -1

        # -- Geometric -- #
        # - Adjust centre of cylinder based on the position number - #

        # Get the cylinder corresponding to the position
        target_cylinder = self.__cylinders[position // self.__cylinder_sides]
        cprint(debug, f"Targeting Cylinder: \t{position // self.__cylinder_sides}\n\t- Weight: {target_cylinder.weight}\t- Radius: {target_cylinder.radius}\t- Centre: {target_cylinder.centre}")

        # Preset the point to the right position of the target cylinder such that both cylinders touch one another
        positioned_point = (target_cylinder.centre[0] + target_cylinder.radius + cylinder.radius, target_cylinder.centre[1])
        cprint(debug, f"Preset position is:\t{positioned_point}")

        # Rotate the positioned point by a radian amount defined by the side number multiplied by the distance between each side.
        cylinder.centre = rotate(
            target_cylinder.centre,
            positioned_point,
            radians((position % self.__cylinder_sides) * (360 / self.__cylinder_sides))
        )
        cprint(debug, f"Rotated position:\t({cylinder.centre[0]:.4f}, {cylinder.centre[1]:.4f})")

        # - Container-based - #
        # Check if cylinder fits within the container based on its current position.
        if (cylinder.left() < 0 or cylinder.right() > CONTAINER_WIDTH) or \
                (cylinder.bottom() < 0 or cylinder.top() > CONTAINER_HEIGHT):
            cprint(debug, "\033[31m\t---- Doesn't fit in container ----\033[0m")

            # in the case it's not fully in the container, move to the next position
            return self.check_feasibility((position + 1) % total_positions, cylinder, total_positions, positions_left - 1, debug)

        cprint(debug, f"\033[32m\t---- Fits inside the container! ----\033[0m")

        # - Neighbour-based - #
        # Check if the cylinder intersects in more than one place with another already placed cylinder.
        for i, individual in enumerate(self.__cylinders[:(total_positions // self.__cylinder_sides) + 1]):
            # checks whether the distance between the two cylinder centres is less than the sum of their radii.
            # allow a small tolerance (0.01) for any rotations.
            if (individual != cylinder) and (dist(individual.centre, cylinder.centre) < individual.radius + cylinder.radius -.01):
                cprint(debug, f"\033[31m\t---- Intersects with Cylinder {i} ----\033[0m", dist(individual.centre, cylinder.centre), individual.radius + cylinder.radius)

                # individual intersects! Therefore, another position needs to be used.
                return self.check_feasibility((position + 1) % total_positions, cylinder, total_positions, positions_left - 1, debug)

        cprint(debug, f"\033[32m\t---- No intersections detected! ----\033[0m")

        return position

    def com(self) -> Tuple[float, float]:
        """
        Calculate the group's centre of mass (COM) in each axis.
        :return: Tuple[float]
        """
        # Get a list of masses multiplied by their axis (MMA)
        mma_x, mma_y = zip(*[(cylinder.weight * cylinder.centre[0], cylinder.weight * cylinder.centre[1]) for cylinder in self.__cylinders])

        return sum(mma_x) / self.__weight, sum(mma_y) / self.__weight

    def visualise(self, lenience: float = .6) -> None:
        """
        Sketches the cylinders within this group in their appropriate locations.
        :param float lenience: The size of the region of acceptance for the overall groups centre of mass. This is to
        visually show whether the group meets the weight distribution criteria.
        :return: None
        """
        # The Figure itself will display as the container.
        fig, ax = plt.subplots(figsize=(10, 10))

        # Draw weight distribution container (central container -> cc)
        cc_width, cc_height = CONTAINER_WIDTH * lenience, CONTAINER_HEIGHT * lenience
        cc_pos = ((CONTAINER_WIDTH - cc_width) / 2, (CONTAINER_HEIGHT - cc_height) / 2)
        cc = Rectangle(cc_pos, cc_width, cc_height,
                              fill=False, edgecolor="#F4BA02", linewidth=2, linestyle="--", label="Central container")
        ax.add_patch(cc)

        # Plot each cylinder and their details
        for cylinder in self.__cylinders:
            # Plot the circle representing a cylinder.
            cylinder_patch = Circle(cylinder.centre, cylinder.radius, fill=False, edgecolor="#99D9DD", linewidth=2)
            ax.add_patch(cylinder_patch)

            # Plot a <-> arrow to signify diameter.
            arrow_style = ArrowStyle.CurveAB(head_length=cylinder.radius * 4, head_width=cylinder.radius * 1.6)
            arrow_patch = FancyArrowPatch((cylinder.left(), cylinder.centre[1]), (cylinder.right(), cylinder.centre[1]),
                                          arrowstyle=arrow_style, color="#AFD8DB", alpha=.4)
            ax.add_patch(arrow_patch)

            # Plot cylinder info like diameter and weight
            ax.text(cylinder.centre[0], cylinder.centre[1] + (cylinder.radius * .35), f"{cylinder.radius * 2}Ø",
                    ha="center", va="center", color="#F7F8F9", fontsize=8 * cylinder.radius)

            ax.text(cylinder.centre[0], cylinder.centre[1] - (cylinder.radius * .35), f"{cylinder.weight}kg",
                    ha="center", va="center", color="#F7F8F9", fontsize=8 * cylinder.radius)

            # Plot the centre of the drawn cylinder
            ax.plot(cylinder.centre[0], cylinder.centre[1], 'o', color="#99D9DD", markersize=4)

        # Mark centre of container
        centre_x, centre_y = CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2
        ax.plot(centre_x, centre_y, 'x', color='#F4BA02', markersize=6, markeredgewidth=3, label='Origin')

        # Mark the group's centre of mass.
        x_com, y_com = self.com()
        ax.plot(x_com, y_com, 'x', color="#E21F4A", markersize=6, markeredgewidth=3, label="Centre of Mass")

        # - Set up axis - #
        ax.set_aspect("equal")
        ax.set_xlim(0, CONTAINER_WIDTH)
        ax.set_ylim(0, CONTAINER_HEIGHT)

        ax.grid(True, alpha=.15, color="#F7F8F9")
        ax.spines[:].set_color("#F7F8F9")
        ax.tick_params(colors="#F7F8F9")
        ax.set_facecolor("#01364C")

        ax.set_title(
            f"Optimised solution for {self.__num_cylinders} cylinder{'s' if self.__num_cylinders > 1 else ''} at generation {self.__generation}\n"
            f"Distance between packed COM and container centre: {dist((x_com, y_com), (centre_x, centre_y)):.3f}\n"
            f"Packed weight: {self.__weight}/{self.__max_weight}",
            color="#F7F8F9", fontsize=14, pad=20, weight="bold"
        )
        ax.legend(loc='upper right', facecolor='#01364C', edgecolor='#F7F8F9', labelcolor='#F7F8F9', framealpha=0.9)

        fig.patch.set_facecolor("#01364C")
        plt.show()


class Population:
    """Manages a population of individuals and evolutionary operations inside a container."""

    def __init__(self, size: int, num_cylinders: int, mutation_rate: float, max_generations: int, cylinder_sides: int,
                 max_weight):
        self.__size = size
        self.__mutation_rate = mutation_rate
        self.__max_generations = max_generations

        self.__generations = 0

        # - Initialise cylinders - #
        # Get a random selection of different cylinder types and save them as objects
        self.__cylinders = [Cylinder(CYLINDER_SIDES, diameter / 2, weight) for weight, diameter in random.choices(CYLINDERS, k=num_cylinders)]

        # Sorts the cylinders in descending order based on size (radius)
        self.__cylinders = sorted(self.__cylinders, reverse=True, key=lambda x: x.weight)

        # Drop all large cylinders that already exceed the maximum weight
        while self.__cylinders and self.__cylinders[0].weight > max_weight:
            del self.__cylinders[0]
            num_cylinders -= 1

        if not self.__cylinders:
            raise Exception(f"\r\033[1m\033[31mCustom Exception: No cylinder can be packed with a maximum weight limit of: {max_weight}")

        # Sets the first cylinder's centre to the middle of the container.
        self.__cylinders[0].centre = (CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2)

        print("+-----------\tInitialised cylinders\t-----------+")
        for i, cylinder in enumerate(self.__cylinders):
            print(f"Cylinder {i+1}:\t- Weight: {cylinder.weight}\t- Centre: {cylinder.centre}\t- Radius: {cylinder.radius}")

        # - Initialise population with random position strings - #
        self.__population = [CylinderGroup(self.__cylinders, num_cylinders, cylinder_sides, max_weight) for _ in range(size)]
        print(f"\nSample of population: {random.sample(self.__population, k=3)}\n")

    def decode(self) -> None:
        """
        Decodes the population to ensure each group of cylinders is grouped feasibly.
        :return: None
        """
        for i, cylinder_group in enumerate(self.__population):
            cylinder_group.decode(i == 0)
            cylinder_group.visualise()
            break

    def evolve(self):
        """Run a single generation of the genetic algorithm."""
        self.decode()



if __name__ == "__main__":
    population = Population(50, 5, .1, 100, CYLINDER_SIDES, 400)
    population.evolve()
