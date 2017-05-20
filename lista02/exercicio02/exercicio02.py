#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno: Bruno Alexandre Krinski                                               #
# Matéria: Processamento de Imagens                                            #
# Exercício 02                                                                 #
#------------------------------------------------------------------------------#

import cv2
import math
import numpy as np 
from matplotlib import pyplot as plt

# Leitura do nome da imagem e o tamanho no eixo X e no eixo Y da janela de equalização
entrada = raw_input("Entre com o nome da imagem: \n")
tamX = input("Entre com o tamanho da janela no eixo X: \n")
tamY = input("Entre com o tamanho da janela no eixo Y: \n")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Leitura da imagem de entrada
imagemEntrada = cv2.imread(entrada,0)

# Calculo do histograma da imagem de entrada
histogramaImagemEntrada = cv2.calcHist([imagemEntrada],[0],None,[256],[0,256])

# Normalização do histograma da imagem de entrada
cv2.normalize(histogramaImagemEntrada, histogramaImagemEntrada,0,1,cv2.NORM_MINMAX)

# Plot do histograma normalizado da imagem de entrada
plt.subplot(242)
plt.plot(histogramaImagemEntrada,'gray')
plt.title('Imagem Original')
plt.xlim([0,255])
plt.ylim([0,1])

# Plot da imagem resultante
plt.subplot(241),plt.imshow(imagemEntrada, 'gray')
plt.title('Imagem Original')
plt.axis("off")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Equalização da imagem de entrada
imagemEntradaEqualizada = cv2.equalizeHist(imagemEntrada)

# Calculo do histograma da imagem de entrada equalizada
histogramaImagemEntradaEqualizada = cv2.calcHist([imagemEntradaEqualizada],[0],None,[256],[0,256])

# Normalização do histograma da imagem de entrada equalizada
cv2.normalize(histogramaImagemEntradaEqualizada, histogramaImagemEntradaEqualizada,0,1,cv2.NORM_MINMAX)

# Plot do histograma normalizado da imagem de entrada equalizada
plt.subplot(244)
plt.plot(histogramaImagemEntradaEqualizada,'gray')
plt.title('Equalizacao Global')
plt.xlim([0,255])
plt.ylim([0,1])

# Plot da imagem resultante
plt.subplot(243)
plt.imshow(imagemEntradaEqualizada, 'gray')
plt.title('Equalizacao Global')
plt.axis("off")

# Salva a imagem equalizada em um arquivo
cv2.imwrite('Equalização.jpg',imagemEntradaEqualizada)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Equalização da imagem de entrada através do método de clahe
equalizacaoClahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(tamY,tamX))
imagemEntradaEqualizadaClahe = equalizacaoClahe.apply(imagemEntrada)

# Calculo do histograma da imagem de entrada equalizada através do método de clahe
histogramaImagemEntradaEqualizadaClahe = cv2.calcHist([imagemEntradaEqualizadaClahe],[0],None,[256],[0,256])

# Normalização do histograma da imagem de entrada equalizada através do método de clahe
cv2.normalize(histogramaImagemEntradaEqualizadaClahe, histogramaImagemEntradaEqualizadaClahe,0,1,cv2.NORM_MINMAX)

# Plot do histograma normalizado da imagem de entrada equalizada através do método de clahe
plt.subplot(246)
plt.plot(histogramaImagemEntradaEqualizadaClahe,'gray')
plt.title('Equalicacao de Clahe')
plt.xlim([0,255])
plt.ylim([0,1])

# Plot da imagem resultante
plt.subplot(245)
plt.imshow(imagemEntradaEqualizadaClahe, 'gray')
plt.title('Equalicacao de Clahe')
plt.axis("off")

# Salva a imagem equalizada através do método de clahe em um arquivo
cv2.imwrite('Clahe.jpg',imagemEntradaEqualizadaClahe)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Calculo da quantidade de pixels nos eixos X e Y da imagem de entrada
axisY = imagemEntrada.shape[0]
axisX = imagemEntrada.shape[1]

# Calculo do tamanho das bordas que guardarão os pixels replicados das bordas da imagem de entrada
aumentoX1 = int(round(tamX/2))
if (tamX % 2 != 0):
    aumentoX2 = aumentoX1
else:
    aumentoX2 = aumentoX1 - 1

aumentoY1 = int(round(tamY/2))
if (tamY % 2 != 0): 
    aumentoY2 = aumentoY1
else:
    aumentoY2 = aumentoY1 - 1

print "Valor Eixo X: " + str(axisX)
print "Valor Eixo Y: " + str(axisY)

print "A imagem aumentará " + str(aumentoX2) + " para a esquerda!"
print "A imagem aumentará " + str(aumentoX1) + " para a direita!"
print "A imagem aumentará " + str(aumentoY2) + " para cima!"
print "A imagem aumentará " + str(aumentoY1) + " para baixo!"

# Aumenta a borda da imagem e espelha os pixels da borda para fora
imagemAumentada = cv2.copyMakeBorder(imagemEntrada,aumentoY2,aumentoY1,aumentoX2,aumentoX1,cv2.BORDER_REFLECT_101)

# Calcula o novo Eixo X e Y da imagem
newAxisY = imagemAumentada.shape[0]
newAxisX = imagemAumentada.shape[1]

print "Valor do Eixo X imagem aumentada: " + str(newAxisX)
print "Valor do Eixo Y imagem aumentada: " + str(newAxisY)

# Percorre a imagem com os pixels da borda espelhados para fora.
# Para cada pixel, calcula a equalização da janela e atribui o pixel do meio da janela equalizada no pixel do meio da janela na imagem.
# Não há necessidade de tratar os pixels das bordas pois, com eles espelhados nas bordas da imagem, ao percorrer a imagem com a janela
# esses pixels são utilizados automaticamente pra o calculo da equalização dos pixels da borda da imagem original.
for y in xrange(0,newAxisY-tamY):
    for x in xrange(0,newAxisX-tamX):
        imagemAumentada[y+int(tamY/2),x+int(tamX/2)] = cv2.equalizeHist(imagemAumentada[y:y+tamY,x:x+tamX])[int(tamY/2),int(tamX/2)]

# Recorta a imagem, retirando os pixels espelhados da imagem.
imagemAumentada = imagemAumentada[aumentoY2:newAxisY-aumentoY1,aumentoX2:newAxisX-aumentoX1]

# Calculo do histograma da imagem de entrada equalizada através do método local
histogramaImagemEntradaEqualizadaLocal = cv2.calcHist([imagemAumentada],[0],None,[256],[0,256])

# Normalização do histograma da imagem de entrada equalizada através do método local
cv2.normalize(histogramaImagemEntradaEqualizadaLocal, histogramaImagemEntradaEqualizadaLocal,0,1,cv2.NORM_MINMAX)

# Plot do histograma normalizado da imagem de entrada equalizada através do método local     
plt.subplot(248)
plt.plot(histogramaImagemEntradaEqualizadaLocal,'gray')
plt.title('Equalizacao Local')
plt.xlim([0,255])
plt.ylim([0,1])

# Plot da imagem resultante
plt.subplot(247),plt.imshow(imagemAumentada, 'gray')
plt.title('Equalizacao Local')
plt.axis("off")

# Salva a imagem equalizada através do método local em um arquivo
cv2.imwrite('out.jpg',imagemAumentada)

# Exibe as imagens plotadas
plt.show()