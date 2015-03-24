__author__ = 'Chusheng Qiu'
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np
import os
import re
import sys

if __name__ == '__main__':

    allow_args_ = ['ngrid', 'nstep', 'nconm', 'nitr'];
    cmd = ['perl','-w','random-walk.pl'];
    arg_formats = [arg+"=%d" for arg in allow_args_];

    ngrid = 100
    nstep = 100

    nconm = [1, 5, 10, 20, 50, 100]
    infect_rates = np.zeros(len(nconm))

    if (len(sys.argv) > 1):
        m = re.search(r"(\w+)=([1-9]\d*)", sys.argv[1])
        if (m.group(1) == 'nitr'):
            cmd.append(arg_formats[allow_args_.index('nitr')] % int(m.group(2)))


    for i, e in enumerate(nconm):
        args = []
        c = cmd[:]
        args.append(arg_formats[0] % (ngrid,))
        args.append(arg_formats[1] % (nstep,))
        args.append(arg_formats[2] % (e, ))
        #combine the command and the arguments into one array
        c.extend(args)
        #execute the random-walk perl script
        (_, ret) = os.popen2(c)
        line = ret.read().split("\n")[1]
        m = re.search(r"(\d+\.?\d*)[ \t]+(\d+\.?\d*)", line)
        infect_rates[i] = float(m.group(1))


    index = np.arange(len(nconm))
    bar_width = 0.35
    opacity = 0.4


    plt.subplot(2,1,1)
    bar_infect = plt.bar(index, infect_rates, bar_width, alpha=opacity, color='r',label='Infected Rate')
    bar_healthy = plt.bar(index + bar_width, 1 - infect_rates, bar_width, alpha=opacity, color='b',label='Healthy Rate')

    plt.xlabel('# of contaminants')
    plt.ylabel('ratio')
    plt.title('Random Walk: Infected & Healthy Rate')
    plt.xticks(index + bar_width, nconm)
    plt.ylim(0,1)
    plt.legend()
    plt.tight_layout()


    plt.subplot(2,1,2)
    plt.xlabel('# of contaminants')
    plt.ylabel('ratio')
    plt.plot(nconm, infect_rates, 'r-', label='Infected Rate')
    plt.plot(nconm, 1 - infect_rates, 'b-', label='Healthy Rate');
    plt.legend()
    plt.show()