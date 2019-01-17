# coding: utf-8
from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import time

def generate_mu_constant(t, mu0):
    return mu0
def generate_tau_constant(t, tau0):
    return tau0
def generate_mu_constant(t, mu0):
    return mu0
def generate_tau_exponential(t, tau0, min_delay=0.):
    return stats.expon.rvs(loc=min_delay, scale=tau0)

def run(generate_mu, generate_tau, T):
    t = 0. # time of first starburst
    M = 0. # stellar mass
    N = 0 # number of starbursts
    taus = []
    mus = []
    while True:
        N += 1
        mu = generate_mu(t)
        mus.append(mu)
        M += mu
        tau = generate_tau(t)
        taus.append(tau)
        t += tau
        if t > T: break
    return N, M, taus, mus
    
def run_constant(tau0, mu0, T):
    return run(lambda t: generate_mu_constant(t, mu0),
               lambda t: generate_tau_constant(t, tau0),
               T)
def run_tau_exp(tau0, mu0, T):
    return run(lambda t: generate_mu_constant(t, mu0),
               lambda t: generate_tau_exponential(t, tau0),
               T)
def run_tau_exp_delay(tau0, min_delay, mu0, T):
    return run(lambda t: generate_mu_constant(t, mu0),
               lambda t: generate_tau_exponential(t, tau0, min_delay),
               T)



def run_N(Ntrials, runfunc, label, make_fig=True):
    start = time.time()
    Nhist = np.zeros(Ntrials, dtype=int)
    Mhist = np.zeros(Ntrials)
    for itrial in range(Ntrials):
        out = runfunc(None)
        Nhist[itrial] = out[0]
        Mhist[itrial] = out[1]
    print("{}: {} trials took {:.1f}s".format(label, Ntrials, time.time()-start))
    if make_fig:
        fig, axes = plt.subplots(1,2,figsize=(12,6))
        axes[0].hist(Nhist)
        axes[1].hist(Mhist)
        #sns.distplot(Nhist, ax=axes[0])
        #sns.distplot(Mhist, ax=axes[1])
        axes[0].set_xlabel("N")
        axes[1].set_xlabel("M")
        fig.suptitle(label)
        return Nhist, Mhist, fig
    return Nhist, Mhist

if __name__=="__main__":
    tau0, mu0, T = 100., 100., 800.
    min_delay = 10.
    Ntrials = 100000
    
    run_N(Ntrials, lambda x: run_constant(tau0, mu0, T), "constant")
    run_N(Ntrials, lambda x: run_tau_exp(tau0, mu0, T), "tauexp")
    run_N(Ntrials, lambda x: run_tau_exp_delay(tau0, min_delay, mu0, T), "tauexpdelay")
    plt.show()
