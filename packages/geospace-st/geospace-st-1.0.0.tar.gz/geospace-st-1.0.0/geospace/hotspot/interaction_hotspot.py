from tqdm import tqdm
import numpy as np
import pandas as pd

from geospace.hotspot.hotspot import _compute_cutoff, compute_hotspots
from geospace.utility.utility import get_activity_dataframe
from geospace.cci.cci import compute_activity


def interaction_hotspots(adata, verbose=False, interactions=None, save_activity=False,
                         method='permutation', min_active_count=1, sig_threshold=0.95, **kwargs):
    # check if activity scores are available
    activity_matrix = get_activity_dataframe(adata)
    if len(list(activity_matrix)) == 0:
        # TODO: really should only compute activity for interactions in the filter if interactions
        # is not None
        try:
            um_scale = adata.uns['um_scale']
        except KeyError:
            # Try to get it automatically assuming Visium data with 55um spots
            try:
                dataset = list(adata.uns['spatial'].keys())[0]
                um_scale = adata.uns['spatial'][dataset]['scalefactors']['spot_diameter_fullres']/55
            except KeyError:
                raise ValueError("Please set adata.uns['um_scale'] to the length of one micrometer"
                                 " in the units of adata.obsm['spatial'].") from None

        secreted_std = 40*um_scale
        contact_threshold = 20*um_scale

        perform_permutations = method == 'permutation'
        activity_matrix = compute_activity(adata, secreted_std=secreted_std,
                                           contact_threshold=contact_threshold,
                                           sig_threshold=sig_threshold,
                                           perform_permutation=perform_permutations,
                                           save_activity=save_activity, verbose=verbose,
                                           min_active_count=min_active_count,
                                           interactions=interactions)

    cols = enumerate(list(activity_matrix))

    if verbose:
        print("Computing CCI hotspots")
        # everything precomputed so following step does not take significant time
        #cols = tqdm(cols, total=activity_matrix.shape[1])

    region_dict = {}

    for _, interaction in cols:
        if interactions is not None and interaction not in interactions:
            # interaction filter
            continue

        data = activity_matrix[interaction]

        if method == 'permutation':
            cutoff = adata.uns['activity_significance_cutoff'][interaction]
        else:
            cutoff = _compute_cutoff(data)

        inds = np.where(data > cutoff)[0]

        regions = compute_hotspots(adata=adata, input_data=inds, return_regions=True, **kwargs)

        if regions is not None:
            region_dict[f"hotspots_{interaction}"] = regions

    hotspots_df = pd.DataFrame(region_dict, index=adata.obs.index)
    adata.obs = pd.concat([adata.obs, hotspots_df], axis=1)
