import os

import matplotlib.pyplot as plt
import scanpy as sc
import seaborn as sns
import numpy as np

# Global variables store dataset-specific information
from geospace.hotspot.geometry import similarity_map

library_id = None
img = None
scale = None
spot_size_preset = None
parameters_set = False
image_path = None


def set_dataset_plot_parameters(dataset):
    """
    Sets global variables that are used in spatial plots for non-Visium datasets
    :param dataset:
    :return:
    """
    global library_id, img, scale, spot_size_preset, parameters_set, image_path
    if dataset == "seqfish":
        img = None
        scale = None
        spot_size_preset = 0.045
    elif "merfish" in dataset:
        img = None
        scale = None
        spot_size_preset = 0.02
    elif "imc" in dataset:
        img = None
        scale = None
        spot_size_preset = 10
    elif "slideseq" in dataset:
        img = None
        scale = None
        spot_size_preset = 30
    else:
        pass

    # So that we can check that the globals are set correctly later
    parameters_set = True


def spatial(adata, spot_size=None, **kwargs):
    """
    Wraps scanpy's pl.spatial function, using parameters from set_dataset_plot_parameters,
    in order to make it a bit
    less annoying to manage parameters when analyzing non-Visium data
    :param adata: adata object to plot (spatial information in .obsm['spatial'])
    :param spot_size: size of spots used to show color parameter
    :param kwargs: Other keyword arguments to pass to sc.pl.spatial, such as color=, etc.
    :return:
    """

    if spot_size is None:
        spot_size = spot_size_preset

    sc.pl.spatial(adata, img=img, scale_factor=scale, spot_size=spot_size,
                  **kwargs)

    try:
        ax = kwargs['ax']
        ax.set_xlabel('')
        ax.set_ylabel('')
    except (KeyError, AttributeError):
        pass


def volcano(df, interaction=None, gene_list=None, ax=None, show=True, xlim=None, ylim=None,
            axis_labels=True, fc_cutoff=0, p_cutoff=2, fontsize=None, xoffset=0, yoffset=0.5,
            marker=None, title=None,
            **kwargs):
    if interaction is not None:
        # filter out the actual genes from the interaction
        ligand, receptor = interaction.split("_")
        ligand = ligand.capitalize()
        receptor = receptor.capitalize()
        df = df.drop(index=ligand).drop(index=receptor)
    x = df["log2(fc)"]
    y = df["-log10(p)"]

    # for coloring points based on significance
    hue = np.zeros(shape=x.shape)
    hue[np.logical_and(x > fc_cutoff, y > p_cutoff)] = 1
    hue[np.logical_and(x < -fc_cutoff, y > p_cutoff)] = 2
    palette = []
    if 0 in hue:
        palette.append(sns.color_palette("muted")[7])
        # palette.append("gray")
    if 1 in hue:
        palette.append(sns.color_palette("muted")[3])
        # palette.append("red")
    if 2 in hue:
        palette.append(sns.color_palette("muted")[0])
        # palette.append("blue")

    # For indicating a subset of genes using a different marker
    style = None
    if marker is not None:
        style = np.zeros(len(x), dtype=np.int32)
        for idx in range(len(x)):
            style[idx] = df.index[idx] in marker

    ax = sns.scatterplot(x=x, y=y, hue=hue, palette=palette, legend=None, ax=ax, style=style,
                         markers=['o', '^'],
                         **kwargs)

    for i, row in df.iterrows():
        x = row["log2(fc)"]
        y = row["-log10(p)"]
        if gene_list is not None and (gene_list is True or i in gene_list):
            # gene_list can be either a list or a dictionary containing offsets
            try:
                gene_xoffset, gene_yoffset = gene_list[i]
            except TypeError:
                gene_xoffset, gene_yoffset = xoffset, yoffset
            ax.text(x + gene_xoffset, y + gene_yoffset, i, fontsize=fontsize,
                    horizontalalignment='right')

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    if not axis_labels:
        ax.set_xlabel('')
        ax.set_ylabel('')
    else:
        ax.set_xlabel('log2(fc)', size=fontsize)
        ax.set_ylabel('-log10(p)', size=fontsize)
    plt.xticks(size=fontsize)
    plt.yticks(size=fontsize)

    # TODO: titles
    if title is not None:
        ax.set_title(title)
    elif interaction is not None:
        ax.set_title(" - ".join([v.capitalize() for v in interaction.split("_")]))
    if show:
        plt.show()

    return ax


def plot_similarity_map(adata, idx, ax=None, linewidth=0.5, linecolor="black", title="",
                        show=False, **kwargs):
    if ax is None:
        fig, ax = plt.subplots()
    try:
        scale_factor = list(adata.uns['spatial'].values())[0]['scalefactors'][
            'tissue_hires_scalef']
    except KeyError:
        if scale is not None:
            scale_factor = scale
        else:
            scale_factor = 1
    try:
        boundary = scale_factor * adata.uns["multi_boundaries"][str(idx)]
    except KeyError:
        raise ValueError("Need to compute boundaries first")
    #ax.fill(boundary[:, 0], boundary[:, 1], color_string)
    ax.plot(boundary[:, 0], boundary[:, 1], linewidth=linewidth, color=linecolor)

    arr = similarity_map(adata, idx=idx)

    adata.obs['tmp'] = arr
    spatial(adata, color="tmp", alpha_img=0.5, ax=ax, title=title, frameon=False, show=show,
            **kwargs)