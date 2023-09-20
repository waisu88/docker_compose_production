from itertools import combinations

lista = [{'Robert', 'Damian'}, {'Robert', 'Hania'}, {'RobertoGOmez', 'Robert'}, {'Damian', 'Robert'}, {'Damian', 'Hania'}, {'RobertoGOmez', 'Damian'}, {'Robert', 'Hania'}, {'Damian', 'Hania'}, {'RobertoGOmez', 'Hania'}, {'RobertoGOmez', 'Robert'}, {'RobertoGOmez', 'Damian'}, {'RobertoGOmez', 'Hania'}]

lista2 = [list(e) for e in lista]

lista3 = combinations(lista2, 4)

print(lista2)
for el in lista3:
    print(el)
print(lista3)
