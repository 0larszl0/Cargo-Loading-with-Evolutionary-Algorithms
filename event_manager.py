from custom_patches.circle import CustomCircle
from matplotlib.backend_bases import KeyEvent
import matplotlib.pyplot as plt
from typing import List


class EventManager:
    """Just handles simple events that happen within a figure."""

    def __init__(self, fig: plt.Figure):
        self.__key_press_id = fig.canvas.mpl_connect("key_press_event", self.__on_key_event)

        self.__cylinder_patches: List[CustomCircle] = []

    @property
    def cylinder_patches(self) -> List[CustomCircle]:
        return self.__cylinder_patches

    @cylinder_patches.setter
    def cylinder_patches(self, new_patches: List[CustomCircle]) -> None:
        self.__cylinder_patches = new_patches

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
                ...

        plt.ioff()

    def toggle_circle_annots(self) -> None:
        """
        Toggles the visibility of every circle's annotations.
        :return: None
        """
        for cylinder in self.__cylinder_patches:
            cylinder.toggle_annotations()
