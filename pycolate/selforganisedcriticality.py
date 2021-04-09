from pycolate.grid_engine import grid
import numpy as np


class MeanFieldSandpile:
    def __init__(self, initconfig, theshold, dissipation_amount, graphics=True):

        self._theshold = theshold
        self._dissipation_amount = dissipation_amount
        self._rulebook = {}
        self.__dedug_messages = False
        self.avalanche_sizes = []

        if any([i > theshold for i in initconfig]):
            raise Exception("The initial configuration is not stable.")

        else:
            self._config = initconfig
            self.__to_tople = False

        self.__want_graphics = graphics

        if self.__want_graphics:

            for height in range(0, theshold):
                self._rulebook[height] = "white"
                self._rulebook[theshold] = "yellow"
                self._rulebook[theshold + 1] = "red"

            self.graphics = grid(self._config, self._rulebook, 10)
            self._frame_list = []

        self.__debug("Inital config:")

    def _drive_pile(self):

        rng = np.random.default_rng()
        site_to_drive = rng.integers(0, len(self._config))
        self._config[site_to_drive] += 1

    def _relax_pile(self):

        to_topple = [i > self._theshold for i in self._config]
        if any(to_topple):
            point_to_topple = np.where(to_topple)[0][0]
            self._config[point_to_topple] -= self._theshold
            self._drive_pile()
            self.__debug("Toppled:")
            self.__to_tople = True
        else:
            self.__debug("No Topple:")
            self.__to_tople = False

    def cycle(self, drives):

        for _ in range(drives):

            self.__debug("DRIVEN:")
            current_avalanche_size = 0
            self._drive_pile()
            self.__snapshot()
            self._relax_pile()
            while self.__to_tople:
                self.__snapshot()
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

        for image in self.image_list:

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

    m = MeanFieldSandpile([2, 2, 2, 1], 2, 1)
    m.cycle(5)
    m.make_gif(
        "/Users/mac/Library/Mobile Documents/com~apple~CloudDocs/Projects/pycolate/pycolate/pycolate/image_test",
        "test",
    )
