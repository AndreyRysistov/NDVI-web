from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np


def plot_ndvi(ndvi):
    fig, ax = plt.subplots(figsize=(12, 12))
    ndvi_class_bins = [-np.inf, 0, 0.15, 0.3, 0.5, np.inf]
    ndvi_class = np.digitize(ndvi, ndvi_class_bins)
    color_names = ["gray", "y", "yellowgreen", "g", "darkgreen"]
    color_cmap = ListedColormap(color_names)
    ndvi_cat_names = ["Объекты неживой природы", "Пустые районы",
                      "Слабая вегетенация", "Умеренная вегетенация", "Высокая вегетенация"
                      ]
    legend_dict = dict(zip(ndvi_cat_names, color_names))
    patch_list = []
    for key in legend_dict:
        data_key = mpatches.Patch(color=legend_dict[key], label=key)
        patch_list.append(data_key)
    ax.imshow(ndvi_class, cmap=color_cmap)
    ax.set_title("NDVI classes", fontsize=14)
    ax.set_axis_off()
    ax.legend(handles=patch_list)
    return fig