#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno: Bruno Alexandre Krinski                                               #
# Matéria: Processamento de Imagens                                            #
# Exercício 01                                                                 #
#------------------------------------------------------------------------------#

import cv2
import numpy as np
from matplotlib import pyplot as plt

imagemNome = raw_input("Entre com o nome da imagem:\n")

img = cv2.imread(imagemNome)

color = ('b','g','r')

for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.subplot(221),plt.plot(histr,color = col),plt.xlim([0,255])
plt.subplot(222),plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()    
