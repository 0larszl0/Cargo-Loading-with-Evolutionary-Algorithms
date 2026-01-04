from matplotlib.patches import Circle, FancyArrowPatch, ArrowStyle
from matplotlib.pyplot import Axes
from matplotlib.text import Text
from typing import Tuple

import matplotlib as mpl


class CustomCircle(Circle):
    def __init__(self, xy: Tuple[float, float], radius: float, weight: float,
                 text_colour: str = "#F7F8F9", arrow_colour: str = "#AFD8DB", **kwargs):
        super().__init__(xy, radius, **kwargs)

        self.__weight = weight

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
            Circle(xy, radius * 0.05, edgecolor=kwargs["edgecolor"], facecolor=kwargs["edgecolor"])  # centre marker
        ]

    def __str__(self):
        return f"CustomCircle (\033[4m{self.__repr__().split('at ')[1][:-1]}\033[0m)"

    def __set_annotations(self, xy: Tuple[float, float]) -> None:
        """
        Sets the positions of the annotations within this circle
        :param Tuple[float, float] xy: The new position
        :return: None
        """
        for annotation in self.__annotations:
            match type(annotation):
                case mpl.patches.FancyArrowPatch:
                    annotation.set_positions((xy[0] - self.radius, xy[1]), (xy[0] + self.radius, xy[1]))

                case mpl.text.Text:
                    label = annotation.get_text()
                    if label.endswith('Ø'):
                        annotation.set_position((xy[0], xy[1] - (self.radius * .35)))

                    elif label.endswith("kg"):
                        annotation.set_position((xy[0], xy[1] + (self.radius * .35)))

                case mpl.patches.Circle:
                    annotation.center = xy

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def centre(self) -> Tuple[float, float]:
        """
        Using this for continuity with British spelling and so some utils can interpret the property the same way.
        :return: Tuple[float, float]
        """
        return self.center  # ignore warning, it does in fact return Tuple[float, float]

    def set_position(self, xy: Tuple[float, float]) -> None:
        """
        Modifies the position of this circle and its annotations.
        :return: None
        """
        self.__set_annotations(xy)
        self.center = xy

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

    def toggle_annotations(self) -> None:
        """
        Toggle the visibility of each annotation this Circle has.
        :return: None
        """
        for annotation in self.__annotations:
            annotation.set_visible(not annotation.get_visible())

