from custom_patches.circle import CustomCircle
from matplotlib.backend_bases import KeyEvent
from matplotlib.legend import Legend
from config import MANUAL_FLICK
import matplotlib.pyplot as plt
import matplotlib as mpl
from typing import List


class EventManager:
    """
        Handles KeyEvents that happen within a figure.
        Any objects collected are strictly used for a given key event, i.e. legends are collected, so on 'l' press, the
        visibility of all legends can be toggled.
    """

    def __init__(self, fig: plt.Figure):
        self.__key_press_id = fig.canvas.mpl_connect("key_press_event", self.__on_key_event)

        self.__cylinder_patches: List[CustomCircle] = []
        self.__legends: List[Legend] = []
        self.__anim_containers = []  # List[AnimatedContainer]

        self.__fpp: int | None = None  # This must be set externally using set_fpp

        # Remove default scaling
        # This is because if you select an axes, and press a key like 'l', the default keymap to scale the axes occurs.
        mpl.rcParams["keymap.xscale"] = []
        mpl.rcParams["keymap.yscale"] = []

    def set_fpp(self, fpp: int) -> None:
        self.__fpp = fpp

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

    def add_anim_containers(self, anim_container) -> None:
        """
        Appends a AnimatedContainer objects to a total list of Animated Objects.
        :param AnimatedContainer anim_container: An animated container holding generational information.
        :return: None
        """
        self.__anim_containers.append(anim_container)

    def flick_positions(self, direction: int = 1) -> None:
        """
        Each patch within each container has their positions manually updated based on the direction of the input.
        :param int direction: 1, for progressing through generations, -1 for regressing through generations.
        :return: None
        """
        # Determines if the global fpp has been set via set_fpp.
        if self.__fpp is None:
            raise Exception(f"\r\033[1m\033[31mCustom Exception: Ensure the Frames-Per-Patch variable has been assigned using set_fpp\033[0m")

        # - Update patch positions - #
        # Repeats n times, specified by self.__fpp, and updates each group of patches within each animated container.
        for i in range(self.__fpp):
            for anim_container in self.__anim_containers:
                # Show the TRANSITION title, when beginning the transition
                if (i == 0) and (direction == 1) and (self.__fpp != 1):  # self.__fpp != 1, ensures there's no quick shimmer of the message when not sliding across positions
                    anim_container.choose_title(anim_container.TRANSITION_TITLE)

                elif (i == 0) and (direction == -1) and (self.__fpp != 1):
                    anim_container.choose_title(anim_container.TRANSITION_TITLE_R)

                anim_container.update_patch_positions(direction)
                anim_container.update_com_marker()
                plt.pause(0.001)  # Runs the GUI event loop to update figure and to pause for n seconds.

                if (i == self.__fpp - 1) and direction == -1:  # Show the BEST title, when completing the transition
                    anim_container.choose_title(anim_container.BEST_TITLE)

        return None

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

            # - Arrow keys - #
            case "right":
                # Determines whether the user can flick between generations
                if not MANUAL_FLICK:
                    return None

                # Checks whether the visualisation is on the last key-generation or not.
                elif self.__anim_containers and (self.__anim_containers[0].save_index == len(self.__anim_containers[0].saved_generations) - 1):
                    return None  # if the user is on the last key generation restrict them the ability to go to a higher index that doesn't exist.

                # update positions
                self.flick_positions()

                # increment save index for each container
                for anim_container in self.__anim_containers:
                    anim_container.save_index += 1
                    anim_container.choose_title(anim_container.BEST_TITLE)

            case "left":
                if not MANUAL_FLICK:
                    return None

                # Checks whether the visualisation is on the first key-generation or not.
                elif self.__anim_containers and (self.__anim_containers[0].save_index == 0):
                    return None  # if the user is on the first key generation, the restrict them to go into a negative index.

                # decrement save index for each container
                for anim_container in self.__anim_containers:
                    anim_container.save_index -= 1

                # update positions
                self.flick_positions(-1)

        plt.ioff()

        return None

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
