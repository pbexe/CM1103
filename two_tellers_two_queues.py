from questions_1_and_2 import theoreticalMeanQueueLength, singleQueue, nextTime
import numpy as np
import matplotlib as mpl
from tqdm import tqdm
mpl.use('pgf')

def figsize(scale):
    fig_width_pt = 512.14963                          # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width/2,fig_height/2]
    return fig_size

pgf_with_latex = {                      # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "axes.labelsize": 10/2,               # LaTeX default is 10pt font.
    "font.size": 10/2,
    "legend.fontsize": 8/2,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8/2,
    "ytick.labelsize": 8/2,
    "lines.linewidth": 0.6,
    "figure.figsize": figsize(0.9),     # default fig size of 0.9 textwidth
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",        # plots will be generated using this preamble
        ]
    }
mpl.rcParams.update(pgf_with_latex)

import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import numpy as np


def doubleQueue(alpha, beta, time=480):
    ta, ts1, ts2, c, maxQ = 0, 0, 0, 0, 0
    Q1, Q2 = 1, 1
    simTime = time

    while True:
        if c < simTime:
            if (ta <= ts1) and (ta <= ts2): # ta block
                ts1 -= ta
                ts2 -= ta
                while True:
                    c += ta
                    if Q1 > Q2:
                        Q2 += 1
                    else:
                        Q1 += 1
                    if max(Q1, Q2) > maxQ:
                        maxQ = max(Q1, Q2)
                    ta = nextTime(alpha)
                    if Q1 != 0 and Q2 != 0:
                        break
            elif ts1 < ta and ts1 < ts2: # ts1 block
                ta -= ts1
                ts2 -= ts1
                c += ts1
                Q1 -= 1
                ts1 = nextTime(beta)
                while Q1 == 0 or Q2 == 0:
                    c += ta
                    if Q1 > Q2:
                        Q2 += 1
                    else:
                        Q1 += 1
                    if max(Q1, Q2) > maxQ:
                        maxQ = max(Q1, Q2)
                    ta = nextTime(alpha)
            else: # ts2 block
                ta -= ts2
                ts1 -= ts2
                c += ts2
                Q2 -= 1
                ts2 = nextTime(beta)
                while Q1 == 0 or Q2 == 0:
                    c += ta
                    if Q1 > Q2:
                        Q2 += 1
                    else:
                        Q1 += 1
                    if max(Q1, Q2) > maxQ:
                        maxQ = max(Q1, Q2)
                    ta = nextTime(alpha)
        else:
            return maxQ


def singleQueueTwoTellers(alpha, beta, time=480):
    ta, ts, c, maxQ = 0, 0, 0, 0
    Q = 1
    simTime = time
    while True:
        if c < simTime:
            if ta < ts:
                ts -= ta
                while True:
                    c += ta
                    Q += 1
                    if Q > maxQ:
                        maxQ = Q
                    ta = nextTime(alpha)
                    if Q != 0:
                        break
            else:
                ta -= ts
                c += ts
                if Q > 1:
                    Q -= 2
                else:
                    Q -= 1
                ts = nextTime(beta)
                while Q == 0:
                    c += ta
                    Q += 1
                    if Q > maxQ:
                        maxQ = Q
                    ta = nextTime(alpha)
        else:
            return maxQ


# I make my own newfig and savefig functions
def newfig(width):
    plt.clf()
    fig = plt.figure(figsize=figsize(width))
    ax = fig.add_subplot(111)
    plt.gcf().subplots_adjust(bottom=0.15)
    return fig, ax


def savefig(filename):
    plt.savefig('{}.pgf'.format(filename))
    plt.savefig('{}.pdf'.format(filename))



time = 60 * 8
iterations = 10000
fig, ax  = newfig(1)

beta = np.arange(0, 5, 0.1)
y = []
for i in tqdm(beta):
    total = 0
    for j in range(iterations):
        total += singleQueue(1, i, time)
    y.append(total / iterations)

beta2 = np.arange(0, 5, 0.1)
y2 = []
for i in tqdm(beta2):
    total = 0
    for j in range(iterations):
        total += doubleQueue(1,i, time)
    y2.append(total / iterations)

beta3 = np.arange(0, 5, 0.1)
y3 = []
for i in tqdm(beta3):
    total = 0
    for j in range(iterations):
        total += singleQueueTwoTellers(1,i, time)
    y3.append(total / iterations)


smoothing = 60

s = UnivariateSpline(beta, y, s=smoothing)
xs = np.linspace(0, 4.9, 100)
ys = s(xs)

s2 = UnivariateSpline(beta2, y2, s=smoothing)
xs2 = np.linspace(0, 4.9, 100)
ys2 = s2(xs2)

s3 = UnivariateSpline(beta3, y3, s=smoothing)
xs3 = np.linspace(0, 4.9, 100)
ys3 = s3(xs3)

betatheo = np.arange(0, 1, 0.002)
ytheo = []
for i in betatheo:
    ytheo.append(theoreticalMeanQueueLength(1,i))

# ax.plot(betatheo, ytheo, label="Theoretical Approach")
# ax.plot(beta, y, label="1 Teller")
# ax.plot(beta2, y2, label="2 Tellers")
# ax.plot(beta3, y3, label="2 Tellers 1 Queue")
ax.plot(xs, ys, label="1 Teller")
ax.plot(xs2, ys2, label="2 Tellers 2 Queues")
ax.plot(xs3, ys3, label="2 Tellers 1 Queue")
ax.set_xlabel(r'Mean time of customer interaction $(\beta$ minutes)')
ax.set_ylabel('Mean Queue Length over ' + str(time) + ' minutes')
plt.legend()
savefig('./figs/two_tellers_two_queues')
