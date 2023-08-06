def percent_in_top_n(list1, list2, topn):
    """ used to compare top DEGs in separate datasets.
    given two lists (list1 and list2), and the depth
    at which to compare them (topn genes), returns the 
    percentage of genes that are found in both lists, 
    along with the depth at which they were compared

    Params
    ------
    list1: first list to be compared
    list2: second list to be compared
    topn: first n elements in the list to be compared

    Returns
    ------
    Returns the intersection of the two lists as a percentage
    up to the comparison depth, i.e. number of elements that
    were shared between the lists.

    """
    return((len(set(list1[:topn]).intersection(list2[:topn]))/topn)*100), topn

def subsample_by_cluster(adata, obs_key, cluster, n_obs, random_state=0):
    import scanpy as sc
    """ given an anndata object with grouping
    `obs_name` in adata.obs, subsamples specific
    cluster to number of observations n_obs
    """

    temp = adata[adata.obs[obs_key].isin([cluster]),:].copy()
    adata = adata[~adata.obs[obs_key].isin([cluster])]
    temp = sc.pp.subsample(temp, n_obs=n_obs, random_state=random_state, copy=True)
    adata = adata.concatenate(temp)

    return adata

def percent_cluster_expressing_gene(adata, obs_key, cluster, gene):
    import numpy as np
    import scanpy as sc

    temp = adata.copy()
    temp = temp[:,gene]

    for clustername in cluster:

        positive_cells = np.count_nonzero(temp[temp.obs[obs_key].isin([clustername])].X.toarray(), axis=0)
        total_cells = temp[temp.obs[obs_key].isin([clustername])].n_obs
        percent_cells = (positive_cells / total_cells)*100
        print(f'{ positive_cells }/{ total_cells }, {percent_cells} (percent) of cells in {clustername} express {gene}.')

def percent_coexpression(adata, obs_key, cluster, gene1, gene2):
    temp = adata[adata.obs[obs_key].isin([cluster])]
    n_cells = ((temp[:,'{}'.format(gene1)].X.toarray() > 0) & (temp[:,'{}'.format(gene2)].X.toarray() > 0)).sum(0)
    pct_cells = (n_cells/temp.n_obs)*100
    print(f'{n_cells}/{temp.n_obs}, in {cluster} expess {gene1} and {gene2}.( {pct_cells} percent )')

