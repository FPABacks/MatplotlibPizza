import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.legend_handler import HandlerBase
from matplotlib.image import BboxImage
from matplotlib.transforms import TransformedBbox, Bbox


def getImage(path, zoom=0.05):
    return OffsetImage(plt.imread(path), zoom=zoom)


class ImgHandler(HandlerBase):
    """
    My attempt at a custom handler
    """
    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        # make the image bigger by increasing the scale:
        # The location or the images in the legend can become weird then though.
        scale = 1
        # Get data from the image
        img_data = orig_handle._data
        img_data = self.crop_img_data(img_data)
        # Get the shape to determine the aspect ratio of the image used
        ratio = img_data.shape[0] / img_data.shape[1]
        other_ratio = width / height
        w_scale = (ratio / other_ratio)

        # Create a new box to put the image in
        bb = Bbox.from_bounds(xdescent - (scale - 1) * (width * w_scale) / 2,
                              ydescent - scale * height / 2,
                              scale * width * w_scale,
                              scale * height)
        # Transform the box so it goes to the right place
        tbb = TransformedBbox(bb, trans)
        # Put the image in the box
        image = BboxImage(tbb)
        # Tell the image what it looks like
        image.set_data(img_data)
        # Tell the legend it has images now
        self.update_prop(image, orig_handle, legend)
        return [image]

    @staticmethod
    def crop_img_data(data):
        """Crops empty part of the image out"""
        rows_sel = np.sum(np.sum(data, axis=1), axis=1) > 0
        cols_sel = np.sum(np.sum(data, axis=0), axis=1) > 0
        data = data[rows_sel]
        data = data[:,cols_sel]
        nrows = np.sum(rows_sel)
        ncols = np.sum(cols_sel)
        if ncols > nrows:
            diff = ncols - nrows
            add = np.zeros((diff // 2, ncols, 4))
            data = np.concatenate((add, data, add), axis=0)
        elif nrows > ncols:
            diff = nrows - ncols
            add = np.zeros((nrows, diff // 2, 4))
            data = np.concatenate((add, data, add), axis=1)
        return data


class ImageScatter:
    """
    Makes a scatter plot with images rather than points. Because... I don't know...
    Works with matplotlib and has its own legend. Works best with square pngs with a transparent background.
    Empty space in the image may be cropped, and additional empty space might be added to make it square.
    Usage:

    # Initialize using the axes of the figure:
    fig, ax = plt.subplots()
    img_ax = ImageScatter(ax)
    img_ax.scatter(x, y, img_path, label="label")

    # Other plotting can still be done with the original axes
    ax.plot(x, y, ls="--", label="line")

    # To make a legend the img_ax.legend() needs to be used to include the images.
    img_ax.legend()
    """

    def __init__(self, ax):
        self.ax = ax
        self.items = ([], [])

    def scatter(self,
                x: (list, tuple, int, float, np.ndarray),
                y: (list, tuple, int, float, np.ndarray),
                img_loc: str,
                label: str = "",
                zoom: float=0.05,
                **kwargs):
        """
        Scatters the image located in img_loc to the indicated coordinates, x and y.
        input:
        x: scalar or array of x coordinates.
        y: scalar or array of y coordinates.
        img_loc: location of the image to be scattered. Anything matplotlib.pyplot.imread can handle.
        label: optional label for a legend, string.
        zoom: float, scaling of the image, default 0.05.
        """
        img = getImage(img_loc, zoom=zoom)

        # If adding only 1 point with floats (or ints)
        if isinstance(x, (int, float)):
            img_box = AnnotationBbox(img, (x, y), frameon=False)
            self.ax.add_artist(img_box)

        # If adding an array of points. Note each point is added separately (So don't use too many points! :))
        else:
            for i in range(len(x)):
                img_box = AnnotationBbox(img, (x[i], y[i]), frameon=False)
                self.ax.add_artist(img_box)

        self.items[0].append(img)
        self.items[1].append(label)

    def legend(self, img_only:bool=False, **kwargs):
        """
        Adds the legend, similar to normal legends, but a custom handler is required for the images.
        FIXME? This affects the order of the items in the legend, it is now always images first,
         could be nice if things could remain the same.

        Works with the normal matplotlib legend keyword arguments, but not regular arguments.
        Added keyword argument: img_only is a bool that skips all non image plotted elements in the legend.
        """
        # First, get the objects created outside of this class, if desired
        if img_only:
            handles, labels = [], []
        else:
            handles, labels = self.ax.get_legend_handles_labels()

        # Second, we have to make the handler map that tells matplotlib how to handle the different object types.
        # This only needs to be done for the images, the others will then get the default, which will work fine.
        handler_map = {}
        for img in self.items[0]:
            handler_map[img] = ImgHandler()

        return self.ax.legend(self.items[0] + handles, self.items[1] + labels,
                              handler_map=handler_map, handlelength=1, handleheight=2, **kwargs)


if __name__ == '__main__':
    # Test case to see if it works:

    # Image paths
    vink_path = "images/vink.png"
    robin_path = "images/robin.png"
    chickadee_path = "images/chickadee.png"

    # Generate some test data
    n = 12
    x = np.random.uniform(4.5, 6, size=n)
    y_vink = x * 0.5 - 9 + np.random.normal(size=n) / 10
    y_robin = x * 0.8 - 11 + np.random.normal(size=n) / 10
    y_chickadee = x * 0.7 - 10 + np.random.normal(size=n) / 10

    # Initialize the figure, axes, and the image scatter thing
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    img_ax = ImageScatter(ax)
    img_ax.scatter(x, y_vink, vink_path, label="Vink")
    img_ax.scatter(x, y_robin, robin_path, label="Robin")
    img_ax.scatter(x, y_chickadee, chickadee_path, label="Chickadee")

    x_lin = np.linspace(4.3, 6.1, 10)
    ax.plot(x_lin, x_lin * 0.5 - 9, c="red", label="Vink fit")
    ax.plot(x_lin, x_lin * 0.8 - 11, c="orange", label="Robin fit")
    ax.plot(x_lin, x_lin * 0.7 - 10, c="0.7", label="Chickadee fit")

    ax.set_xlim(4.3, 6.1)
    ax.set_ylim(np.min([y_robin, y_vink, y_chickadee]) - 0.1, np.max([y_robin, y_vink, y_chickadee]) + 0.1)
    ax.set_xlabel("Luminosity")
    ax.set_ylabel("Mass-loss rate")

    # Legend must be made with the ImageScatter's version, otherwise it does not work...
    # img_ax.legend()
    # Can also make two legends
    img_legend = img_ax.legend(img_only=True, loc="upper left")
    ax.legend(loc="lower right")
    ax.add_artist(img_legend)

    plt.tight_layout()

    plt.savefig("best_fig_test.pdf", dpi=600)
    plt.show()
