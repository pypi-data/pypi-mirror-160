from matplotlib import pyplot as plt


def legend_to_right_of_plot(ax=None, **overrides):
    ax = ax or plt.gca()

    kwargs = dict(frameon=False, loc="center left", bbox_to_anchor=(1, 0.5))
    kwargs.update(overrides)

    ax.legend(**kwargs)
