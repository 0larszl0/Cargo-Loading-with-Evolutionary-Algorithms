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
            Circle(xy, radius, edgecolor=kwargs["edgecolor"])  # centre marker
        ]

    @property
    def xy(self) -> Tuple[float, float]:
        return self.__xy

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

    def show_annotations(self, ax: Axes) -> None:
        """
        Display the annotations onto an axis.
        :param plt.Axes ax: The axes to the display the annotations onto.
        :return: None
        """
        for annotation in self.__annotations:
            ax.add_patch(annotation)

        ax.add_patch(self)