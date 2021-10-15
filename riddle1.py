#sheabang missing

# load packages
import itertools
import numpy as np
import pandas as pd
import sys

input_file = sys.argv[1]
group_size = int(sys.argv[2])
print(input_file, group_size)

names_list = []
input = []
# input func (sys.argv[1])
with open(input_file, 'r') as f:
  for i in f.readlines():
    #print(i.strip().split(','))
    l = i.strip().split(',')
    l = [i.strip() for i in l]
    input.append(l)
    [names_list.append(i.strip()) for i in l]
    #names_list.append(list(i for i in l]))

names_list = list(set(names_list))
names_list_len = len(names_list)

#group_size = 3 # sys.argv[2]

# összes lehetséges kombináció
comb_all = list(itertools.combinations(names_list, group_size)) 
comb_all[:5]

# mátrix, ahol nyomon lehet követni ki-kivel és hányszor volt már, csapatszámtól és csapatmérettől függetlenül
data = pd.DataFrame(np.zeros((names_list_len,names_list_len)), columns=names_list, index=names_list) 

# szimmetrikus mátrix feltöltése
for lista in input:
  #print(len(lista))
  combis = list(itertools.combinations(lista, 2))
  for c in combis:
    #print(c[0], c[1])
    data.loc[c[0], c[1]] +=1
    data.loc[c[1], c[0]] +=1

# szimeetrikus mátrix felezése, mert egyik része felesleges, duplikátumok szerepelnének
data = data.mask(np.triu(np.ones(data.shape, dtype=np.bool_)))


# Olyan optimális csoportokat keresek, ahol  diákokat rakok össze akik nem voltak még együtt, növekvő soorrendbe rakva, hogy a végén legyenek azok akik együtt voltak 
# Szimmetrikus mátrix lekerdezése és csapatok generálása
# Sőlyok hozzárendelése annak alapján, hányszor voltak együtt az adott emberek
combs_all_new = []
for combos in comb_all:
  weight = 0
  c = list(itertools.combinations(combos, 2))
  for t in c:
    #print(t)
    w = [data.loc[t[0], t[1]] if data.loc[t[0], t[1]] is None else data.loc[t[1], t[0]]]
    #print(int(w[0]))
    weight += int(w[0])
  #print(weight)
  combs_with_weights = (weight, combos)
  #print(combs_with_weights)
  combs_all_new.append(combs_with_weights)


# súlyok közül mi a maximum érték
max_ertek = 0
for tuples in combs_all_new:
  if tuples[0] > max_ertek:
    max_ertek = tuples[0]


# kombinációk növekvő sorrendbe rakása
sorted_combs_all_new = []

for i in range(max_ertek+1):
  for tuples in combs_all_new:
    if tuples[0] == i:
      sorted_combs_all_new.append(tuples)

# Output - Generating output.txt a sorbarendezett súlyokkal és csoportokkal
# data list of tuples
def output(lista):
   with open('output.txt', 'w') as f:
    for t in lista:
      for elem in t[1]:
          f.write(elem + ", ")
      f.write("\n")

print(sorted_combs_all_new)
output(sorted_combs_all_new)

