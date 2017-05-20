#coding: utf-8 
#!/usr/bin/python 

#------------------------------------------------------------------------------# 
# Aluno: Bruno Alexandre Krinski                                               # 
# Matéria: Processamento de Imagens                                            # 
# Exercicio 04                                                                 # 
#------------------------------------------------------------------------------#

import cv2 
import math 
import time 
import numpy as np 
from matplotlib import pyplot as plt

#------------------------------------------------------------------------------# 
# Função principal                                                             # 
#------------------------------------------------------------------------------# 
if (__name__ == '__main__'):
	
	img = cv2.imread('clown.jpg',0)
	y,x = img.shape
	fshift1 = np.fft.fftshift(np.fft.fft2(img))
	magnitude_spectrum = 20*np.log(np.abs(fshift1))

	mOriginal = np.array(magnitude_spectrum)
	
	plt.subplot(141)
	plt.imshow(img,cmap='gray')
	plt.title('Imagem Original')
	plt.xticks([])
	plt.yticks([])

	plt.subplot(142)
	plt.imshow(mOriginal,cmap='gray')
	plt.title('Espectro de Magnitude')
	plt.xticks([])
	plt.yticks([])	
	
	cv2.circle(magnitude_spectrum,(190,122), 8, (0,0,0),-1)
	cv2.line(magnitude_spectrum,(190, 122),(x,122),(0,0,0),1)
	cv2.line(magnitude_spectrum,(190,0),(190, 122),(0,0,0),1)

	cv2.circle(magnitude_spectrum,(105,172), 8, (0,0,0),-1)
	cv2.line(magnitude_spectrum,(0, 172),(105,172),(0,0,0),1)
	cv2.line(magnitude_spectrum,(105,172),(105, y),(0,0,0),1)

	cv2.circle(magnitude_spectrum,(170,160), 8, (0,0,0),-1)
	#cv2.line(magnitude_spectrum,(170, 160),(x,160),(0,0,0),1)
	#cv2.line(magnitude_spectrum,(170,0),(170, 160),(0,0,0),1)

	cv2.circle(magnitude_spectrum,(126,134), 8, (0,0,0),-1)
	#cv2.line(magnitude_spectrum,(126, 134),(x,134),(0,0,0),1)
	#cv2.line(magnitude_spectrum,(126,0),(126, 134),(0,0,0),1)
 
	vt = np.exp(magnitude_spectrum/20)
	angulo = np.angle(fshift1)
	volta = (vt*np.sin(angulo)*1j) + (vt*np.cos(angulo))

	f_ishift = np.fft.ifftshift(volta)
	img_back = np.fft.ifft2(f_ishift)
	img_back = np.abs(img_back)

	plt.subplot(143)
	plt.imshow(img_back,cmap='gray')
	plt.title('Imagem Resultado')
	plt.xticks([])
	plt.yticks([])

	plt.subplot(144)
	plt.imshow(magnitude_spectrum,cmap='gray')
	plt.title('Novo Espectro de Magniture')
	plt.xticks([])
	plt.yticks([])

	plt.show()
