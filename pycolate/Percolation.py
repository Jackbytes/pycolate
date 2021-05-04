# python3 setup.py bdist_wheel
# twine upload dist/*
import numpy as np
from pycolate.grid_engine import grid
from colorsys import hsv_to_rgb
from scipy.ndimage import measurements
import scipy.ndimage as ndimage
from random import shuffle
import PIL

CRIT_PROB = 0.59274621


class Percolation:
    def __init__(self, width: int, height: int, occupationProb: float):

        """The essential properties are defined and set, and the percolation configuration is created."""

        self.height = height  # The height of the configuration.

        self.width = width  # The width of the configuration.

        self._site_size = (
            10  # The width and height of each site in the illustration in pixels.
        )

        self.percolated = (
            False  # Has the configuration percolated? We dont know yet, so false.
        )

        self.clusters = (
            []
        )  # This list will eventually contain the clusters. Each cluster is a list of sites in this list.

        self.found_clusters = (
            False  # Has the cluster finding algorithm been run? So far false.
        )

        self.generated_graphics = False  # Has any kind of illustration generating function been run? So far false.

        prob = occupationProb  # This just makes the next line more compact.

        rng = np.random.default_rng() #Numpys RNG.

        self.config = rng.choice(
            [0, 1], p=[1 - prob, prob], size=(width, height)
        )  # A numpy array, 1=occupied, 0=unoccupied.

    def cluster_find(self):

        """Finds the clusters in the configuration."""

        self.percolated_size = 0  # The size of the percolated cluster, we'll assume zero until it is found.

        labeledConfig, num = measurements.label(
            self.config
        )  # The labeled configuration, each number corresponds to a unique cluster. Num is the number of labels.

        sizes = ndimage.sum(
            self.config, labeledConfig, range(num + 1)
        )  # The sizes of the clusters.

        sizes = sizes[sizes != 0]  # Removes any zeros, just in case.

        labels = np.unique(
            labeledConfig
        )  # Returns a list of the labels. Used for indexing the labels.

        labelsToCheck = labels[
            labels != 0
        ]  # We dont care about the unoccupied sites, labelled 0.

        # If a cluster is on two opposing edges then it is percolating.
        # The next 4 lines just slice these out so we can easily find the percolating cluster,

        leftColumn = labeledConfig[
            :, 0
        ]  # The left most column, used for checking for the percolating cluster.

        rightColumn = labeledConfig[
            :, -1
        ]  # The right most column, again used for checking for the percolating cluster.

        topRow = labeledConfig[
            0
        ]  # Top most column, same reasoning as the other columns

        bottomRow = labeledConfig[
            -1
        ]  # Bottom most column, same reasoning as the above.

        for label in labelsToCheck:  # Iterate though all labels.

            left = label in leftColumn  # Is it touching the left edge?

            right = label in rightColumn  # Is it touching the right edge?

            bottom = label in bottomRow  # Is it touching the bottom edge?

            top = label in topRow  # Is it touching the top edge?

            if (left and right) or (
                bottom and top
            ):  # Is it touching two opposing edges? If so then it is percolating!!

                self.percolLabel = label  # The label of this special cluster.

                self.percolated = True  # We can know set this to true since the percolating cluster has been found.

                break  # Exit this loop, since we have found the percolating cluster.

        if (
            self.percolated
        ):  # If the percolated cluster has been found we need some unique logic.

            self.percolated_size = len(
                labeledConfig[labeledConfig == self.percolLabel]
            )  # Size of percolated cluster.

            self.sizes = sizes[
                sizes != self.percolated_size
            ]  # We isolate the other cluster sizes into a different list.

            self.mean_cluster_size = np.mean(
                self.sizes
            )  # The mean of the cluster sizes excluding the percolated cluster size.

        if not self.percolated:  # If the percolated cluster was not found.

            self.mean_cluster_size = np.mean(
                sizes
            )  # We can just take the mean size of all sizes, since there is no percolated cluster size to exclude.

        self.labeledConfig = labeledConfig  # The numpy array where each cluster has a unique number to label it.

        self.found_clusters = True  # The cluster finding algorithm has been run.

    def pretty_clusters(self):

        """Generates a pretty illstration where each cluster has a unique, distinct colour."""

        labelsToCheck = np.unique(self.labeledConfig)  # Creates a list of labels.

        for label in labelsToCheck:  # Iterate though possible labels.

            if (
                label != 0
            ):  # Just a double check, we dont care about the unoccupied sites.

                coordsOfPoints = np.transpose(
                    np.where(self.labeledConfig == label)
                )  # creates a list of the cluster points.

                self.clusters.append(coordsOfPoints)  # Adds this to the cluster list.

        tmp = np.unique(self.labeledConfig)  # Copy of the unique labels.

        labelsToDraw = np.delete(tmp, np.where(tmp == 0))

        clusterNum = len(self.clusters)  # Number of clusters

        hues = np.linspace(
            1, 350, num=clusterNum + 1
        )  # Generates clusterNum (a integer) unique colors

        shuffle(hues)  # Randomises the hues.

        rulebook = {}  # Initalises dictionary used for colouring.

        j = 1  # Inital value for 'for loop'.

        for i in labelsToDraw:  # Iterates through labels to draw.

            rulebook[i] = "hsv({},{}%,{}%)".format(
                hues[j], np.random.uniform(20, 60), np.random.uniform(50, 100)
            )  # A 'rulebook' is a dictionary for the grid package, it is structured as {label:'color'}

            j += 1

        rulebook[
            0
        ] = "white"  # Just a double check that 0 (unoccupied) is definitely white.

        self.graphics = grid(
            self.labeledConfig, rulebook, self.site_size
        )  # The grid object that will be the graphics for this percolation.

        self.generated_graphics = True  # We have generated the self.graphics property.

    def simple_clusters(self, color="hotpink"):

        """Generates a basic illustration where occupied sites are 'color' and unoccupied sites are white."""

        rulebook = {0: "white", 1: color}  # 0 is unoccupied, 1 is occupied.

        self.graphics = grid(
            self.config, rulebook, self.site_size
        )  # Creates a grid object. Just has two colours.

        self.generated_graphics = True  # We have generated the self.graphics property.

    def only_percolating_cluster(self, color="hotpink"):

        """Generates an illustration where only the percolated cluster is drawn.

        Raises
        ------
        Exception
            Raised if no percolating cluster exists.
        """

        if not self.percolated:

            raise Exception("The configuration must have a percolated cluster to draw.")

        percolating_cluster_config = np.where(
            self.labeledConfig == self.percolLabel, self.labeledConfig, 0
        )  # Removes everything but the percolated cluster from the labeled configuration.

        rulebook = {
            0: "white",
            self.percolLabel: color,
        }  # Unoccupied and other clusters are white, percolated cluster is 'color'.

        self.graphics = grid(
            percolating_cluster_config, rulebook, self.site_size
        )  # An object from the grid package, uses the numpy array and the above to color it.

        self.generated_graphics = True  # We have generated the self.graphics property.

    def display(self):

        """Displays the generated illustration.

        Raises
        ------
        Exception
            A exception is raised if the clusters have not been found or no graphics have been generated.
        """

        if not self.found_clusters or not self.generated_graphics:

            raise Exception(
                "Run cluster_find and generate graphics before attempting to display."
            )

        self.graphics.display()  # Displays the grid object

    def save(self, path):

        """Saves the generated illustration to path.

        Raises
        ------
        Exception
            A exception is raised if the clusters have not been found or no graphics have been generated.
        """

        if not self.found_clusters or not self.generated_graphics:

            raise Exception(
                "Run cluster_find and generate_graphics before attempting to save."
            )

        self.graphics.image.save("{}".format(path))

    @property
    def site_size(self):
        return self._site_size

    @site_size.setter
    def site_size(self, new_size):
        """Sets the site_size, checks it is a positive integer greater then 1. The site size is the linear length of the squares used
        in the grid illustration.

        Parameters
        ----------
        new_size : int
            The new site size.

        Raises
        ------
        TypeError
            Raised if the given values is not an integer.
        ValueError
            Raised if the given value is smaller then 1.
        """

        if type(new_size) != int:
            raise TypeError("The site_site must be a postive integer.")
        if not new_size >= 1:
            raise ValueError("The site_site must be a positive integer.")
        self._site_size = new_size


class PercolationExperiment:
    def __init__(self, *args):

        self.data = {}

        self.collect_mean = self.collect_perc_size = self.collect_sizes = False

        if "mean cluster size" in args:

            self.collect_mean = True

            self.data["mean cluster sizes"] = []

        if "percolated cluster size" in args:

            self.collect_perc_size = True

            self.data["percolated cluster sizes"] = []

        if "cluster sizes" in args:

            self.collect_sizes = True

            self.data["cluster sizes"] = []

    def run(self, sample_size: int, width: int, height: int, occupation_prob: float):

        for i in range(sample_size):

            temp_perc = Percolation(
                width=width, height=height, occupationProb=occupation_prob
            )

            temp_perc.cluster_find()

            if self.collect_perc_size:
                self.data["percolated cluster sizes"].append(temp_perc.percolated_size)
            if self.collect_mean:
                self.data["mean cluster sizes"].append(temp_perc.mean_cluster_size)
            if self.collect_sizes:
                self.data["cluster sizes"] += temp_perc.sizes.tolist()

            del temp_perc


if __name__ == "__main__":

    from math import log
    import scipy.stats
    lower = 500
    higher = 1000
    lengths = range(lower,higher)
    percolating_cluster_sizes = []
    current = 1
    for length in lengths:
        for _ in range(0,10):
            successful = False
            sample = []
            while not successful:
                p = Percolation(length,length,CRIT_PROB)
                p.cluster_find()
                if p.percolated:
                    sample.append(p.percolated_size)
                    successful = True
        print(current/(higher - lower))
        percolating_cluster_sizes.append(np.mean(sample))
        current += 1
        
    x = [log(i) for i in lengths]
    y = [log(i) for i in percolating_cluster_sizes]
    import matplotlib.pyplot as plt 
    plt.loglog(x,y,'.')
    plt.show()