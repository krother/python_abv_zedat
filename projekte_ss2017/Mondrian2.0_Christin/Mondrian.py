# -*- coding: utf-8 -*-
"""
@author: Christin Jacobsen

Der Programmcode ist unter den Bedingungen der MIT-Lizenz nutzbar.
"""


import numpy as np
import PIL.Image as Image
from scipy.signal import convolve2d as conv
from random import randint



directory = "blume2.jpg"

params = {'threshold':        10000,
          'strichdicke':          4,
          'random_rechtecke': False}    

# Anmerkungen: 
# Theshold      ~ Schwellenwert der Farbauswahl
# Strichdicke   ~ Dicke der Begrenzungslinien (pixel)
# Boolean False ~ Teilungsverhältnisse orientieren sich zwingend am goldenen Schnitt
# Boolean True  ~ Rechtecke, deren Größen alleinig durch threshold-spezifische 
#                 Farbkontrastdichte-Funktion generiert werden. Je "feiner" das 
#                 Bild, je größer die RGB-Farbkontraste, desto kleiner die Rechtecke


def _get_grenzen(ar, a, b, c, d, rand = True):
    phi = (1+5**0.5)/2
    n, m = ar.shape
    if rand:
        senk_waag = bool(randint(0,1))
    else:
        senk_waag = (n>m)
    links_rechts = bool(randint(0,1))
    if senk_waag:
        if links_rechts:
            k = int(n/(1+1/phi))
        else:
            k = int(n/(phi+1))
        ar1 = (ar[:k,:], a, b, a+k, d)
        ar2 = (ar[k:,:], a+k, b, c, d)
    else:
        if links_rechts:
            k = int(m/(1+1/phi))
        else:
            k = int(m/(phi+1))
        ar1 = (ar[:,:k], a, b, c, b+k)
        ar2 = (ar[:,k:], a, b+k, c, d)
    return ar1, ar2
        

def do_something(arr, params):
    threshold = params['threshold']
    dicke = params['strichdicke']
    randiii = params['random_rechtecke']
    r, g, b = 1/3,1/3,1/3
    ar = arr[:,:,0]*r+arr[:,:,1]*g+arr[:,:,2]*b
    matrix = np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,-24,1,1],[1,1,1,1,1],[1,1,1,1,1]])
    contrast = np.abs(conv(ar, matrix, mode = 'same'))
    n, m = ar.shape
    
    rechteck_liste = [(contrast, 0, 0, n, m)]
    
    
    
    noch_rechtecke_uebrig = True
    while noch_rechtecke_uebrig:
        noch_rechtecke_uebrig = False
        k = len(rechteck_liste)
        print(k)
        for i in range(k):
            rechteck, a, b, c, d = rechteck_liste.pop(0)
            if (np.sum(rechteck)  > threshold) and ((c-a)>8*dicke) and ((d-b)>8*dicke):
                noch_rechtecke_uebrig = True
                ar1, ar2 = _get_grenzen(rechteck, a, b, c, d, randiii)
                rechteck_liste.append(ar1)
                rechteck_liste.append(ar2)
            else:
                rechteck_liste.append((rechteck, a, b, c, d))
    
    arrr = np.zeros(arr.shape)
    for rechteck, e, f, g, h in rechteck_liste:
        #print(a, b, c, d)
        a, b, c, d = e+dicke, f+dicke, g-dicke, h-dicke
        arr[a:c,b:d,:] = np.sum(arr[a:c,b:d,:], axis = (0,1))/(((c-a)*(d-b))+1)
        arrr[a:c,b:d,:] = 1
    arr *= arrr.astype('uint8')
    return arr
                
                
    

im = Image.open(directory)
imAr = np.array(im)

new_imAr = do_something(imAr, params)

new_im = Image.fromarray(new_imAr)

#new_im.show()

new_im.save("blume_mondrian.jpg")
