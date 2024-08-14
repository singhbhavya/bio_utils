import scanpy as sc
import gseapy as gp
import pandas as pd
import matplotlib.pyplot as plt
import time

def analyze_cell_type(adata, cell_type, obs, comparison_group, reference_group, gene_set='GO_Biological_Process_2021', output_dir=None):
    # Ensure obs categories are in the correct order
    adata.obs[obs] = pd.Categorical(adata.obs[obs], categories=[comparison_group, reference_group], ordered=True)
    
    # Sort and subset adata by cell type
    indices = adata.obs.sort_values(['annotated', obs]).index
    adata = adata[indices,:]
    
    bdata = adata[adata.obs["annotated"] == cell_type].copy()
    bdata = bdata[~bdata.obs[obs].isna()]

    # GSEA analysis
    t1 = time.time()
    cls_vector = bdata.obs[obs].tolist()
    
    res = gp.gsea(data=bdata.to_df().T, 
                  gene_sets=gene_set,
                  cls=cls_vector,
                  permutation_num=1000,
                  permutation_type='phenotype',
                  outdir=None,
                  method='s2n',
                  threads=16)
    t2 = time.time()
    print(f"GSEA completed in {t2-t1} seconds")

    # Differential expression analysis
    sc.tl.rank_genes_groups(bdata,
                            groupby=obs,
                            use_raw=False,
                            method='wilcoxon',
                            groups=[comparison_group],
                            reference=reference_group)

    result = bdata.uns['rank_genes_groups']
    groups = result['names'].dtype.names
    degs = pd.DataFrame(
        {group + '_' + key: result[key][group]
        for group in groups for key in ['names','scores', 'pvals','pvals_adj','logfoldchanges']})

    # Save DEGs to CSV
    degs_sig = degs[degs[f'{comparison_group}_pvals_adj'] < 0.05]
    degs_up = degs_sig[degs_sig[f'{comparison_group}_logfoldchanges'] > 0]
    degs_dw = degs_sig[degs_sig[f'{comparison_group}_logfoldchanges'] < 0]

    csv_name = f"{comparison_group.lower()}_{cell_type.lower().replace(' ', '_')}.csv"
    degs.to_csv(csv_name, index=False)
    print(f"DEGs saved to {csv_name}")

    # Enrichment analysis for upregulated genes
    gene_list_up = degs_up[f'{comparison_group}_names']
    enr_up = gp.enrichr(gene_list=gene_list_up.tolist(),
                        gene_sets=gene_set,
                        outdir=None)
    enr_up.res2d.Term = enr_up.res2d.Term.str.split(" \(GO").str[0]
    
    # Dotplot for upregulated genes
    gp.dotplot(enr_up.res2d, figsize=(3,5), title="Up", cmap=plt.cm.autumn_r)
    plt.show()

    # Enrichment analysis for downregulated genes
    gene_list_dw = degs_dw[f'{comparison_group}_names']
    enr_dw = gp.enrichr(gene_list=gene_list_dw.tolist(),
                        gene_sets=gene_set,
                        outdir=None)
    enr_dw.res2d.Term = enr_dw.res2d.Term.str.split(" \(GO").str[0]

    # Dotplot for downregulated genes
    gp.dotplot(enr_dw.res2d, figsize=(3,5), title="Down", cmap=plt.cm.winter_r, size=5)
    plt.show()

    return degs
