#!/usr/bin/env python3

import random
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.path as path

N = 100
CyclesPerIteration = 10
Amount = 100
verbose = True
write_movie = False

fig, ax = plt.subplots()
fig.canvas.set_window_title('Give away money')
ax.set_xlim(0, N)
ax.set_ylim(0, 6 * Amount)
ax.set_xlabel('people')
ax.set_ylabel('money')

counter_text = ax.text(2, Amount * 6 - 30, '', fontsize=8, fontweight='bold')
stddev_text = ax.text(2, Amount * 6 - 50, '', fontsize=8)

data = np.ones(N, dtype=np.int32) * Amount
lo = np.ones(N, dtype=np.float32) * Amount
hi = np.zeros(N, dtype=np.float32)
avg = np.zeros(N, dtype=np.float32)
cumsum = np.zeros(N, dtype=np.float32)

left = np.arange(N, dtype=np.int32)
right = left + 1

# create bars
bar_nverts = N * (1 + 3 + 1)
bar_verts = np.zeros((bar_nverts, 2))
bar_codes = np.ones(bar_nverts, dtype=int) * path.Path.LINETO
bar_codes[0::5] = path.Path.MOVETO
bar_codes[4::5] = path.Path.CLOSEPOLY
bar_verts[0::5, 0] = left
bar_verts[0::5, 1] = np.zeros(N)  # bottom
bar_verts[1::5, 0] = left
bar_verts[1::5, 1] = np.zeros(N)  # top
bar_verts[2::5, 0] = right
bar_verts[2::5, 1] = np.zeros(N)  # top
bar_verts[3::5, 0] = right
bar_verts[3::5, 1] = np.zeros(N)  # bottom
bar_path = path.Path(bar_verts, bar_codes)
bar_patch = patches.PathPatch(
    bar_path, facecolor='#7b9bce', edgecolor='#a3bfed', lw=1)
ax.add_patch(bar_patch)

# create upper limits line strips
upper_nverts = N * 2
upper_codes = np.ones(upper_nverts, dtype=int) * path.Path.MOVETO
upper_codes[1::2] = path.Path.LINETO
upper_verts = np.zeros((upper_nverts, 2))
upper_verts[0::2, 0] = left
upper_verts[0::2, 1] = np.zeros(N)
upper_verts[1::2, 0] = right
upper_verts[1::2, 1] = np.zeros(N)
upper_path = path.Path(upper_verts, upper_codes)
upper_patch = patches.PathPatch(
    upper_path, edgecolor='#11cc11', lw=2)
ax.add_patch(upper_patch)

# create lower limits line strips
lower_nverts = N * 2
lower_codes = np.ones(lower_nverts, dtype=int) * path.Path.MOVETO
lower_codes[1::2] = path.Path.LINETO
lower_verts = np.zeros((lower_nverts, 2))
lower_verts[0::2, 0] = left
lower_verts[0::2, 1] = np.zeros(N)
lower_verts[1::2, 0] = right
lower_verts[1::2, 1] = np.zeros(N)
lower_path = path.Path(lower_verts, lower_codes)
lower_patch = patches.PathPatch(
    lower_path, edgecolor='#cc1111', lw=2)
ax.add_patch(lower_patch)

# create average line strips
avg_nverts = N * 2
avg_codes = np.ones(avg_nverts, dtype=int) * path.Path.MOVETO
avg_codes[1::2] = path.Path.LINETO
avg_verts = np.zeros((avg_nverts, 2))
avg_verts[0::2, 0] = left
avg_verts[0::2, 1] = np.zeros(N)
avg_verts[1::2, 0] = right
avg_verts[1::2, 1] = np.zeros(N)
avg_path = path.Path(avg_verts, avg_codes)
avg_patch = patches.PathPatch(
    avg_path, edgecolor='#111111', lw=2, alpha=0.8)
ax.add_patch(avg_patch)

random.seed()

counter = 0


def animate(_):
    global lo, hi, avg, cumsum, counter
    for j in range(CyclesPerIteration):
        for k in range(N):
            if data[k] > 0:
                while True:  # make sure to give away money to another person
                    to = random.randrange(N)
                    if to != k:
                        break
                data[k] -= 1
                data[to] += 1
        counter += 1
        lo = np.fmin(lo, data)
        hi = np.fmax(hi, data)
        cumsum = cumsum + data
        avg = cumsum / counter
    bar_verts[1::5, 1] = data
    bar_verts[2::5, 1] = data
    lower_verts[0::2, 1] = lo
    lower_verts[1::2, 1] = lo
    upper_verts[0::2, 1] = hi
    upper_verts[1::2, 1] = hi
    counter_text.set_text('# {:d}'.format(counter))
    avg_verts[0::2, 1] = avg
    avg_verts[1::2, 1] = avg
    stddev_text.set_text('σ = {:.2f}'.format(np.std(avg)))
    if write_movie:
        moviewriter.grab_frame()
    if verbose:
        print("\r{} iterations ...".format(counter), end='', flush=True)
    return [bar_patch, upper_patch, lower_patch, avg_patch, counter_text, stddev_text]


if write_movie:
    Writer = animation.writers['ffmpeg']
    moviewriter = Writer(fps=25, bitrate=2000)
    moviewriter.setup(fig=fig, outfile='give-away-1$-B.mp4', dpi=72)

ani = animation.FuncAnimation(fig, animate, data, interval=1, blit=True)

plt.show()

if write_movie:
    moviewriter.finish()
