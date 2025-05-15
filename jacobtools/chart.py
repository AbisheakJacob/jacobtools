import matplotlib.pyplot as plt
import seaborn as sns

def set_global_style():
    sns.set_theme(style='whitegrid')  # You can choose 'white', 'darkgrid', etc.
    plt.rcParams.update({
        'figure.figsize': (10, 6),
        'axes.titlesize': 16,
        'axes.labelsize': 14,
        'axes.edgecolor': '#333333',
        'axes.linewidth': 1.2,
        'axes.grid': True,
        'grid.color': '#dddddd',
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': '#444444',
        'font.family': 'sans-serif',
        'font.sans-serif': 'DejaVu Sans'
    })

    sns.set_palette("Set2")  # or use custom_palette = sns.color_palette([...])



def plot_line(data, x, y, hue=None, title='', xlabel='', ylabel=''):
    set_global_style()
    plt.figure()
    ax = sns.lineplot(data=data, x=x, y=y, hue=hue)
    ax.set_title(title)
    ax.set_xlabel(xlabel if xlabel else x)
    ax.set_ylabel(ylabel if ylabel else y)
    plt.tight_layout()
    plt.show()


def plot_bar(data, x, y, hue=None, title='', xlabel='', ylabel='', orient='v'):
    set_global_style()
    plt.figure()
    ax = sns.barplot(data=data, x=x, y=y, hue=hue, orient=orient)
    ax.set_title(title)
    ax.set_xlabel(xlabel if xlabel else x)
    ax.set_ylabel(ylabel if ylabel else y)
    plt.tight_layout()
    plt.show()


def plot_heatmap(data, title='', xlabel='', ylabel='', annot=True, fmt=".2f", cmap='coolwarm'):
    set_global_style()
    plt.figure()
    ax = sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap, cbar=True)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()
    plt.show()

def save_plot(filename, dpi=300):
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', transparent=False)
