import matplotlib.pyplot as plt

class Data:
    def __init__(self, d):
        self.foreground = d[0]
        self.background = d[1]
        self.uninterf = float(d[4])
        self.interf = float(d[5])
        tmp = d[6].replace('%', '')
        self.delta = float(tmp)

with open('raw_data.csv', 'r') as f:
    data = [line.strip().split(',') for line in f]
    data = [Data(d) for d in data[1:]]
    data = [d for d in data 
            if d.foreground != 'fio' 
            and d.background != 'fio']
victim = {d.foreground:[] for d in data}
perp = {d.background:[] for d in data}

for d in data:
    victim[d.foreground].append(d.delta)
    perp[d.background].append(d.delta)

labels = sorted(list({d.foreground for d in data}))
vicplot = [victim[l] for l in labels]
perplot = [perp[l] for l in labels]

plt.title("Interference when benchmark program is the victim")
plt.boxplot(vicplot, labels=labels)
plt.axhline(linestyle='--')
plt.xticks(rotation='45')
plt.ylabel('Interference')
plt.tight_layout()
plt.savefig('victim.png', format='png')
plt.clf()

plt.title("Interference when benchmark program is the perpetrator")
plt.boxplot(perplot, labels=labels)
plt.axhline(linestyle='--')
plt.xticks(rotation='45')
plt.ylabel("Interference")
plt.tight_layout()
plt.savefig('perp.png', format='png')

