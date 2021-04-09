from pycolate.grid_engine import grid
import numpy as np


class MeanFieldSandpile:
    def __init__(
        self,
        initconfig,
        theshold,
        dissipation_amount,
        graphics=True,
        rulebook=None,
    ):

        self._theshold = theshold
        self._dissipation_amount = dissipation_amount
        self._rulebook = {}
        self.__dedug_messages = True
        self.avalanche_sizes = []

        if any([i > theshold for i in initconfig]):
            raise Exception("The initial configuration is not stable.")

        else:
            self._config = initconfig
            self.__to_tople = False

        self.__want_graphics = graphics

        if self.__want_graphics:

            if rulebook == None:

                for height in range(0, theshold):
                    self._rulebook[height] = "white"
                self._rulebook[theshold - 1] = "yellow"
                self._rulebook[theshold] = "orange"
                self._rulebook[theshold + 1] = "red"

            else:

                self._rulebook = rulebook

            self.graphics = grid(self._config, self._rulebook, 30)
            self._frame_list = []

        self.__debug("Inital config:")

    def _drive_pile(self, ignore_list=[], number_to_drive=1):

        rng = np.random.default_rng()
        site_to_drive = rng.integers(0, len(self._config) - 1)
        while site_to_drive in ignore_list:
            site_to_drive = rng.integers(0, len(self._config) - 1)
        self._config[site_to_drive] += 1
        self.__snapshot()

    def _relax_pile(self):

        to_topple = [i > self._theshold for i in self._config]
        if any(to_topple):
            site_to_topple = np.where(to_topple)[0][0]
            self._config[site_to_topple] -= self._dissipation_amount
            self._drive_pile(ignore_list=[site_to_topple])
            self.__to_tople = True
        else:
            self.__to_tople = False

    def cycle(self, drives):

        self.__snapshot()

        for _ in range(drives):

            current_avalanche_size = 0
            self._drive_pile()
            self._relax_pile()
            while self.__to_tople:
                current_avalanche_size += 1
                self._relax_pile()
            self.avalanche_sizes.append(current_avalanche_size)

    def make_gif(self, path, file_name):

        self._frame_list[0].save(
            f"{path}/{file_name}.gif",
            format="GIF",
            append_images=self._frame_list[1:],
            save_all=True,
            duration=1000,
            loop=0,
        )

    def make_frames(self, path):

        x = 0

        for image in self._frame_list:

            image.save(f"{path}/{x}.png")

            x += 1

    def __snapshot(self):

        if self.__want_graphics:

            self.graphics.draw_config(self._config)

            self._frame_list.append(self.graphics.image.copy())

    def __debug(self, debug_message):
        if self.__dedug_messages:
            print(f"{debug_message}: {self._config}")


if __name__ == "__main__":

    m = MeanFieldSandpile([0, 0, 0, 0], 1, 1)
    m.cycle(3)
    m.make_frames(
        "/Users/mac/Library/Mobile Documents/com~apple~CloudDocs/Projects/pycolate/pycolate/pycolate/image_test"
    )
