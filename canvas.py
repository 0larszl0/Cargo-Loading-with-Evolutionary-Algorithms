from matplotlib.artist import Artist
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib import animation
from config import CONTAINER_WIDTH, CONTAINER_HEIGHT
import matplotlib.pyplot as plt
from cylinders import Cylinder, CylinderGroup
from custom_patches.circle import CustomCircle
from typing import List, Dict, Tuple, Iterable, Union
from utils import com


class Container:
    def __init__(self, **subplot_kwargs):
        self._fig, self._ax = plt.subplots(**subplot_kwargs)

        self._best_cylinder_group: Union[CylinderGroup, None] = None
        self._cylinder_patches: List[CustomCircle] = []
        self._com_marker: Union[Line2D, None] = None

    @property
    def best_cylinder_group(self) -> Union[CylinderGroup, None]:
        return self._best_cylinder_group

    @best_cylinder_group.setter
    def best_cylinder_group(self, new_best: CylinderGroup) -> None:
        self._best_cylinder_group = new_best

    def add_cylinders(self) -> None:
        """
        Creates CustomCircle objects that correspond to each cylinder in the best_cylinder_group's cylinders respectively.
        :return: None
        """
        if self._best_cylinder_group is None:  # checks whether the best cylinder group has been set.
            raise Exception("\r\033[1m\033[31mCustom Exception: Ensure that the best cylinder group is set before calling Container.add_cylinders()\033[0m")

        for cylinder in self._best_cylinder_group.cylinders:
            # append a CustomCircle object at position (0, 0), this will be changed when saving states.
            self._cylinder_patches.append(
                CustomCircle((0, 0), cylinder.radius, cylinder.weight, fill=False, edgecolor="#99D9DD", linewidth=2))

    def draw_patches(self) -> None:
        """
        Adds the cylinder patches onto an axes.
        :return: None
        """
        for cylinder_patch in self._cylinder_patches:
            cylinder_patch.add_to(self._ax)

    def draw_acceptance_range(self, weight_range: float = .6, rect_color: str = "#F4BA02") -> None:
        """
        Draws the weight distribution container (wbc) to the figure.
        :param float weight_range: The proportion of the container/figure.
        :param str rect_color: The hex-colour of the rectangle's outline.
        :return: None
        """
        wbc_width, wbc_height = CONTAINER_WIDTH * weight_range, CONTAINER_HEIGHT * weight_range
        wbc_pos = ((CONTAINER_WIDTH - wbc_width) / 2, (CONTAINER_HEIGHT - wbc_height) / 2)

        wbc = Rectangle(wbc_pos, wbc_width, wbc_height, fill=False, edgecolor=rect_color, linewidth=2, linestyle="--", label="Central container")

        self._ax.add_patch(wbc)

    def draw_centre(self, marker_colour: str = "#F4BA02") -> None:
        """
        Add a marker indicating the centre of the figure/container. This marker does not need to be tracked.
        :param str marker_colour: The hex-colour of the marker.
        :return: None
        """
        self._ax.plot(CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2, 'x', color=marker_colour, markersize=6, markeredgewidth=3, label='Origin')

    def draw_com_marker(self) -> None:
        """
        Draws the Center of Mass marker onto the screen.
        :return: None
        """
        x_com, y_com = com(self._cylinder_patches, self._best_cylinder_group.weight)

        self._com_marker = self._ax.plot(x_com, y_com, 'x', color="#E21F4A", markersize=6, markeredgewidth=3, label="Centre of Mass")[0]

    def set_title(self, title: str, colour: str = "#F7F8F9") -> None:
        """
        Sets a title to the figure.
        :param str title: The title to set.
        :param str colour: The colour of the title.
        :return: None
        """
        self._ax.set_title(title, color=colour, fontsize=14, pad=20, weight="bold")

    def setup_axis(self, *, spine_colour: str = "#F7F8F9", tick_colour: str = "#F7F8F9", grid_colour: str = "#F7F8F9",
                   face_colour: str = "#01364C", legend_colour: str = "#F7F8F9", figure_face_colour: str = "#01364C") -> None:
        """
        Set aspect ratios, x & y limits, a title, colours and a legend.
        :return: None
        """
        # - Set up axis - #
        self._ax.set_aspect("equal")
        self._ax.set_xlim(0, CONTAINER_WIDTH)
        self._ax.set_ylim(0, CONTAINER_HEIGHT)

        self._ax.grid(True, alpha=.15, color=grid_colour)
        self._ax.spines[:].set_color(spine_colour)
        self._ax.tick_params(colors=tick_colour)
        self._ax.set_facecolor(face_colour)

        self._ax.legend(loc='upper right', facecolor=face_colour, edgecolor=legend_colour, labelcolor=tick_colour, framealpha=0.9)

        self._fig.patch.set_facecolor(figure_face_colour)

    @staticmethod
    def show() -> None:
        """
        Shows the figure containing all the artists.
        :return: None
        """
        plt.show()


class AnimatedContainer(Container):
    def __init__(self, fpp: int, **subplot_kwargs):
        super().__init__(**subplot_kwargs)

        # frames per patch, how many positions to move in between each position.
        # Say you're going from (8, y) -> (9, y), with fpp = 60, you have to move in increments of (9-8) / 60
        self.__fpp = fpp

        self.__frame = -1
        self.__save_index = -1

        self.__save_states = {}  # {Cylinder patch: [[List of different centres deemed best at particular generations], [A list of increments between 'i' and 'i+1' centres]]}
        self.__saved_generations = []

    @property
    def save_states(self) -> Dict[Cylinder, Tuple[float, float]]:
        return self.__save_states

    def save_state(self, generation: int) -> None:
        """
        Saves the new position of each cylinder associated with an artist.
        :param int generation: The generation to save at.
        :return: None
        """
        for i, cylinder in enumerate(self._best_cylinder_group.cylinders):
            cylinder_patch = self._cylinder_patches[i]

            # check whether a save state exists for a cylinder patch
            if not self.__save_states.get(cylinder_patch, False):
                # - if no save exists - #
                # Add a save state for that patch
                self.__save_states[cylinder_patch] = [[cylinder.centre], []]

                # Set the starting position for that patch
                cylinder_patch.set_position(cylinder.centre)

                continue

            # Record the new best centre for a cylinder patch
            self.__save_states[cylinder_patch][0].append(cylinder.centre)

            # Append the x and y increments the patch needs to make each frame to get to the new centre.
            self.__save_states[cylinder_patch][1].append((
                (self.__save_states[cylinder_patch][0][-1][0] - self.__save_states[cylinder_patch][0][-2][0]) / self.__fpp,
                (self.__save_states[cylinder_patch][0][-1][1] - self.__save_states[cylinder_patch][0][-2][1]) / self.__fpp
            ))

        # Record the generation that improved the pre-existing solution.
        self.__saved_generations.append(generation)

    def update_com_marker(self) -> None:
        """
        Updates the x and y positions of the com marker, based on cylinder patch positions and weights.
        :return: None
        """
        x_com, y_com = com(self._cylinder_patches, self._best_cylinder_group.weight)

        self._com_marker.set_xdata([x_com])
        self._com_marker.set_ydata([y_com])

    def update(self, _) -> Iterable[Artist]:
        """
        Updates the artist's positions based on the difference between the current position and the next whilst
        incorporating the amount of fps the animation will have.
        :return: Iterable[Artist]
        """
        if self.__frame == -1:
            self.__save_index += 1
            self.__frame += 1
            return self._cylinder_patches

        for i, cylinder in enumerate(self._best_cylinder_group.cylinders):
            cylinder_patch = self._cylinder_patches[i]

            x_incr, y_incr = self.__save_states[cylinder_patch][1][self.__save_index]
            cylinder_patch.set_position((cylinder_patch.centre[0] + x_incr, cylinder_patch.centre[1] + y_incr))

        self.update_com_marker()

        self.__frame += 1
        if self.__frame == 60:
            self.__frame = -1

        return self._cylinder_patches

    def show(self) -> None:
        """
        An override of the child method.
        :return: None
        """
        frames = (len(self.__saved_generations) - 1) * self.__fpp  # calculates the total number of frames for this animation.
        anim = animation.FuncAnimation(fig=self._fig, func=self.update, frames=frames, interval=0, repeat=False)
        plt.show()



if __name__ == "__main__":
    d = AnimatedContainer(60, figsize=(10, 10))

    d.draw_acceptance_range()
    d.draw_centre()
    d.setup_axis()

    plt.show()