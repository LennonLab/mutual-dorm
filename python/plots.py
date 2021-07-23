import matplotlib.pyplot as plt

def freq_m(path, freqs):
    """
    plots frequency of multiple sims
    """

    fig, axs = plt.subplots(figsize=(8,4), dpi=80)
    axs.hist(freqs, bins=30)
    axs.set_xlabel('Frequency of Type A')

    plt.savefig(path)

    return None

def trait_m(path, trait):
    
    figs, axs = plt.subplots(figsize=(8,4), dpi=80)
    axs.hist(trait, bins=30)
    axs.set_xlabel('Mean trait value')

    plt.savefig(path)
    
    return None

def meta_m(path, metabolites):
    """
    plots frequency of multiple sims
    """

    fig, axs = plt.subplots(figsize=(8,4), dpi=80)
    axs.hist(metabolites, bins=30)
    axs.set_xlabel('Produced metabolites')

    plt.savefig(path)

    return None

def R_m(path, R):
    
    figs, axs = plt.subplots(figsize=(8,4), dpi=80)
    axs.hist(R, bins=30)
    axs.set_xlabel('Internal Resources')

    plt.savefig(path)
    
    return None

def N_m(path, N):

    figs, axs = plt.subplots(figsize=(8,4), dpi=80)
    axs.hist(N, bins=30)
    axs.set_xlabel('Total population density')

    plt.savefig(path)   

    return None
