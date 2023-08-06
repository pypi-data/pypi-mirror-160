import warnings
import scipy.sparse

import numpy as np

from sklearn.neighbors import BallTree
from sklearn.preprocessing import normalize
from scipy.spatial import Delaunay


def get_neighbor_adjacency(coords, eps=None, k=None, weight=None, return_row_col=False):
    """
    Compute either k-nearest neighbor or epsilon-radius neighbor adjacency graph
    :param coords: Spatial coordinates of each cell
    :param eps: radius cutoff for epsilon-radius neighbors
    :param k: number of nearest neighbors for k-nearest neighbors
    :param weight: Function mapping distance to value in weighted adjacency (default: f(x) = 1)
    :param return_row_col: If true, return the row and column variables from sparse coo format
    :return:
    """
    tree = BallTree(coords)
    n_cells = len(coords)
    if eps is not None and k is not None:
        warnings.warn('k is ignored if eps is provided')

    if eps is not None:
        nearby_col, dist = tree.query_radius(coords, eps, return_distance=True)
        coords = []
        nearby_row = []
        for i, col in enumerate(nearby_col):
            nearby_col[i] = col
            if weight is not None:
                coords.append(weight(dist[i]))
            nearby_row.append(i * np.ones(shape=col.shape, dtype=col.dtype))
    elif k is not None:
        nearby_col = tree.query(coords, k,
                                return_distance=False)  # [:, 1:]  # remove self connections
        nearby_row = []
        for i, col in enumerate(nearby_col):
            nearby_row.append(i * np.ones(shape=col.shape, dtype=col.dtype))
    else:
        raise ValueError("Provide either distance eps or number of neighbors k")

    nearby_row = np.concatenate(nearby_row)
    nearby_col = np.concatenate(nearby_col)
    if weight is None or k is not None:
        coords = np.ones(shape=nearby_row.shape)
    else:
        coords = np.concatenate(coords)

    nearby = scipy.sparse.csr_matrix((coords, (nearby_row, nearby_col)),
                                     shape=(n_cells, n_cells))

    if return_row_col:
        return nearby, nearby_row, nearby_col

    return nearby


def compute_spatial_transport_matrices(adata,
                                       secreted_std,
                                       secreted_threshold_cutoff,
                                       contact_threshold=None):
    """
    Return the spatial prior belief of possibility of interaction between every possible pair of
    cells for both secreted signaling and cell-cell contact type interactions
    """

    ncells = adata.shape[0]

    # gaussian diffusion kernel - threshold is two standard deviations
    sigma = secreted_std

    def weight_fn(x):
        return np.exp(-0.5 * ((x / (2 * sigma)) ** 2))

    coords = adata.obsm['spatial']
    transport_secreted = get_neighbor_adjacency(coords, eps=sigma * secreted_threshold_cutoff,
                                                weight=weight_fn)

    # delauney for direct contact
    tri = Delaunay(adata.obsm['spatial'])
    indptr, indices = tri.vertex_neighbor_vertices
    data = np.ones(shape=indices.shape)
    transport_contact = scipy.sparse.csr_matrix((data, indices, indptr), shape=[ncells, ncells])

    # filter out edges in delauney triangulation that are too long
    if contact_threshold is not None:
        transport_contact = transport_contact.multiply(
            get_neighbor_adjacency(coords, eps=contact_threshold))

    # normalize across number of neighbors
    transport_contact = normalize(transport_contact, norm='l1', axis=1)
    transport_secreted = normalize(transport_secreted, norm='l1', axis=1)

    adata.obsp['transport_contact'] = transport_contact
    adata.obsp['transport_secreted'] = transport_secreted
