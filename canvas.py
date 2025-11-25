from matplotlib.patches import Rectangle
from matplotlib import animation
from config import CONTAINER_WIDTH, CONTAINER_HEIGHT
import matplotlib.pyplot as plt
from cylinders import Cylinder
from custom_patches.circle import CustomCircle
from typing import List


class Canvas:
    def __init__(self, **subplot_kwargs):
        self._fig, self._ax = plt.subplots(**subplot_kwargs)

        self._artists: List[CustomCircle] = []

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

    def add_cylinder(self, cylinders: List[Cylinder]):
        ...
        # self._artists.append(CustomCircle(cylinder.centre, cylinder.radius, cylinder.weight))
        # As the centre of a cylinder is the only thing that is guaranteed to change, the callback will only occur when a cylinder moves.
        # self._artists[-1].add_callback()

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
        self.__save_states = {}

    def save_state(self) -> None:
        """
        Saves the current position of each artist.
        :return: None
        """
        for artist in self._artists:
            if self.__save_states.get(artist, False):
                self.__save_states[artist].append(artist.xy)
                continue

            self.__save_states[artist] = [artist.xy]

    def update(self, frame: int) -> None:
        """
        Updates the artist's positions based on the difference between the current position and the next whilst
        incorporating the amount of fps the animation will have.
        :param int frame: The current frame being shown.
        :return: None
        """
        ...

    def show(self) -> None:
        """
        An override of the child method.
        :return: None
        """
        animation.FuncAnimation(fig=self._fig, func=self.update, fps=self.__fps, interval=30)
        plt.show()



if __name__ == "__main__":
    d = DynamicCanvas(60, figsize=(10, 10))

    d.draw_acceptance_range()
    d.mark_centre()
    d.setup_axis()

    plt.show()