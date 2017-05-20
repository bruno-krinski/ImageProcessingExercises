#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno: Bruno Alexandre Krinski                                               #
# Matéria: Processamento de Imagens                                            #
# Exercício 01                                                                 #
#------------------------------------------------------------------------------#

import sys
import cv2
import numpy

#------------------------------------------------------------------------------#
# Função: CalculaQuantizacao                                                   #
# Entradas:                                                                    #
# v: Vetor de inteiros                                                         #
# q: Método de quantização                                                     #
# Saída: inteiro com valor da média, mediana ou modo                           #
#------------------------------------------------------------------------------#
def calculaQuantizacao(v,q):
 # Calculo da média #
 if (q == "media"):
  s = 0
  for i in v:
   s += i
  return int(s/len(v))
 # Calculo da mediana #
 elif (q == "mediana"):
  lv = sorted(v)
  n = len(lv)
  if n % 2 == 0:
   return (lv[n/2-1] + lv[n/2]) / 2
  else:
   return lv[len(lv)/2]
 # Calculo da moda #
 elif (q == "moda"):
  moda = -1
  n_moda = 0
  lv = sorted(v)
  for i in lv:
   if i == moda:
    continue
   elif lv.count(i) > n_moda:
    n_moda = lv.count(i)
    moda = i
  return moda
 # Método de quantização desconhecido #
 else:
  print "Parâmetro errado. Técnica de quantização desconhecida"

# Função main #
if (__name__ == '__main__'):
 # Verifica os parametros de entrada #
 if (len(sys.argv) != 5): 
  print "Quantidade de parâmetros errada!!!"
  print "Uso: exercicio01.py <nome da imagem> <porcentual de amostragem> <níveis de cinza> <técnica de quantização(media,mediana,moda)>"
 else:
  
  porcentualAmostragem = float(sys.argv[2])
  nivelCinza = int(sys.argv[3])
  tecnicaQuantizacao = str(sys.argv[4])
  
  imagem = cv2.imread(str(sys.argv[1]),0) 

  numPixelsEixoX = imagem.shape[0]
  numPixelsEixoY = imagem.shape[1] 
  
  print "Quantidade de pixels eixo X: " , numPixelsEixoX
  print "Quantidade de pixels eixo Y: " , numPixelsEixoY  

  nQuadradosX = numPixelsEixoX * porcentualAmostragem
  nQuadradosY = numPixelsEixoY * porcentualAmostragem

  print "Número de quadrados eixo X: ", nQuadradosX
  print "Número de quadrados eixo Y: ", nQuadradosY

  numPixelsCadaQuadradoX = int(numPixelsEixoX / nQuadradosX)
  numPixelsCadaQuadradoY = int(numPixelsEixoY / nQuadradosY)

  print "Número de pixels cada quadrado X: " , numPixelsCadaQuadradoX
  print "Número de pixels cada quadrado Y: " , numPixelsCadaQuadradoY
    
  y = 0
  while y < numPixelsEixoY:
   x = 0
   while x < numPixelsEixoX:
    v = []
    for yl in range(0,numPixelsCadaQuadradoY):
     for xl in range(0,numPixelsCadaQuadradoX):
      if (xl+x < numPixelsEixoX) and (yl+y < numPixelsEixoY):
       v.append(imagem.item(xl + x, yl + y))
    novoValorPixel = calculaQuantizacao(v,tecnicaQuantizacao)
    for yl in range(0,numPixelsCadaQuadradoY):
     for xl in range(0,numPixelsCadaQuadradoX):
      if (xl+x < numPixelsEixoX) and (yl+y < numPixelsEixoY):
       imagem.itemset(xl + x, yl + y, novoValorPixel)
    x += numPixelsCadaQuadradoX
   y += numPixelsCadaQuadradoY
  
  r = int(256 / nivelCinza)
  imagem = numpy.uint8(imagem/r)*r

  cv2.imshow('image',imagem)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
