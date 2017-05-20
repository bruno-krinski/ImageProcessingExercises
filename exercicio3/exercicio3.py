#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno: Bruno Alexandre Krinski                                               #
# Matéria: Processamento de Imagens                                            #
# Exercicio 03                                                                 #
#------------------------------------------------------------------------------#

import cv2
import math
import time
import numpy as np
from matplotlib import pyplot as plt

#------------------------------------------------------------------------------#
# Funções utilizadas em ambos exercícios                                       #
#------------------------------------------------------------------------------#

# Função para realizar o plot de imagens
# t = 0 -> imagem
# t = 1 -> histograma
# c = 0 -> cinza
# c = 1 -> colorido
# clr -> cor do histograma
def plotador(img,position,title,t,c,clr):
 plt.subplot(position)
 if (t == 0 and c == 0):
  plt.imshow(img,'gray') 
  plt.title(title)
  plt.xticks([])
  plt.yticks([])
 elif (t == 0 and c == 1):
  plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
  plt.title(title)
  plt.xticks([])
  plt.yticks([])
 elif (t == 1 and c == 0):
  cv2.normalize(img,img,0,1,cv2.NORM_MINMAX)
  plt.plot(img,'gray')
  plt.title(title)
  plt.xlim([0,255])
  plt.ylim([0,1])
 elif (t == 1 and c == 1):
  cv2.normalize(img,img,0,1,cv2.NORM_MINMAX)
  plt.plot(img,color = clr)
  plt.title(title)
  plt.xlim([0,255])
  plt.ylim([0,1])

# Função que compara dois histogramas
def comparaHistogramas(h1,h2):
 cv2.normalize(h1,h1,0,1,cv2.NORM_MINMAX)
 cv2.normalize(h2,h2,0,1,cv2.NORM_MINMAX)
 return cv2.compareHist(h1,h2,cv2.HISTCMP_CORREL)

#------------------------------------------------------------------------------#
# Exercicio 01                                                                 #
# Faça um programa que receba o valor do resvio padrao 'sigma' e o tamanho do  #
# filtro, gere o filtro gaussiano correspondente e o convolucione com uma      #
# imagem                                                                       #
#------------------------------------------------------------------------------#

# Função Gaussiana
def g(x,y,sigma2):
 x = x**2
 y = y**2
 a = float(math.exp(-(float((x+y)/sigma2)))/(math.pi*sigma2))
 return a
 
# Função que calcula a imagem através do filtro gaussiano do openCV
def gaussianOpencv(img, tamMask):
 return cv2.GaussianBlur(img,(tamMask,tamMask),0)
 
# Função que calcula a imagem através da mascara que eu construi 
def minhaGaussiana(img,tamMask,sigma):
   
 sigma2 = 2 * (float(sigma)**2)
 pivo = tamMask/2
 vMask = []
 mask = np.ones((tamMask,tamMask),np.float32)

 for x in xrange(-pivo, pivo+1):
  for y in xrange(-pivo, pivo+1):
   vMask.append(g(x,y,sigma2))

 count = 0
 for i in xrange(0,tamMask):
  for j in xrange(0,tamMask):
   mask.itemset((i,j),vMask[count])
   count += 1
 return cv2.filter2D(img,-1,mask)

# Função do exercício 1
def exercicio01(imagem):
 
 # Leitura da imagem
 img = cv2.imread(imagem,0)
 
 # Leitura do tamanho da mascara, deve ter tamanho ímpar
 tamMask = input("Entre com o tamanho da mascara:")
 if tamMask % 2 == 0:
  print "Tamanho de máscara inválido. A mascara tem tamanho ímpar!"
  return 0
 
 # Leitura do valor do sigma
 sigma = input("Entre com o valor do sigma:")

 # Calcula o histograma da imagem original
 h0 = cv2.calcHist([img],[0],None,[256],[0,256])
 
 # Executa a máscara gaussiana através da função do openCV
 init = time.time()
 gaussianBlur = gaussianOpencv(img,tamMask)
 end = time.time()
 
 # Calcula o histograma da imagem resultante
 h1 = cv2.calcHist([gaussianBlur],[0],None,[256],[0,256])
 
 print "Tempo de execução do filtro gaussiano do openCV: " + str(end-init)
 
 # Executa a máscara gaussiana através da minha implementação
 init = time.time()
 dst  = minhaGaussiana(img,tamMask,sigma)
 end = time.time()
 
 # Calcula o histograma da imagem resultante
 h2 = cv2.calcHist([dst],[0],None,[256],[0,256])
 
 # Impressão dos resultados
 print "Tempo de execução do meu filtro gaussiano:       " + str(end-init)
 
 print "-------------------------------------------------------------"
 print "Igualdade entre a imagem original e a imagem gaussiana opencv:"
 print comparaHistogramas(h0,h1)
 print "\nIgualdade entre a imagem original e a imgem minha gaussiana:"
 print comparaHistogramas(h0,h2)
 print "\nIgualdade entre a imagem gaussiana opencv e minha gaussiana:"
 print comparaHistogramas(h1,h2)
 print "-------------------------------------------------------------"

 plotador(gaussianBlur,323,'Imagem GaussianBlur',0,0,0)
 plotador(dst,325,'Minha Gaussiana',0,0,0)
 plotador(img,321,'Original',0,0,0)
 plotador(h0,322,'Histograma',1,0,0)
 plotador(h1,324,'Histograma',1,0,0)
 plotador(h2,326,'Histograma',1,0,0) 
 
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# Implemente um filtro da mediana e compare o desempenho com a implementação   #
# do openCV tanto em termos da imagem resultante, quanto em tempo de processa- #
# mento. Teste com imagens de grandes dimensões.                               #
#------------------------------------------------------------------------------#

# Função que converte uma imagem em um vetor
def img2vetor(mascara,tam):
 v = [] 
 for y in xrange(0,tam):
  for x in xrange(0,tam):
   v.append(mascara[y,x])
 return sorted(v)

# Função que calcula a imagem através do filtro da mediana do opencv
def medianaOpencv(img,tamMask):
 return cv2.medianBlur(img,tamMask)

# Função que calcula a imagem através do filtro da mediana que eu construi
def minhaMediana(img,tamMask):
 
 axisY = img.shape[0]
 axisX = img.shape[1]

 aumento = int(round(tamMask/2))

 nImg = cv2.copyMakeBorder(img,aumento,aumento,aumento,aumento,
                                                        cv2.BORDER_REFLECT_101)
 nAxisY = nImg.shape[0]
 nAxisX = nImg.shape[1]
 
 endImg = np.ones((axisY,axisX),np.float32)
 for y in xrange(0,nAxisY-tamMask+1):
  for x in xrange(0,nAxisX-tamMask+1):
   mascara = nImg[y:y+tamMask,x:x+tamMask]
   v = img2vetor(mascara,tamMask)
   endImg[y,x] = v[int(round(len(v)/2))+1]
 
 return endImg  
  
# Função do exercício 2
def exercicio02(imagem):

 # Leitura da imagem e to tamanho da máscara, que deve ser um número ímpar
 img = cv2.imread(imagem,0)
 tamMask = input("Entre com o tamanho da máscara:")
 if tamMask % 2 == 0:
  print "Tamanho de máscara inválido. A mascara tem tamanho ímpar!"
  return 0
 
 # Calcula o histograma da imagem original 
 h0 = cv2.calcHist([img],[0],None,[256],[0,256])
 
 # Executa o filtro da mediana implementado pelo OpenCV
 init = time.time()
 medianBlur = medianaOpencv(img,tamMask)
 end = time.time()
 
 print "Tempo de execução do filtro da média do openCV: " + str(end-init) 
 # Calcula o histograma da imagem resultante
 h1 = cv2.calcHist([medianBlur],[0],None,[256],[0,256])
 
 # Executa o filtro da mediana implementado por mim.
 init = time.time()
 dst = minhaMediana(img,tamMask)
 end = time.time()

 print "Tempo de execução do meu filtro da média:       " + str(end-init)   
 # Calcula o histograma da imagem resultante
 h2 = cv2.calcHist([dst],[0],None,[256],[0,256])
 
 # Impressão dos resultados
 print "-------------------------------------------------------------"
 print "Igualdade entre a imagem original e a imagem mediana opencv:"
 print comparaHistogramas(h0,h1)
 print "\nIgualdade entre a imagem original e a imgem minha mediana:"
 print comparaHistogramas(h0,h2)
 print "\nIgualdade entre a imagem mediana opencv e minha mediana:"
 print comparaHistogramas(h1,h2)
 print "-------------------------------------------------------------"

 plotador(medianBlur,323,'Imagem medianBlur',0,0,0)
 plotador(dst,325,'Minha Mediana',0,0,0)
 plotador(img,321,'Original',0,0,0)
 plotador(h0,322,'Histograma',1,0,0)
 plotador(h1,324,'Histograma',1,0,0)
 plotador(h2,326,'Histograma',1,0,0) 
  
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# Teste da mediana em imagens com ruido                                        #
#------------------------------------------------------------------------------#

# Função que abre uma imagem, gera um ruído nela, e executa o filtro da 
# mediana na imagem com ruído
def mediana_ruido(imagem):
 img = cv2.imread(imagem,0)
 ruido = input("Entre com o nivel do ruido:")
 tamMask = input("Entre com o tamanho da mascara:")
 plotador(img,321,'Imagem Original',0,0,0)
 h0 = cv2.calcHist([img],[0],None,[256],[0,256])
 plotador(h0,322,'Histograma',1,0,0)
 
 rImg = geraRuido(img,ruido)
 plotador(rImg,323,'Imagem com Ruido',0,0,0)
 h1 = cv2.calcHist([rImg],[0],None,[256],[0,256])
 plotador(h1,324,'Histograma',1,0,0)

 medianBlur = medianaOpencv(rImg,tamMask)
 h2 = cv2.calcHist([medianBlur],[0],None,[256],[0,256])
 plotador(medianBlur,325,'Mediana aplicado em ruido',0,0,0)
 plotador(h2,326,'Histograma',1,0,0)

#------------------------------------------------------------------------------#
# Gerador de ruídos                                                            #
#------------------------------------------------------------------------------#

# Gera ruídos em uma imagem.
def geraRuido(img,nivel):
 a = np.array(img)
 b = np.array(img)
 cv2.randn(a,0,nivel)
 return a + b
  
# Função que gera 100 imagens com ruído e empilha elas em lotes de 10 imagens
def gerador_de_ruidos(imagem):
 
 img = cv2.imread(imagem,0)
 ruido = input("Entre com o nivel do ruido:")
 plotador(img,221,'Imagem Original',0,0,0)
 
 h0 = cv2.calcHist([img],[0],None,[256],[0,256])
 plotador(h0,222,'Histograma',1,0,0)
 
 rImg = geraRuido(img,ruido)
 plotador(rImg,223,'Imagem com Ruido',0,0,0)
 
 h1 = cv2.calcHist([rImg],[0],None,[256],[0,256])
 plotador(h1,224,'Histograma',1,0,0)
 plt.show()
 
 for j in xrange(0,10):
  imgs = []
  for i in xrange(0,10):
   rImg = geraRuido(img,ruido)
   imgs.append(rImg)
  
  s = imgs[0]/10
  for i in xrange(1,10):
   s = cv2.add(s,imgs[i]/10)
   
  plotador(s,121,'soma',0,0,0)
  h2 = cv2.calcHist([s],[0],None,[256],[0,256])
  plotador(h2,122,'Histograma',1,0,0)
  plt.show()
 
#------------------------------------------------------------------------------#
# Função principal                                                             #
#------------------------------------------------------------------------------#
if (__name__ == '__main__'):

 print "Entre com o número correspondente:"
 print "1 - exercicio 01 : Filtro Gaussiano"
 print "2 - exercicio 02 : Filtro Mediana"
 print "3 - gerador de ruídos"
 print "4 - teste mediana em imagens com ruido"

 ex = input("Escolha:")
 imagem = raw_input("Entre com o nome da imagem:")
 if (ex == 1):
  init = time.time()
  exercicio01(imagem)
  end = time.time()
  print "Tempo total de execução: " + str(end-init)
 elif (ex == 2):
  init = time.time()
  exercicio02(imagem)
  end = time.time()
  print "Tempo total de execução: " + str(end-init)
 elif (ex == 3):
  gerador_de_ruidos(imagem)
 elif (ex == 4):
  mediana_ruido(imagem)
 else:
  print "Escolha inválida! Digite 1,2,3 ou 4"
 plt.show() 
