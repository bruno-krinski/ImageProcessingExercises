#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno : Bruno Alexandre Krinski                                              #
# Matéria : Processamento de Imagens                                           #
# Exercicio: Implemente uma programa que leia a imagem abaixo e forneça como   #
#            saída uma imagem colorida com os objetos rotulados e também uma   # 
#            lista com a área de cada objeto.                                  #
#------------------------------------------------------------------------------#

import cv2
import math
import time
import numpy as np
from matplotlib import pyplot as plt

#------------------------------------------------------------------------------#
# Nome : celulas                                                               #
# Parametro 1 : nomeImagem (Nome do arquivo de imagem)                         #
# Retorno : imgThresholdCopy3 (Imagem contendo o resultado)                    #
# Descrição : Função que calcula a area em pixels da um conjunto de células    #
#------------------------------------------------------------------------------#
def celulas(nomeImagem):
 
  # Abre o arquivo da imagem
  imgInput = cv2.imread(nomeImagem,0) 
 
  # Aplica o filtro da mediana na imagem
  imgMedian = cv2.medianBlur(imgInput,3)
 
  # Faz a limiarização da imagem
  ret,imgThreshold = cv2.threshold(imgMedian,220,255,cv2.THRESH_BINARY_INV)
 
  # Encontra os contornos dos objetos da imagem 
  a,contours,b = cv2.findContours(imgThreshold,cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_NONE)
 
  imgThresholdCopy = imgThreshold.copy()
 
  # Gera uma imagem toda preta
  imgThreshold[0:imgThreshold.shape[0],0:imgThreshold.shape[1]] = 0 
  
  # Imagem que armazenará todos os contornos
  imgThresholdCopy3 = imgThreshold.copy()
  imgThresholdCopy3 = cv2.cvtColor(imgThresholdCopy3,cv2.COLOR_GRAY2BGR)
 
  count = 0
  listOfAreas = []

  # Para cada contorno encontrada na imagem
  for c in contours:
    
    # Imagem para armazenar um único contorno
    imgThresholdCopy2 = imgThreshold.copy()
    imgThresholdCopy2 = cv2.cvtColor(imgThresholdCopy2,cv2.COLOR_GRAY2BGR)

    # Desenha este contorno na imagem tota preta
    cv2.drawContours(imgThresholdCopy2, [c], 0, (0,255,0), 1)
    
    
    # Desenha este contorno na imagem contendo os demais contornos
    cv2.drawContours(imgThresholdCopy3, [c], 0, (0,255,0), 1)
    
    imgThresholdCopy2 = cv2.cvtColor(imgThresholdCopy2,cv2.COLOR_BGR2GRAY)
    
    # Encontra todos os circulos na imagem que contém somente o contorno atual
    circles = cv2.HoughCircles(imgThresholdCopy2,
                               cv2.HOUGH_GRADIENT,
                               1,
                               10,
                               param1=20,
                               param2=15,
                               minRadius=20,
                               maxRadius=30)

    # Caso tenha encontrado algum circulo
    if circles != None:
           
      n = 0
      somaArea = 0

      circles = np.uint16(np.around(circles))
      imgThresholdCopy2 = cv2.cvtColor(imgThresholdCopy2,cv2.COLOR_GRAY2BGR)
      
      # Para cada circulo encontrado
      for i in circles[0,:]:

        # Desenha ele na imagem
        cv2.circle(imgThresholdCopy3,(i[0],i[1]),i[2],(255,0,0),1)
        
        # Calcula a area deste circulo
        area = int(math.pi * (i[2]**2))
        
        listOfAreas.append(area)

        # E armazena a area em um acumulador
        somaArea += area
        
        n += 1

        # Encontra as coordenadas para escrever o rótulo da célula
        x = i[0]
        y = i[1]

        # Ajuste fino para imagens muito próximas da borda
        if count == 13:
          x -= 10

        # Escreve o rótulo do circulo (célula) na imagem
        cv2.putText(imgThresholdCopy3,str(count),(x,y), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0))
        count += 1
      # Calcula a area média dos ciruclos encontrados
      mediaArea = somaArea/n

      # Calcula a area total do contorno
      totArea = int(cv2.contourArea(c))

      # Verifica se tem células cujo circulo não foi detectado
      if ((totArea - somaArea) >= 0.5*mediaArea):
        
        # Ajusta na mão os casos especiais
        
        M = cv2.moments(c)
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        if count == 8:
          y += 20
        elif count == 36:
          y += 10
        elif count == 61:
          x += 30 
        listOfAreas.append(mediaArea)

        cv2.putText(imgThresholdCopy3,str(count),(x+10,y), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0))
        count += 1   
    # Caso não encontre nenhum circulo, é calculado a area do contorno
    else:
      M = cv2.moments(c)
      x = int(M["m10"] / M["m00"])
      y = int(M["m01"] / M["m00"]) 
      area = int(cv2.contourArea(c))
      listOfAreas.append(area)

      if count == 36:
        x -= 10
      cv2.putText(imgThresholdCopy2,str(count), (x,y), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0))
      cv2.putText(imgThresholdCopy3,str(count), (x,y), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,0,0))
      count += 1
  
  # Imprime a lista de areas  
  for l in range(0,len(listOfAreas)):
    print("A célula número " + str(l) + " tem area: " + str(listOfAreas[l]))
  print("Total de células: " + str(len(listOfAreas)))

  return imgThresholdCopy3
#------------------------------------------------------------------------------#
# Função principal                                                             #
#------------------------------------------------------------------------------#
if (__name__ == '__main__'):
  nomeImagem = input("Digite o nome da imagem: ")
 
  init = time.time()
  img = celulas(nomeImagem)
  end = time.time()

  cv2.imshow("Imagem Final", img)
  cv2.waitKey(0)
