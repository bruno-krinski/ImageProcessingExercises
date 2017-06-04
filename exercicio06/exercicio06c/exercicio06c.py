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
# Nome : contaLinhasImagem                                                     #
# Parametro 1 : nomeImagem                                                     #
# Retorno : numLinhas (Número de linhas na imagem)                             #
# Descrição : Função que conta o número de linhas em uma imagem                #
#------------------------------------------------------------------------------#
def contaLinhasImagem(nomeImagem):
 
  # Abre o arquivo de imagem
  img = cv2.imread(nomeImagem,0)
 
  # Armazena informações de largura e comprimento da imagem
  axisY, axisX = img.shape
 
  # Limiariza a imagem
  ret2, nImg = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
 
  # Conta a quantidade de pixels brancos em cada linha da imagem
  numUns = []
  for y in range(0,axisY):
    numUns.append(axisX - cv2.countNonZero(nImg[y,:]))
  
  # Realiza o plot do histograma com o númedo de pixels brancos em cada 
  # linha da imagem
  plt.subplot(111)
  plt.plot(np.flipud(numUns),range(len(numUns)),'gray')
  plt.title('Histograma')
  
  y1 = 0
  y2 = 0

  count = 0
  limite = 6
  limite2 = 20
  marca = False
  numLinhas = 0
  # Para cada linha do histograma
  for i in range(0,len(numUns)):

    # Verifica se a quantidade de uns é maior que o limite e se ainda não 
    # encontrou nenhuma linha
    if (numUns[i] > limite) and not marca:
      # Marca este ponto como inicio de uma linha
      y1 = i
      # E que ele achou uma linha
      marca = True
    
    #  Se ele ja encontrou uma linha
    if marca:
      # Verifica de o núero de uns está abaixo do limite
      if numUns[i] < limite:
        # Marca este ponto como o final de uma linha
        y2 = i 
      # Veriifca se os pontos tem uma distancia concideravel entre eles  
      if (y2 - y1) > limite2:
        # Então, encontrou uma linha
        numLinhas += 1
        cv2.imwrite('linha'+str(count)+'.jpg',nImg[y1:y2,0:axisX])
        count += 1
        marca = False
  return numLinhas          

#------------------------------------------------------------------------------#
# Função principal                                                             #
#------------------------------------------------------------------------------#
if (__name__ == '__main__'):
 
 # Realiza a leitura do nome do arquivo de imagem a ser aberto
 nomeImagem = input("Digite o nome da imagem: ")
 
 # Chama a função do programa calculando seu tempo de execução
 init = time.time()
 n = contaLinhasImagem(nomeImagem)
 end = time.time()
 
 print("Total de linhas na imagem: " + str(n))
 print("Tempo total de execução: " + str(end-init))
 
 plt.show()

