from matplotlib.artist import Artist
from matplotlib.patches import Rectangle
from matplotlib import animation
from config import CONTAINER_WIDTH, CONTAINER_HEIGHT
import matplotlib.pyplot as plt
from cylinders import Cylinder
from custom_patches.circle import CustomCircle
from typing import List, Dict, Tuple


class Canvas:
    def __init__(self, **subplot_kwargs):
        self._fig, self._ax = plt.subplots(**subplot_kwargs)

        self._artists: Dict[Cylinder, CustomCircle] = {}  # {Reference of object: Reference of custom patch}

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

    def mark_centre(self, marker_colour: str = "#F4BA02") -> None:
        """
        Add a marker indicating the centre of the figure/container.
        :param str marker_colour: The hex-colour of the marker.
        :return: None
        """
        self._ax.plot(CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2, 'x', color=marker_colour, markersize=6, markeredgewidth=3, label='Origin')

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

    def add_cylinders(self, cylinders: List[Cylinder]) -> None:
        """
        Groups a cylinder with a custom circle.
        :param List[Cylinder] cylinders: The cylinders to group.
        :return: None
        """
        for cylinder in cylinders:
            self._artists[cylinder] = CustomCircle((0, 0), cylinder.radius, cylinder.weight,
                                                   fill=False, edgecolor="#99D9DD", linewidth=2)

    def position_cylinders(self) -> None:
        """
        Positions cylinders based on the save states.
        :return: None
        """
        ...

    @staticmethod
    def show() -> None:
        """
        Shows the figure containing all the artists.
        :return: None
        """
        plt.show()


class DynamicCanvas(Canvas):
    def __init__(self, fps: int, **subplot_kwargs):
        super().__init__(**subplot_kwargs)

        self.__fps = fps
        self.__frame = -1
        self.__save_index = 0

        self.__save_states = {}
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
        for cylinder in self._artists.keys():
            if not self.__save_states.get(cylinder, False):  # checks whether the cylinder in __save_states exists
                self.__save_states[cylinder] = [[cylinder.centre], []]  # if not, then add an entry for it.
                continue

            self.__save_states[cylinder][0].append(cylinder.centre)  # adds the new centre of the cylinder to its associated save
            self.__save_states[cylinder][1].append((  # appends the x and y increments the cylinder needs to make each frame to get to the new centre.
                (self.__save_states[cylinder][0][-1][0] - self.__save_states[cylinder][0][-2][0]) / self.__fps,
                (self.__save_states[cylinder][0][-1][1] - self.__save_states[cylinder][0][-2][1]) / self.__fps
            ))

        self.__saved_generations.append(generation)

    def update(self, frame: int) -> List[Artist]:
        """
        Updates the artist's positions based on the difference between the current position and the next whilst
        incorporating the amount of fps the animation will have.
        :return: None
        """
        if self.__frame == -1:
            self.__save_index += 1
            self.__frame += 1
            return

        # for cylinder, cylinder_patch in self._artists.items():
        #     cylinder_patch.add_to(self._ax)

        self.__frame += 1
        if self.__frame == 60:
            self.__frame = -1



    def show(self) -> None:
        """
        An override of the child method.
        :return: None
        """
        frames = (len(self.__saved_generations) - 1) * self.__fps
        # self.update(frames)
        # anim = animation.FuncAnimation(fig=self._fig, func=self.update, frames=frames, interval=self.__fps, repeat=False)
        plt.show()



if __name__ == "__main__":
    d = DynamicCanvas(60, figsize=(10, 10))

    d.draw_acceptance_range()
    d.mark_centre()
    d.setup_axis()

    plt.show()