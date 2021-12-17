import matplotlib.pyplot
import matplotlib.image
import os

# original source
# https://stackoverflow.com/questions/52331622/plotnine-any-work-around-to-have-two-plots-in-the-same-figure-and-print-it

def _check_plotnine_grid(plots_list, figsize):
    if not type(plots_list) == list:
        raise ValueError('Input plots_list is not a list')
    if (not type(figsize) == tuple) or (not len(figsize) == 2):
        raise ValueError('Input figsize should be a tuple of length 2')

def plotnine_grid(plots_list, row=None, col=1, height=None, width=None, dpi=500, ratio=None, pixels=10000,
                    figsize=(12, 8), file=None):

    """
    Create a grid of plotnine plots.

    Function input
    ----------
    plots_list      : a list of plotnine.ggplots
    row, col        : numerics to indicate in how many rows and columns the plots should be ordered in the grid
                defaults: row -> length of plots_list; col -> 1
    height, width   : the height and width of the individual subplots created by plotnine
                    can be automatically determined by a combination of dpi, ratio and pixels
    dpi             : the density of pixels in the image. Default: 500. Higher numbers could lead to crisper output,
                    depending on exact situation
    ratio           : the ratio of heigth to width in the output. Standard value is 1.5 x col/row.
                    Not used if height & width are given.
    pixels          : the total number of pixels used, default 10000. Not used if height & width are given.
    figsize         : tuple containing the size of the final output after making a grid, in pixels (default: (1200,800))

    Function output
    ----------
    A matplotlib figure that can be directly saved with output.savefig().
    """

    _check_plotnine_grid(plots_list, figsize)  # Check the input

    # Assign values that have not been provided based on others. In the end, height and width should be provided.
    if row is None:
        row = len(plots_list)

    if ratio is None:
        ratio = 1.5 * col / row

    if height is None and width is not None:
        height = ratio * width

    if height is not None and width is None:
        width = height / ratio

    if height is None and width is None:
        area = pixels / dpi
        width = np.sqrt(area/ratio)
        height = ratio * width

    # Do actual subplot creation and plot output.
    i = 1
    fig = matplotlib.pyplot.figure(figsize=figsize)
    matplotlib.pyplot.autoscale(tight=True)

    for image_sel in plots_list:  # image_sel = plots_list[i]
        image_sel.save('image' + str(i) + '.png', height=height, width=width, dpi=500, verbose=False)
        fig.add_subplot(row, col, i)
        matplotlib.pyplot.imshow(matplotlib.image.imread('image' + str(i) + '.png'), aspect='auto')
        fig.tight_layout()
        # fig.get_axes()[i-1].axis('off')
        # display(fig.get_axes())
        fig.get_axes()[i-1].set_axis_off()
        fig.get_axes()[i].set_axis_off()
        i = i + 1
        os.unlink('image' + str(i - 1) + '.png')  # os.unlink is basically os.remove but in some cases quicker
        fig.patch.set_visible(False)

        file = file.replace(' ', '_')
        fig.savefig('imgs/{}.png'.format(file))

    matplotlib.pyplot.close()
    # return fig
