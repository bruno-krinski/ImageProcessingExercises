#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno : Bruno Alexandre Krinski                                              #
# Matéria : Processamento de Imagens                                           #
# Exercício: Usando a técnica de projeção de histograma, informe a quantidade  # 
#            de linhas de texto presentes na imagem abaixo.                    #
#------------------------------------------------------------------------------#

import cv2
import math
import time
import numpy as np
from matplotlib import pyplot as plt

#------------------------------------------------------------------------------#
# Nome : calculaDCC                                                            #
# Parametro 1 : v (Lista do Chain Codes)                                       #
# Retorno : d (Lista com a diferença dos Chain Codes)                          #
# Descrição : Função que calcula a diferença entre os Chain Codes de um objeto #
#------------------------------------------------------------------------------#
def calculaDCC(v):
  d = []
  for i in range(1,len(v)):
    if (v[i] >= v[i-1]):
      d.append(v[i] - v[i-1])
    else:
      d.append(8-v[i]-v[i-1])
  return d

#------------------------------------------------------------------------------#
# Nome : euclidianDist                                                         #
# Parametro 1 : v1 (lista de elementos)                                        #
# Parametro 2 : v2 (lista de elementos)                                        #
# Retorno : q (Distancia euclidiana entre as duas listas de elementos)         #
# Descrição : Calcula a distancia euclidiana entre duas listas                 #
#------------------------------------------------------------------------------#
def euclidianDist(v1,v2):
  p = 0
  for i in range (0,len(v1)):
    p += (v1[i] - v2[i])**2
  q = math.sqrt(p)
  return q

#------------------------------------------------------------------------------#
# Nome : normalizaVetor                                                        #
# Parametro 1 : v (Lista de elementos)                                         #
# Retorno : n (Lista de elementos)                                             #
# Descrição : Retorna uma lista de elementos contendo a porcentagem de         #
#             ocorrencia de cada elemento na lista de entrada                  #   
#------------------------------------------------------------------------------#
def normalizaVetor(v):
  n = []
  for x in set(v):
    n.append(float(v.count(x))/float(len(v)))
  return n

#------------------------------------------------------------------------------#
# Nome : normalizaVetor                                                        #
# Parametro 1 : v (Lista de elementos)                                         #
# Retorno : n (Lista de elementos)                                             #
# Descrição : Retorna uma lista de elementos contendo a porcentagem de         #
#             ocorrencia de cada elemento na lista de entrada                  #   
#------------------------------------------------------------------------------#
def normalizaVetor2(v):
  n = []
  for x in range(0,8):
    n.append(float(v.count(x))/float(len(v)))
  return n

#------------------------------------------------------------------------------#
# Nome: chainCode                                                              #
# Parametro 1 : p1 (Um par de coordenadas x,y)                                 #
# Parametro 2 : p2 (Um par de coordenadas x,y)                                 #
# Retorno : Chain code correspondende ao par de pontos da entrada              #
# Descrição : Calcula o chain code correspondente ao par de pontos da entrada  #
#------------------------------------------------------------------------------#
def chainCode(p1,p2):
  if (p1[0][0] == p2[0][0]) and (p1[0][1] > p2[0][1]):
    return 0
  elif (p1[0][0] < p2[0][0]) and (p1[0][1] > p2[0][1]):
    return 7
  elif (p1[0][0] < p2[0][0]) and (p1[0][1] == p2[0][1]):
    return 6
  elif (p1[0][0] < p2[0][0]) and (p1[0][1] < p2[0][1]):
    return 5
  elif (p1[0][0] == p2[0][0]) and (p1[0][1] < p2[0][1]):
    return 4
  elif (p1[0][0] > p2[0][0]) and (p1[0][1] < p2[0][1]):
    return 3
  elif (p1[0][0] > p2[0][0]) and (p1[0][1] == p2[0][1]):
    return 2
  elif (p1[0][0] > p2[0][0]) and (p1[0][1] > p2[0][1]):
    return 1  

#------------------------------------------------------------------------------#
# Nome: calculaCC                                                              #
# Parametro 1 : contorno (Lista de pontos do contorno de um objeto)            #
# Retorno : cc (Lista com os chain codes do contorno da imagem)                #
# Descrição : Calcula o chain code de um sequencia de pontos da imagem         #
#------------------------------------------------------------------------------#
def calculaCC(contorno):
  cc = []
  for i in range(1,len(contorno)):
    cc.append(chainCode(contorno[i-1],contorno[i]))
  return cc

#------------------------------------------------------------------------------#
# Nome : calculaDiferençaCC                                                    #
# Parametro 1 : nomeImagem (Nome do arquivo de imagem)                         #
# Retorno : 0                                                                  #
# Descrição : Função que calcula a diferença entre objetos dentro de uma imagem#
#------------------------------------------------------------------------------#
def calculaDiferencaCC(nomeImagem):
 
  # Le a imagem de entrada
  img = cv2.imread(nomeImagem)
 
  # Transforma em escala de cinza
  imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
  # Limiariza a imagem
  ret, thresh = cv2.threshold(imgray,127,255,0)
 
  # Inverte os valores da imagem
  thresh = abs(thresh - 255)
 
  # Calcula a lista de contornos de cada objeto da imagem
  im2,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                                      cv2.CHAIN_APPROX_NONE)
  normalizedCC = []
  normalizedDCC = []
  # Para cada lista de pontos que representam um contorno da imagem
  for cnt in contours:

    # Calcula o chain code dos pontos
    cc = calculaCC(cnt)

    # Calcula a diferença entre os chain codes
    dcc = calculaDCC(cc)
  
    # Normaliza os chain codes
    a = normalizaVetor(cc)

    # Normaliza a diferença entre os chain codes
    b = normalizaVetor2(dcc)

    normalizedCC.append(a)
    normalizedDCC.append(b)
  
  # Limites para definir quais objetos são iguais ou não
  limite = 0.3
  limite2 = 0.2 

  # Para cada conjunto de contornos (objetos)
  for i in range(0,len(contours)):
    cnt = contours[i]
    cntImg = img.copy()
    cntImg2 = img.copy()

    # Calcula a distancia (diferença) entre cada objeto da imagem
    for j in range(0,len(contours)):
      # Primeiro através dos chain codes
      if (euclidianDist(normalizedCC[i],normalizedCC[j]) <= limite):
        cv2.drawContours(cntImg, [contours[j]], 0, (255,0,0),3)
      # Segundo através da diferença entre chain codes
      if (euclidianDist(normalizedDCC[i],normalizedDCC[j]) <= limite2):
        cv2.drawContours(cntImg2, [contours[j]], 0, (0,0,255),3)
    cv2.drawContours(cntImg, [cnt], 0, (0,255,0), 3)
    cv2.imwrite('chainCodes'+str(i)+'.png',cntImg)
    cv2.drawContours(cntImg2, [cnt], 0, (0,255,0), 3)
    cv2.imwrite('chainCodesDiferenca'+str(i)+'.png',cntImg2)
  return 0
  
#------------------------------------------------------------------------------#
# Função principal                                                             #
#------------------------------------------------------------------------------#
if (__name__ == '__main__'):
 nomeImagem = input("Digite o nome da imagem: ")
 
 init = time.time()
 calculaDiferencaCC(nomeImagem)
 end = time.time()

 print("Tempo total de execução: " + str(end-init))

