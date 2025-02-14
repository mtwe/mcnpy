# -*- coding: utf-8 -*-
"""
Created on Wed Feb 04 12:34:38 2015

@author: Aaron
"""

import matplotlib.pyplot as plt
from reader import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import numpy as np

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs
        
    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

def plot_events(events, ignore_termination=False, ignore_surface=False):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    color_dict = {1: 'blue', 2: 'blue', 3: 'red', 4: 'purple', 5: 'orange'}
    
    for ev in events:
        if ignore_termination:
            if ev.type / 1000 == 5:
                continue
        if ignore_surface:
            if ev.type / 1000 == 3:
                continue
        ax.plot([ev.xxx], [ev.yyy], [ev.zzz], 'o', markersize=10, color=color_dict[ev.type/1000], alpha=0.4)
#        length = np.sqrt(ev.uuu**2 + ev.vvv**2 + ev.www**2)
        a = Arrow3D([ev.xxx, ev.xxx + ev.uuu], [ev.yyy, ev.yyy + ev.vvv], [ev.zzz, ev.zzz + ev.www],
                    mutation_scale=20, lw=3, arrowstyle='-|>', color='r', alpha=0.4)
        ax.add_artist(a)
    
    ax.set_xlabel('X (cm)')
    ax.set_ylabel('Y (cm)')
    ax.set_zlabel('Z (cm)')
    
    plt.draw()
    plt.show()
    
if __name__ == '__main__':
    with open('example/ptrac', 'r') as ptrac:
        header = ptrac_header(ptrac)
        input_format = ptrac_input_format(ptrac)
        event_format = ptrac_event_format(ptrac)

        for i in xrange(4):
            history = parse_ptrac_events(ptrac, event_format)

    plot_events(history.events)