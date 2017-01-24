#!python3
from random import *
from math import *
from copy import *
from sys import *
from statistics import *
from time import *

#Resolvedor de SUDOKUS con GA
#
#Esther Cuervo Fernandez
#23.Nov.2016

#Constantes
tam_tablero = 9
lado_subgrid = (int)(sqrt(tam_tablero))
probabilidad_recombinacion = 0.6
probabilidad_mutacion = 0.1
tam_poblacion = 10000

#Tableros

tablero_inicial = [8,-1,-1,-1,-1,-1,-1,1,-1,4,-1,6,-1,-1,-1,-1,-1,-1,-1,-1,7,4,-1,-1,6,5,-1,5,-1,9,-1,-1,-1,-1,4,8,-1,3,-1,-1,7,-1,-1,2,-1,7,8,-1,-1,-1,-1,1,-1,3,-1,5,2,-1,-1,1,3,-1,-1,-1,-1,-1,-1,-1,-1,9,-1,2,-1,9,-1,-1,-1,-1,-1,-1,5]

#4x4 SUDOKUS
#Easy
#tablero_inicial = [ 4,-1,-1,-1,-1, 1, 4,-1,-1, 2, 3,-1,-1,-1,-1, 2]

#Hard
#tablero_inicial = [ 1,-1,-1, 4,-1,-1,-1,-1,4,-1,-1,-1,2,-1,-1, 3]

#9x9 SUDOKUS
#Easy
#tablero_inicial = [-1,-1,4,3,-1,8,-1,6,-1,5,-1,-1,-1,-1,7,-1,-1,-1,-1,-1,-1,4,1,5,3,-1,8,2,-1,-1,5,-1,7,6,-1,-1,-1,1,4,-1,8,-1,7,5,-1,-1,-1,7,1,-1,2,-1,-1,4,1,-1,6,8,7,3,-1,-1,-1,-1,-1,-1,2,-1,-1,-1,-1,3,-1,4,-1,5,-1,1,8,-1,-1]
#tablero_inicial = [2,-1,-1,7,5,9,-1,3,4,4,-1,-1,-1,-1,1,-1,5,-1,-1,-1,-1,-1,8,-1,1,-1,-1,-1,-1,-1,5,2,1,-1,8,-1,6,1,5,-1,-1,-1,2,7,4,-1,9,-1,6,7,4,-1,-1,-1,-1,-1,5,-1,9,-1,-1,-1,-1,-1,6,-1,1,-1,-1,-1,-1,7,2,1,-1,5,6,7,-1,-1,8]

#Medium
#tablero_inicial = [3,-1,-1,-1,6,-1,-1,-1,-1,-1,7,6,-1,-1,-1,9,3,-1,-1,1,4,3,-1,-1,7,6,8,-1,-1,5,-1,-1,-1,-1,8,-1,-1,9,-1,8,-1,4,-1,2,-1,-1,4,-1,-1,-1,-1,1,-1,-1,5,3,4,-1,-1,7,6,2,-1,-1,8,2,-1,-1,-1,3,5,-1,-1,-1,-1,-1,5,-1,-1,-1,7]
#tablero_inicial = [6,2,7,-1,-1,3,-1,-1,-1,-1,-1,-1,1,-1,2,-1,4,8,-1,-1,-1,5,-1,-1,2,-1,-1,-1,1,-1,5,-1,-1,7,-1,-1,-1,8,-1,-1,3,-1,-1,1,-1,-1,-1,4,-1,-1,8,-1,5,-1,-1,-1,9,-1,-1,2,-1,-1,-1,4,7,-1,9,-1,6,-1,-1,-1,-1,-1,-1,3,-1,-1,4,9,6]

#Hard
#tablero_inicial = [-1,2,-1,-1,3,1,-1,-1,-1,7,-1,4,-1,-1,8,-1,5,-1,-1,-1,-1,4,-1,-1,-1,-1,2,-1,-1,6,-1,7,-1,3,1,-1,-1,-1,-1,-1,9,-1,-1,-1,-1,-1,9,5,-1,4,-1,7,-1,-1,6,-1,-1,-1,-1,2,-1,-1,-1,-1,1,-1,8,-1,-1,6,-1,9,-1,-1,-1,1,6,-1,-1,5,-1]
#tablero_inicial = [-1,1,-1,-1,-1,3,2,-1,-1,2,-1,5,-1,-1,-1,-1,7,-1,-1,8,-1,4,-1,-1,-1,-1,3,-1,4,-1,-1,-1,-1,-1,7,-1,6,1,2,-1,-1,-1,3,9,8,-1,7,-1,-1,-1,-1,-1,2,-1,4,-1,-1,-1,-1,2,-1,6,-1,-1,6,-1,-1,-1,-1,9,-1,1,-1,-1,9,8,-1,-1,-1,4,-1]

#Evil
#tablero_inicial = [-1,4,-1,-1,1,9,-1,-1,-1,5,-1,2,-1,-1,-1,4,-1,-1,-1,-1,-1,-1,-1,-1,9,-1,-1,3,-1,1,-1,5,-1,-1,7,6,-1,-1,-1,-1,2,-1,-1,-1,-1,4,6,-1,-1,3,-1,5,-1,2,-1,-1,8,-1,-1,-1,-1,-1,-1,-1,-1,6,-1,-1,-1,9,-1,4,-1,-1,-1,8,7,-1,-1,2,-1]

#16x16 SUDOKU
#tablero_inicial = [-1,3,-1,4,15,-1,-1,-1,-1,11,6,-1,-1,-1,13,-1,-1,13,-1,6,-1,-1,5,-1,-1,-1,-1,1,7,3,4,-1,-1,-1,-1,-1,14,1,-1,-1,-1,8,7,2,-1,-1,15,-1,-1,10,-1,-1,7,-1,-1,6,13,5,-1,-1,9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,14,-1,1,16,-1,7,-1,9,13,15,-1,-1,1,4,-1,5,-1,11,9,2,-1,-1,10,-1,-1,5,14,-1,-1,-1,-1,-1,8,-1,-1,3,-1,-1,-1,16,-1,-1,-1,-1,12,-1,-1,-1,6,-1,-1,-1,-1,-1,8,-1,-1,-1,8,-1,-1,-1,-1,-1,-1,-1,-1,14,-1,-1,15,-1,-1,-1,6,-1,15,10,-1,8,-1,1,-1,-1,-1,5,16,14,2,9,4,1,-1,16,-1,-1,-1,-1,6,13,-1,10,-1,-1,14,-1,-1,-1,-1,13,-1,-1,-1,11,5,-1,-1,-1,2,-1,10,12,-1,-1,-1,5,16,13,6,-1,-1,11,2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,11,-1,14,-1,7,-1,-1,-1,10,-1,-1,-1,8,10,4,3,-1,5,-1,-1,-1,-1,-1,12,9,-1,-1,-1,-1,-1,15,-1,-1,16,-1,1,-1,5,7,13,11]


#Funciones auxiliares
def inverso(T):
  return (int)(1/T)
def get_filas(tablero):
   filas = []
   fil = []
   for r in range(lado_subgrid):
     for f in range(lado_subgrid):
       for s in range(lado_subgrid):
         subgrid = s + (r*lado_subgrid)
         for i in range(lado_subgrid):
           elemento_de_subgrid = f*lado_subgrid+i
           e = subgrid*tam_tablero + elemento_de_subgrid
           fil.append(tablero[e])
       filas.append(list(fil))
       fil.clear()

   return filas
def get_indices_filas(tablero):
   filas = []
   fil = []
   for r in range(lado_subgrid):
     for f in range(lado_subgrid):
       for s in range(lado_subgrid):
         subgrid = s + (r*lado_subgrid)
         for i in range(lado_subgrid):
           elemento_de_subgrid = f*lado_subgrid+i
           e = subgrid*tam_tablero + elemento_de_subgrid
           fil.append(e)
       filas.append(list(fil))
       fil.clear()
   return filas
def get_columnas(tablero):
   columnas = []
   col = []
   for r in range(lado_subgrid):
     for c in range(lado_subgrid):
       for s in range(lado_subgrid):
         subgrid = s*lado_subgrid + r
         for i in range(lado_subgrid):
           elemento_de_subgrid = i*lado_subgrid + c
           e = subgrid*tam_tablero + elemento_de_subgrid
           col.append(tablero[e])
       columnas.append(list(col))
       col.clear()
   return columnas
def get_indices_columnas(tablero):
   columnas = []
   col = []
   for r in range(lado_subgrid):
     for c in range(lado_subgrid):
       for s in range(lado_subgrid):
         subgrid = s*lado_subgrid + r
         for i in range(lado_subgrid):
           elemento_de_subgrid = i*lado_subgrid + c
           e = subgrid*tam_tablero + elemento_de_subgrid
           col.append(e)
       columnas.append(list(col))
       col.clear()
   return columnas
def to_String(tablero):
  filas = get_filas(tablero)
  string = ""
  cont_nl = 0
  for f in range(tam_tablero):
    string += " "
    cont_tab = 0
    cont_nl +=1
    for e in filas[f]:
      cont_tab +=1
      if e == -1:
        string += "_"
      else:
        string += str(e)
      string += " "
      if (cont_tab%lado_subgrid)==0:
        string+="\t"
    string += "\n"
    if (cont_nl%lado_subgrid)==0:
      string += "\n"
  string +="\n"

  return string

#Funciones GA
def inicializar(indices_fijos):
  poblacion = [None]*tam_poblacion

  for c in range(tam_poblacion):
    poblacion[c] = [-1]*(tam_tablero*tam_tablero)
    for s in range(tam_tablero):
      permutacion = list(range(1,tam_tablero+1))
      shuffle(permutacion)
      for e in range(tam_tablero):
        poblacion[c][(s*tam_tablero)+e] = permutacion[e]

    for i in indices_fijos:
      subgrid_del_indice = floor(i/tam_tablero)
      array_a_buscar = poblacion[c][tam_tablero*subgrid_del_indice:tam_tablero*(subgrid_del_indice+1)]
      valor_fijo = tablero_inicial[i]
      indice_debe_estar = i
      indice_esta = array_a_buscar.index(valor_fijo)+(subgrid_del_indice*tam_tablero)

      poblacion[c][indice_esta] = poblacion[c][indice_debe_estar]
      poblacion[c][indice_debe_estar] = valor_fijo

  return poblacion
def funcion_adaptacion(tablero):
  colisiones = 0
  filas = get_filas(tablero)
  columnas = get_columnas(tablero)

  for i in filas:
    contadores = [0]*tam_tablero
    for e in i:
      contadores[e-1] += 1

    for j in contadores:
      if j>1:
        colisiones += j-1


  for i in columnas:
    contadores = [0]*tam_tablero
    for e in i:
      contadores[e-1] += 1

    for j in contadores:
      if j>1:
        colisiones += j-1

  #la funcion de adaptacion devolvera el inverso del numero de colisiones. El cromosoma con mayor funcion, tendra menos colisiones
  #esto implica tener en cuenta las posibles 0 colisiones
  if(colisiones == 0):
    return -1
  else:
    inverso = (float)(1/colisiones)
    return inverso
def seleccion(poblacion,funciones,sum_funciones): 
  f_nor = [0]*len(funciones)
  for e in range(len(funciones)):
    f_nor[e] = funciones[e]/sum_funciones

  padres = []
  lista_aleatorios = [0]*tam_poblacion
  for i in range(tam_poblacion):
    lista_aleatorios[i] = random()

  lista_aleatorios.sort()

  sum = 0
  indice_aleatorio = 0

  for i in range(tam_poblacion):
    sum += f_nor[i]
    while indice_aleatorio<tam_poblacion and sum > lista_aleatorios[indice_aleatorio]:
      padres.append(poblacion[i])
      indice_aleatorio += 1

  return padres
def recombinacion(padres):
  nueva_generacion = []
  while len(padres)>1:
    padre_1 = padres[0]
    del padres[0]
    r = randint(0,len(padres)-1)
    padre_2 = padres[r]
    del padres[r]
    if random()<=probabilidad_recombinacion:
      #obligamos a que el punto de corte sea como mucho, la ultima subgrid
      subgrid_corte = randint(0,tam_tablero-2)

      trozo_1 = padre_1[subgrid_corte*tam_tablero:]
      trozo_2 = padre_2[subgrid_corte*tam_tablero:]

      hijo_1 = padre_1[0:subgrid_corte*tam_tablero] + trozo_2
      hijo_2 = padre_2[0:subgrid_corte*tam_tablero] + trozo_1
    else:
      hijo_1 = padre_1
      hijo_2 = padre_2

    nueva_generacion.append(hijo_1)
    nueva_generacion.append(hijo_2)
  #si el tamano de poblacion es impar, quedara un padre en la lista y un hijo sin asignar. si es par, se habran asignado todos
  if len(padres)>0:
    nueva_generacion.append(padres[0])

  return nueva_generacion
def mutacion(poblacion,indices_fijos):
  mutados = poblacion + []
  for c in range(tam_poblacion):
    #intentaremos mutar por cada subgrid en el tablero, protegiendo siempre los valores fijados al principio
    for s in range(tam_tablero):
      r = random()
      if r <= probabilidad_mutacion:
        elemento_1 = randint(0,tam_tablero-1)
        elemento_2 = randint(0,tam_tablero-1)
        while elemento_1 == elemento_2:
          elemento_1 = randint(0,tam_tablero-1)
          elemento_2 = randint(0,tam_tablero-1)

        indice_el_1 = s*tam_tablero + elemento_1
        indice_el_2 = s*tam_tablero + elemento_2

        if(not(indice_el_1 in indices_fijos) and not(indice_el_2 in indices_fijos)):
          tmp = mutados[c][indice_el_1]
          mutados[c][indice_el_1] = mutados[c][indice_el_2]
          mutados[c][indice_el_2] = tmp

  return mutados

def evolucion(poblacion,indices_fijos):
  contador_generaciones = 0
  puntero_minimos = 0

  funciones = [0]*tam_poblacion
  sum_funciones = 0

  for c in range(tam_poblacion):
    funciones[c]=funcion_adaptacion(poblacion[c])
    sum_funciones += funciones[c]

  I = list(map(inverso,funciones))
  desviacion = pstdev(I)
  print("Generacion: ",0,": mejor resultado = ",I[funciones.index(max(funciones))]," peor resultado = ",max(I)," desviacion tipica = ",pstdev(I))

  while True:

    if -1 in funciones:
      print("Solucion encontrada tras ", contador_generaciones, " generaciones")
      print(to_String(poblacion[funciones.index(-1)]))

      print("Constantes:")
      print("Probabilidad de recombinacion ",probabilidad_recombinacion)
      print("Probabilidad de mutacion ",probabilidad_mutacion)
      print("Tamaño poblacion ",tam_poblacion)
      print("Respuesta encontrada en ",time()-tiempo_comienzo," segundos.")

      exit()

    padres = seleccion(poblacion,funciones,sum_funciones)
    siguiente_generacion = recombinacion(padres)
    poblacion = mutacion(siguiente_generacion,indices_fijos)

    contador_generaciones += 1

    sum_funciones = 0
    for c in range(tam_poblacion):
      funciones[c]=funcion_adaptacion(poblacion[c])
      sum_funciones += funciones[c]

    I = list(map(inverso,funciones))
    print("Generacion: ",contador_generaciones,": mejor resultado = ",I[funciones.index(max(funciones))]," peor resultado = ",max(I)," desviacion tipica = ",pstdev(I))

#Main
def main():
  indices_fijos = []

  print("Tablero inicial:")
  print(to_String(tablero_inicial))

  for i in range(tam_tablero*tam_tablero):
    if(tablero_inicial[i]!=-1):
      indices_fijos.append(i)

  poblacion_inicial = inicializar(indices_fijos)
  evolucion(poblacion_inicial,indices_fijos)

print("Constantes:")
print("Probabilidad de recombinacion ",probabilidad_recombinacion)
print("Probabilidad de mutacion ",probabilidad_mutacion)
print("Tamaño poblacion ",tam_poblacion)
tiempo_comienzo = time()

main()
