import scanpy as sc
import pandas as pd
import anndata

def get_activity_dataframe(adata):
    obs_names = list(adata.obs)
    activity_names = [v for v in obs_names if "activity_" in v]
    return sc.get.obs_df(adata, keys=activity_names)


def write(adata, name):
    adata = adata.copy()
    adata.obs.to_pickle(f'{name}.pkl')
    adata.obs = pd.DataFrame(index=adata.obs.index)
    adata.write(f'{name}.h5ad')


def read(name):
    adata = anndata.read_h5ad(f'{name}.h5ad')
    adata.obs = pd.read_pickle(f'{name}.pkl')
    return adata