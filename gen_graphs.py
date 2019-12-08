import argparse
import matplotlib.pyplot as plt
import csv
import numpy as np
from sys import argv

class Data:
    def __init__(self, raw):
        self.foreground = raw[0]
        self.background = raw[1]
        self.desc = raw[2]
        self.value = raw[3]
        self.uninterfered = float(raw[4])
        self.interfered = float(raw[5])
        r = raw[6].replace('%', '')
        self.delta = float(r)
    def fore(self):
        return self.foreground
    def back(self):
        return self.background

parser = argparse.ArgumentParser()
parser.add_argument("-s", '--save', help='save file', default='img.png')
parser.add_argument("-c", '--color', help='define matplotlib colormap', default='RdYlBu')
parser.add_argument('-i', '--input', help='input data file', default='raw_data.csv')
args = parser.parse_args()

svname = args.save
color = args.color
fname = args.input

with open(fname, 'r') as f:
    x = [line.strip().split(',') for line in f]
x = x[1:]
data = [Data(line) for line in x]
labels = list({d.foreground for d in data if d.foreground != 'fio'})
labels.sort()
maps = {l:{k: [] for k in labels} for l in labels}
for d in data:
    if d.fore() == 'fio' or d.back() == 'fio':
        continue
    maps[d.fore()][d.back()].append(d.delta)

for fore in labels:
    for back in labels:
        arr = maps[fore][back]
        k = len(arr)
        if k == 1:
            maps[fore][back] = round(arr[0], 2)
        else:
            maps[fore][back] = round(sum(arr) / k, 2)
arr = []
for fore in labels:
    temp = []
    for back in labels:
        temp.append(maps[fore][back])
    arr.append(temp)


fig, ax = plt.subplots()
im = ax.imshow(arr, cmap=color)
cbar = ax.figure.colorbar(im, ax=ax, cmap=color)
cbar.ax.set_ylabel('% interference', rotation=-90, va='bottom')
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))

ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

plt.xlabel("Foreground")
plt.ylabel("Background")

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(labels)):
    for j in range(len(labels)):
        text = ax.text(j, i, maps[labels[i]][labels[j]], ha="center",
                va='center', color='black')
ax.set_title("VM interference")

fig.tight_layout()
plt.savefig(svname, format='png')
