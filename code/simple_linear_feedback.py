import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats as stats
from scipy.interpolate import interp1d
from scipy.integrate import odeint
from math import log
import sys

# normal reactions for simple birth/death process
def ReactionsNormal(selected_reaction,w,m):
    x = w+m
    if 'h1' in selected_reaction:
        w += 1
    elif 'h2' in selected_reaction:
        if w<=0:
            w = w
        else:
            w -= 1
    elif 'h3' in selected_reaction:
        m += 1
    elif 'h4' in selected_reaction:
        if m<=0:
            m = m
        else:
            m -= 1
    return w,m

# simple gillespie
def GillespieNormal(t_max,w,m,mu,b,nss,delta):
    reactions = ['h1','h2','h3','h4']
# used for time points when reactions occurred
    times = []
# ms and ws are used for storing quantities of mutant and wild type overtime
    ms = []
    ws = []
    t = 0
    hs = []
# continue iterating as long as t is less than t_max and m/w populations are both greater than 0
    while t<t_max:
# define lambda based on the equation of the system
        lam = mu + b*(nss-w-delta*m)
# check that lambda is greater than 0
        if lam>0:
# calculate hazards for each reaction
            h1 = lam*w
            h2 = mu*w
            h3 = lam*m
            h4 = mu*m
# sum up all hazards
            h0 = h1 + h2 + h3 + h4
# calculate probabilities for each reaction occurring
            p1 = h1/h0
            p2 = h2/h0
            p3 = h3/h0
            p4 = h4/h0
# calculate time until next reaction
            t_prime = -log(np.random.uniform())/h0
            t = t_prime+t
# randomly select reaction using probability weights
            selected_reaction = random.choices(reactions, weights = (p1,p2,p3,p4))
# update w and m depending on which reaction was chosen
            w,m = ReactionsNormal(selected_reaction,w,m)
# calculate heteroplasmy
            h = m/(m+w)
# add information to lists
            hs.append(h)
            times.append(t)
            ws.append(w)
            ms.append(m)
# if lambda is less than 0, set lambda to 0 and continue
        else:
            lam = 0
            h1 = lam*w
            h2 = mu
            h3 = lam*m
            h4 = mu
# sum up all hazards
            h0 = h1 + h2 + h3 + h4
# calculate probabilities for each reaction occurring
            p1 = h1/h0
            p2 = h2/h0
            p3 = h3/h0
            p4 = h4/h0
# calculate time until next reaction
            t_prime = -log(np.random.uniform())/h0
            t = t_prime+t
# randomly select reaction using probability weights
            selected_reaction = random.choices(reactions, weights = (p1,p2,p3,p4))
# update w and m depending on which reaction was chosen
            w,m = ReactionsNormal(selected_reaction,w,m)
# calculate heteroplasmy
            h = m/(m+w)
# add information to lists
            hs.append(h)
            times.append(t)
            ws.append(w)
            ms.append(m)
    return hs,ws,ms,times

TMAX = 1000
x0 = [int(sys.argv[1]),int(sys.argv[2])]
w0 = x0[0]
m0 = x0[1]
mu = 0.023
b = 10**-4
nss = 1000
delta = 1

het_linear,w_linear,m_linear,time_linear = GillespieNormal(TMAX,w0,m0,mu,b,nss,delta)
plt.plot(w_linear,m_linear)
plt.show()
