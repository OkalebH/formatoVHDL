# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 18:09:45 2020
converts an image into a 24 fp image
@author: Okale
"""
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def float_convert(dec):
    #Decimal Number
    exp = dec[len(dec)-2:len(dec)+1]
    man = dec[4:8]
    exp = bin(127 + int(exp))
    exp = exp[2:len(exp)+1]
    if(len(exp) < 8):
        exp = str(0) + exp
    #convierte a binario
    dls = bin(int(man,16))
    #elimina el último bit
    dls = dls[2:len(dls)-1]
    fp = str(0) + str(exp) + str(dls)
    fp = hex(int(fp,2))
    
    return fp
    
def convert_img(img):
    img = np.array(img)
    img = img / np.max(img) #image normalization
    # plt.imshow(img,cmap="gray")
    # plt.show()
    img = img.reshape((img.size,))
    imSer = np.zeros((img.size,3))

    for i in range(img.size):
        if img[i] == 0.0:
            imSer[i][0] = 0
            imSer[i][1] = 0
            imSer[i][2] = 0
        elif img[i] == 1.0:
            imSer[i][0] = 63
            imSer[i][1] = 128
            imSer[i][2] = 0
        else:
            fp = float_convert(img[i].hex())
            imSer[i][0] = int(fp[2:4],16)
            imSer[i][1] = int(fp[4:6],16)
            imSer[i][2] = int(fp[6:8],16)
    
    imSer = np.array(imSer,dtype=np.uint8)
    
    return imSer

def int_convert(fp):
    img = np.array(fp)
    print(img.shape)
    #x = int(img.shape[0]/3)
    #img = np.reshape(fp,(x,3))
    x=100
    img_recibida = np.zeros((x,))
    for i in range(img.shape[0]):
        #Convierte a binario los datos recibidos
        byte_1 = bin(img[i][0])
        byte_2 = bin(img[i][1])
        byte_3 = bin(img[i][2])
        #Toma los bits de cada campo
        byte_1 = byte_1[2:len(byte_1)]
        byte_2 = byte_2[2:len(byte_2)]
        byte_3 = byte_3[2:len(byte_3)]
        #Añade los bits que le faltan a cada Byte
        byte_1 = complete_byte(byte_1)
        byte_2 = complete_byte(byte_2)
        byte_3 = complete_byte(byte_3)
        #concatena el número para que sean 24 bits
        fp = byte_1 + byte_2 + byte_3
        #separa los bits en sus respectivos campos
        s = fp[0]
        exp = fp[1:9]
        man = fp[9:len(fp)+1]
        #desbiasa el exponente
        exp = int(exp,2) - 127
        #Convierte la mantisa en una lista iterable
        man = list(man)
        man = np.array(man,dtype=np.float64)
        #Decimales de cada bit
        f_bits = [0.5,0.25,0.125,0.0625,0.03125,0.015625,0.0078125,0.00390625,0.001953125,0.0009765625,0.00048828125,0.000244140625,0.0001220703125,0.00006103515625,0.000030517578125]
        f_bits = np.array(f_bits)
        #Realiza la multiplicación de la mantisa con los decimales de cada bit
        n_dec = 1 + sum(f_bits * man)
        n_dec = n_dec * (2**exp)
        n_dec = round(n_dec * 255)
        if s == 1:
            n_dec = n_dec * -1
            
        img_recibida[i] = n_dec#int(n_dec)
        
    x = int(np.sqrt(x))
    img_recibida = np.reshape(img_recibida,(x,x))     
    return img_recibida      

def complete_byte(bits):
    if len(bits) < 8:
        while(len(bits)<8):
            bits = "0" + bits
        byte = bits
    else:
        byte = bits
            
    return byte
if "__main__" == __name__:
    #Lee imagen en formato de escala de grises
    img = cv.imread("img/diez.png",cv.IMREAD_GRAYSCALE)
    plt.imshow(img,cmap="gray")
    plt.show()
    #Convierte la imagen a un arreglo de numpy 
    img_serial = convert_img(img)
    
    x,y = img_serial.shape
    size = x*y
    hex_img = []
    num = ""
    for i in range(x):
        for j in range(y):
            num = num + hex(img_serial[i][j])[2:4]
        hex_img.append("x"+'"'+num+'"'+",")
        num = ""
            
    #Imagen en formato bytearray que será enviada por el puerto serial
    #img_serial = bytearray(img_serial)
    #img_serial = img.reshape((1,size))
    # ####
    # ###
    # ### AQUI VA EL CÖDIGO PARA ENVIAR LA IMAGEN
    # ###
    # ####
    img_recibida = int_convert(img_serial)
    np.save("matriz_float.npy",img_recibida)
    plt.imshow(img_recibida,cmap="gray")
    plt.show()

    # for pixel in img_serial:
        
    #     print(pixel)
        
    #Dentro del bytearray se introduce una lista y no un array
    #img_serial = int(img_serial)