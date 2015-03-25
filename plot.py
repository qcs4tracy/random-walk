__author__ = 'Chusheng Qiu'
import matplotlib
import platform
if platform.platform().lower().startswith('darwin'):
    matplotlib.use('TkAgg')
    
from matplotlib import pyplot as plt
import numpy as np
import os
import re
import sys

ngrid = 100
nstep = 100

#parameters to random-walk.pl perl script
allow_args_ = ['ngrid', 'nstep', 'nconm', 'nitr']
cmd = ['perl','-w','random-walk.pl']
arg_formats = [arg+"=%d" for arg in allow_args_]


"""
Experiment with different # of contaminant cells

    Arguments:
        nconms: array, the set of # of contaminant cells
    Return value:
        infect_rates, array, set of infected rate, the same size of nconms array
"""
def run_diff_nconm(nconms):

    infect_rates = np.zeros(len(nconms))

    #execute the perl script and get the result data back
    for i, e in enumerate(nconms):
        args = []
        c = cmd[:]
        args.append(arg_formats[0] % (ngrid,))
        args.append(arg_formats[1] % (nstep,))
        args.append(arg_formats[2] % (e,))
        #combine the command and the arguments into one array
        c.extend(args)
        #execute the random-walk perl script
        (_, ret) = os.popen2(c)
        line = ret.read().split("\n")[1]
        m = re.search(r"(\d+\.?\d*)[ \t]+(\d+\.?\d*)", line)
        infect_rates[i] = float(m.group(1))

    return infect_rates


"""
Experiment with different # of moves

    Arguments:
        nmoves: array, the set of # of moves
        nconm: int, the contaminant cells
    Return value:
        infect_rates, array, set of infected rate, the same size of nmoves array
"""
def run_diff_nmoves(nmoves, nconm=50):

    infect_rates = np.zeros(len(nmoves))

    #execute the perl script and get the result data back
    for i, e in enumerate(nmoves):
        args = []
        c = cmd[:]
        args.append(arg_formats[0] % (ngrid,))
        args.append(arg_formats[1] % (e,))
        args.append(arg_formats[2] % (nconm,))
        #combine the command and the arguments into one array
        c.extend(args)
        #execute the random-walk perl script
        (_, ret) = os.popen2(c)
        line = ret.read().split("\n")[1]
        m = re.search(r"(\d+\.?\d*)[ \t]+(\d+\.?\d*)", line)
        infect_rates[i] = float(m.group(1))

    return infect_rates


#plot a figure on infected rates
def plot(infect_rates, xs, title, xlabel):

    if (len(infect_rates) != len(xs)):
        raise ValueError('the two parameters should be of the same size');

    index = np.arange(len(xs))
    bar_width = 0.35
    opacity = 0.4

    plt.subplot(2,1,1)
    bar_infect = plt.bar(index, infect_rates, bar_width, alpha=opacity, color='r',label='Infected Rate')
    bar_healthy = plt.bar(index + bar_width, 1 - infect_rates, bar_width, alpha=opacity, color='b',label='Healthy Rate')

    plt.xlabel(xlabel)
    plt.ylabel('ratio')
    plt.title(title)
    plt.xticks(index + bar_width, xs)
    plt.ylim(0,1)
    plt.legend()
    plt.tight_layout()

    plt.subplot(2,1,2)
    plt.xlabel(xlabel)
    plt.ylabel('ratio')
    plt.plot(xs, infect_rates, 'r-', label='Infected Rate')
    plt.plot(xs, 1 - infect_rates, 'b-', label='Healthy Rate');
    plt.legend()
    plt.show()


if __name__ == '__main__':
    #decide # of iteration(the more the better) to get the probability estimations
    if (len(sys.argv) > 1):
        m = re.search(r"(\w+)=([1-9]\d*)", sys.argv[1])
        if (m.group(1) == 'nitr'):
            cmd.append(arg_formats[allow_args_.index('nitr')] % int(m.group(2)))

    #diff. # of contaminant cells
    nconm_set = [1, 5, 10, 20, 50, 100]
    inf_rates = run_diff_nconm(nconm_set)
    plot(inf_rates, nconm_set, 'Random Walk with Diff. # of Contaminant Cells: Infected & Healthy Rate', \
         '# of contaminant cells')

    #diff. # of moves
    nmvs = [5, 20, 50, 100, 150, 200]
    inf_rates = run_diff_nmoves(nmvs)
    plot(inf_rates, nmvs, 'Random Walk with Diff. # of Moves: Infected & Healthy Rate', \
         '# of moves')