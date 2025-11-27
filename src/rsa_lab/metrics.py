import numpy as np
from scipy.stats import entropy

def js_divergence(a:np.ndarray,b:np.ndarray,bins='auto')->float:
    ha, edges = np.histogram(a, bins=bins, density=True)
    hb, _ = np.histogram(b, bins=edges, density=True)
    pa = ha / (ha.sum() + 1e-12)
    pb = hb / (hb.sum() + 1e-12)
    m = 0.5*(pa+pb)
    return 0.5*(entropy(pa, m) + entropy(pb, m))

def mutual_information_empirical(samples, labels, bins=50):
    import numpy as np
    x = np.asarray(samples)
    y = np.asarray(labels)
    edges = np.histogram_bin_edges(x, bins=bins)
    bin_idx = np.digitize(x, edges) - 1
    import collections
    total = len(x)
    cnt = collections.Counter((int(b), int(l)) for b,l in zip(bin_idx, y))
    mi = 0.0
    for (b,l), c in cnt.items():
        pxy = c / total
        px = sum(v for (bb,ll), v in cnt.items() if bb==b)/total
        py = sum(v for (bb,ll), v in cnt.items() if ll==l)/total
        mi += pxy * np.log(pxy / (px*py + 1e-12) + 1e-12)
    return mi
