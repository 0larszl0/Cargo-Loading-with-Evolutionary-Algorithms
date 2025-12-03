from custom_patches.circle import CustomCircle
from matplotlib.backend_bases import KeyEvent
from matplotlib.legend import Legend
import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import List


class EventManager:
    """Just handles simple events that happen within a figure."""

    def __init__(self, fig: plt.Figure):
        self.__key_press_id = fig.canvas.mpl_connect("key_press_event", self.__on_key_event)

        self.__cylinder_patches: List[CustomCircle] = []
        self.__legends: List[Legend] = []

        # Remove default scaling
        # This is because if you select an axes, and press a key like 'l', the default keymap to scale the axes occurs.
        mpl.rcParams["keymap.xscale"] = []
        mpl.rcParams["keymap.yscale"] = []

    def add_patch(self, cylinder_patch: CustomCircle) -> None:
        """
        Appends a cylinder patch to the overall list of patches.
        :param CustomCircle cylinder_patch: A patch representing a cylinder.
        :return: None
        """
        self.__cylinder_patches.append(cylinder_patch)

    def add_legend(self, legend: Legend) -> None:
        """
        Appends a Legend to the overall list of Legends.
        :param Legend legend: A Legend within a plot.
        :return: None
        """
        self.__legends.append(legend)

    def __on_key_event(self, event: KeyEvent) -> None:
        """
        Handles key events.
        :param KeyEvent event: The key that was pressed.
        :return: None
        """
        plt.ion()  # temporarily enable interactive mode for the key event to show.

        match event.key:
            case 'a':
                self.toggle_circle_annots()

            case 'l':
                self.toggle_legends()

        plt.ioff()

    def toggle_circle_annots(self) -> None:
        """
        Toggles the visibility of every circle's annotations.
        :return: None
        """
        for cylinder in self.__cylinder_patches:
            cylinder.toggle_annotations()

    def toggle_legends(self) -> None:
        """
        Toggles the visibility of each legend in the figure.
        :return: None
        """
        for legend in self.__legends:
            legend.set_visible(not legend.get_visible())
