from matplotlib.patches import Circle, FancyArrowPatch, ArrowStyle
from matplotlib.pyplot import Axes
from matplotlib.text import Text
from typing import Tuple


class CustomCircle(Circle):
    def __init__(self, xy: Tuple[float, float], radius: float, weight: int,
                 text_colour: str = "#F7F8F9", arrow_colour: str = "#AFD8DB", **kwargs):
        super().__init__(xy, radius, **kwargs)

        self.__xy = xy
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
            Circle(xy, radius * 0.05, edgecolor=kwargs["edgecolor"])  # centre marker
        ]

    @property
    def xy(self) -> Tuple[float, float]:
        return self.__xy

    def add_to(self, ax: Axes) -> None:
        """
        Adds the circle and its annotations to the Axes.
        :param plt.Axes ax: The axes to display the annotations and circle onto.
        :return: None
        """
        for annotation in self.__annotations:
            if type(annotation) == Text:
                ax.add_artist(annotation)
                continue

            ax.add_patch(annotation)

        ax.add_patch(self)

    # def toggle_visibility(self) -> None:
    #     """
    #     Toggles the visibility of the circle and its annotations.
    #     :return: None
    #     """
    #     for annotation in self.__annotations:
    #         annotation.set_visible(not annotation.get_visible())
    #
    #     self.set_visible(not self.get_visible())

    def update_annotations(self) -> None:
        """
        Updates the positions of all the annotations based on the new circle's centre.
        :return: None
        """
        ...

