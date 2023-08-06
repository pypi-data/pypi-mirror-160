import numpy as np
import matplotlib.pyplot as plt


def bubble_plot(corr):
    # Plot as miracle plot
    p = corr.reset_index().melt(id_vars="drug_pathway")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(
        p["expression_pathway"],
        p["drug_pathway"],
        c=p["value"],
        cmap="RdBu_r",
        s=5 + np.e ** 6 ** p["value"].abs(),
        alpha=0.5,
    )
    ax.set_xticklabels(p["expression_pathway"].unique(), rotation=90)
    return fig
