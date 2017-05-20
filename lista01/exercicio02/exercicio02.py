#coding: utf-8
#!/usr/bin/python

#------------------------------------------------------------------------------#
# Aluno: Bruno Alexandre Krinski                                               #
# Matéria: Processamento de Imagens                                            #
# Exercício 02                                                                 #
#------------------------------------------------------------------------------#

import sys
import numpy
import cv2

if (__name__ == '__main__'):

 image = cv2.imread('wdg4.png',0)
 rows,cols = image.shape

 image2 = cv2.imread('wdg5.png',0)
 image2 = image2[0:image.shape[0],0:image.shape[1]]
 lim = 120
 for i in range(0,rows):
  for j in range(0,cols):
   if (image.item(i,j) > lim):
    image.itemset((i,j),255)
   else:
    image.itemset((i,j),0)
   if (image2.item(i,j) > lim):
    image2.itemset((i,j),255)
   else:
    image2.itemset((i,j),0)

 pts1 = numpy.float32([[126,218], [202,70 ], [412,189]])
 pts2 = numpy.float32([[412,172], [329,309], [134,159]])

 M = cv2.getAffineTransform(pts1,pts2)

 dst = cv2.warpAffine(image,M,(cols,rows),borderValue=255)

 count = 0
 for i in range(0, rows):
  for j in range(0, cols):
   if (image2.item(i,j) - dst.item(i,j)) != 0:
    count += 1

 print "A imagem tem " , count , "pixels diferentes"

 final = cv2.addWeighted(image2,1,dst,0.3,0)

 cv2.imshow('image',dst)
 cv2.waitKey(0)
 cv2.destroyAllWindows()
 
 cv2.imshow('image',image2)
 cv2.waitKey(0)
 cv2.destroyAllWindows()

 cv2.imshow('image',final)
 cv2.waitKey(0)
 cv2.destroyAllWindows()
