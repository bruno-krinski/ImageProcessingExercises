#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno: Bruno Alexandre Krinski                                               #
# Matéria: Processamento de Imagens                                            #
# Exercício 03                                                                 #
#------------------------------------------------------------------------------#

import cv2
import numpy
from matplotlib import pyplot as plt

# Abre os cinco arquivos de imagens
imgs = []
for i in xrange(0,5):
    imgs.append(cv2.imread("imagem"+str(i)+".jpg"))

# Vetor para armazenar os histogramas da primeira imagem a qual será usada de base comparação das demais.
histogramas = []

# Faz o plot da primeira imagem.
plt.subplot(5,4,1)
plt.imshow(cv2.cvtColor(imgs[0], cv2.COLOR_BGR2RGB))
plt.title('Imagem 1')
plt.axis("off")

# Calcula o histograma azul
histogramaOrigem0 = cv2.calcHist([imgs[0]],[0],None,[256],[0,255])
cv2.normalize(histogramaOrigem0,histogramaOrigem0,0,1,cv2.NORM_MINMAX)
histogramas.append(histogramaOrigem0)

# Plota o histograma azul
plt.subplot(5,4,2)
plt.plot(histogramaOrigem0,color = 'b')
plt.xlim([0,255])

# Calcula o histograma verde
histogramaOrigem1 = cv2.calcHist([imgs[0]],[1],None,[256],[0,255])
cv2.normalize(histogramaOrigem1,histogramaOrigem1,0,1,cv2.NORM_MINMAX)
histogramas.append(histogramaOrigem1)

# Plota o histograma verde
plt.subplot(5,4,3)
plt.plot(histogramaOrigem1,color = 'g')
plt.xlim([0,255])

# Calcula o histograma vermelho
histogramaOrigem2 = cv2.calcHist([imgs[0]],[2],None,[256],[0,255])
cv2.normalize(histogramaOrigem2,histogramaOrigem2,0,1,cv2.NORM_MINMAX)
histogramas.append(histogramaOrigem2)

# Plota o histograma vermelho
plt.subplot(5,4,4)
plt.plot(histogramaOrigem2,color = 'r')
plt.xlim([0,255])


color = ('b','g','r')

# Para o restante das imagens
count = 5
for i in xrange(1,5):
    # Faz o plot dessas imagens
    plt.subplot(5,4,count)
    plt.imshow(cv2.cvtColor(imgs[i], cv2.COLOR_BGR2RGB))
    plt.title('Imagem '+str(i+1))
    plt.axis("off")
    count += 1
    print "Comparação da imagem 1 com a imagem " + str(i+1) + ":"
    for ch, col in enumerate(color):
               
        # Calcula o histograma para cada faixa de cor
        hist = cv2.calcHist([imgs[i]],[ch],None,[256],[0,255])
        cv2.normalize(hist, hist,0,1,cv2.NORM_MINMAX)
        
        # Compara os histogramas obtidos com os histogramas da imagem original
        sc = cv2.compareHist(histogramas[ch],hist,cv2.HISTCMP_CORREL)
        
        # Plota os histogramas 
        plt.subplot(5,4,count),plt.plot(hist,color = col)
        plt.xlim([0,255])
        count += 1
        
        # Imprime a diferença entre os histogramas
        print sc
        
plt.show()