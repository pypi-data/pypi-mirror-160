from matplotlib import rcParams
from cycler import cycler
import seaborn as sns


def fis_dark_theme():    
    orange='#ef8354'
    mid_orange = '#FF9822'
    light_orange = '#FFE6C4'
    light_white = '#FFFEF1'
    dark_orange = '#EF6848'
    yellow_orange = '#FFB650'
    darked = '#303030'
    contrast_orange = '#10D0EE' #(bright blue)

    sns.set(rc={
        'axes.facecolor':'#303030', 
        'figure.facecolor':'#303030',
        'text.color':light_white,
        'axes.labelcolor':light_white,
        'xtick.color':light_white,
        'ytick.color':light_white,
    })




    dark_theme_colors = ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]
    dark_theme_colors + ["#fd7f6f", "#7eb0d5", "#b2e061", "#bd7ebe", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]
    dark_theme_colors + ["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"]
    dark_theme_colors + ["#e60049", "#0bb4ff", "#50e991", "#e6d800", "#9b19f5", "#ffa300", "#dc0ab4", "#b3d4ff", "#00bfa0"]
    rcParams['figure.figsize'] = 10,8
    rcParams['figure.facecolor'] = '#303030'
    rcParams['axes.facecolor'] = '#303030'
    rcParams['figure.facecolor'] = '#303030'
    rcParams['axes.edgecolor'] = light_white
    rcParams['text.color'] = light_white
    rcParams['axes.labelcolor'] = light_white
    rcParams['xtick.color'] = light_white
    rcParams['ytick.color'] = light_white
    rcParams['axes.grid'] = True
    rcParams['grid.color'] = light_white
    rcParams['grid.alpha'] = .1
    rcParams['axes.prop_cycle'] = cycler(color=dark_theme_colors)
    rcParams['image.cmap'] = 'Oranges'
    rcParams['boxplot.patchartist'] = True
    rcParams['boxplot.boxprops.color'] = orange
    rcParams['boxplot.whiskerprops.color'] = orange
    rcParams['boxplot.capprops.color'] = orange
    rcParams['boxplot.flierprops.color'] = orange
    rcParams['boxplot.flierprops.markeredgecolor'] = yellow_orange
