import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale

# -*- coding: utf-8 -*-

locale.setlocale(locale.LC_ALL, '')

document = 'date_imobiliare.ro.csv'
data = pd.read_csv(document)

preturi = []

for i in data.Pret:

    pret_str = i.split(' ')

    if (pret_str[0].lstrip() == 'PretNecomunicat'):
        pass
    else:
        pret_int = int(pret_str[0].translate(None, '.'))
        preturi.append(pret_int)

mpdata = []

for i in data.Metri_Patrati:
    mpstr = i.split(' ')

    if (mpstr[0] == 'Etaj' or 'P' in mpstr[0] or mpstr[1] == 'cam'):
        pass
    else:
        if (',' in mpstr[0]):
            mpstr[0] = mpstr[0].replace(',', '.')
        mp_int = float(mpstr[0])
        mpdata.append(mp_int)


preturi_plot = [i / 1000 for i in preturi]



plt.figure(1)
sns.distplot(preturi_plot, bins=10, kde=False, rug=True)
plt.title('Home prices histogram')
plt.xlabel('Price in 1000s EUR')
plt.ylabel('Number of houses')
plt.show()

plt.figure(2)
sns.distplot(preturi_plot, hist=False, rug=True)
plt.title('Forma curbei distributiei pretului dupa numarul de apartamente')
plt.xlabel('Preturi')
plt.ylabel('Number of houses')
plt.show()

print len(preturi_plot)
print len(mpdata)

print 'Highest price:', max(preturi), 'EUR'
print 'Lowest price:', min(preturi), 'EUR'

print 'Highest number of square meters for an apartment:', max(mpdata)
print 'Lowest number of square meters for an apartment:', min(mpdata)
