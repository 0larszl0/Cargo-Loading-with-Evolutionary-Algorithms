from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, ArrowStyle
from matplotlib.text import Text
from config import CONTAINER_WIDTH, CONTAINER_HEIGHT
import matplotlib.pyplot as plt
from typing import Tuple


class CylinderPatch(Circle):
    def __init__(self, xy: Tuple[float, float], radius: float, weight: int,
                 text_colour: str = "#F7F8F9", arrow_colour: str = "#AFD8DB", **kwargs):
        super().__init__(xy, radius, **kwargs)

        arrow_style = ArrowStyle.CurveAB(head_length=radius * 4, head_width=radius * 1.6)

        self.__annotations = [
            FancyArrowPatch(  # <-> arrow annotation
            (xy[0] - radius, xy[1]), (xy[0] + radius, xy[1]),
                arrowstyle=arrow_style, color=arrow_colour, alpha=.4
            ),
            Text(  # diameter text
                xy[0], xy[1] - (radius * .35), f"{radius * 2}Ø",
                ha="center", va="center", color=text_colour, fontsize=8 * radius
            ),
            Text(  # weight text
                xy[0], xy[1] + (radius * .35), f"{weight}kg",
                ha="center", va="center", color=text_colour, fontsize=8 * radius
            ),
            Circle(xy, radius, edgecolor=kwargs["edgecolor"])  # centre marker
        ]

    def clear(self) -> None:
        """
        Clears this patch and all its annotations from the figure its attached to.
        :return: None
        """
        for annotation in self.__annotations:
            annotation.remove()

        self.remove()

    def update_annotations(self) -> None:
        """
        Updates the positions of all the annotations based on the new circle's centre.
        :return: None
        """
        ...

    def show_annotations(self, ax: plt.Axes) -> None:
        """
        Display the annotations onto an axis.
        :param plt.Axes ax: The axes to the display the annotations onto.
        :return: None
        """
        ...


class Canvas:
    def __init__(self, fig: plt.Figure, ax: plt.Axes):
        self.__fig = fig
        self.__ax = ax

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

        self.__ax.add_patch(wbc)

    def mark_centre(self, marker_colour: str = "#F4BA02") -> None:
        """
        Add a marker indicating the centre of the figure/container.
        :param str marker_colour: The hex-colour of the marker.
        :return: None
        """
        self.__ax.plot(CONTAINER_WIDTH / 2, CONTAINER_HEIGHT / 2, 'x', color=marker_colour, markersize=6, markeredgewidth=3, label='Origin')

    def set_title(self, title: str, colour: str = "#F7F8F9") -> None:
        """
        Sets a title to the figure.
        :param str title: The title to set.
        :param str colour: The colour of the title.
        :return: None
        """
        self.__ax.set_title(title, color=colour, fontsize=14, pad=20, weight="bold")

    def setup_axis(self, spine_colour: str = "#F7F8F9", tick_colour: str = "#F7F8F9", grid_colour: str = "#F7F8F9",
                   face_colour: str = "#01364C", legend_colour: str = "#F7F8F9", figure_face_colour: str = "#01364C") -> None:
        """
        Set aspect ratios, x & y limits, a title, colours and a legend.
        :return: None
        """
        # - Set up axis - #
        self.__ax.set_aspect("equal")
        self.__ax.set_xlim(0, CONTAINER_WIDTH)
        self.__ax.set_ylim(0, CONTAINER_HEIGHT)

        self.__ax.grid(True, alpha=.15, color=grid_colour)
        self.__ax.spines[:].set_color(spine_colour)
        self.__ax.tick_params(colors=tick_colour)
        self.__ax.set_facecolor(face_colour)

        self.__ax.legend(loc='upper right', facecolor=face_colour, edgecolor=legend_colour, labelcolor=tick_colour, framealpha=0.9)

        self.__fig.patch.set_facecolor(figure_face_colour)


class DynamicCanvas(Canvas):
    def __init__(self, fig: plt.Figure, ax: plt.Axes, transition_speed: float):
        super().__init__(fig, ax)
        self.__transition_speed = transition_speed



    # def add_


if __name__ == "__main__":
    figg, axx = plt.subplots(figsize=(10, 10))
    d = DynamicCanvas(figg, axx, 1.)

    d.draw_acceptance_range()
    d.mark_centre()
    d.setup_axis()

    plt.show()