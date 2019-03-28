import numpy as np
import cv2
from sys import exit
from os import path

CEND = '\33[0m'
CBOLD = '\33[1m'
CRED = '\33[31m'
CGREEN = '\33[32m'
CBLUE = '\33[34m'
NEG = '\033[5;37;40m'
NEGEND = '\033[0;37;40m'

def insertRedByBinary(binary_img, image, read_mode):
    if(read_mode == cv2.IMREAD_GRAYSCALE):
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    b, g, r = cv2.split(image)
    binary_img = binary_img.astype(np.uint8)
    cv2.bitwise_or(r, binary_img, r)
    cv2.bitwise_not(binary_img, binary_img)
    cv2.bitwise_and(b, binary_img, b)
    cv2.bitwise_and(g, binary_img, g)
    return cv2.merge((b, g, r))

def distanceMatCalculator(pixel, image, read_mode):
    if(read_mode == cv2.IMREAD_ANYCOLOR):
        img_aux = np.zeros((img.shape[0], img.shape[1], img.shape[2]))
        img_aux[:] = pixel  # solid color image made of the clicked color
        img_aux = img_aux - img
        b, g, r = cv2.split(img_aux)
        dist = np.zeros((img.shape[0], img.shape[1]))
        dist = (b**2 + g**2 + r**2)  # euclidian distance
        # threshold for the minimum distance required
        cv2.threshold(dist, (13**2)-1, 255, cv2.THRESH_BINARY_INV, dist)
        return dist
    elif(read_mode == cv2.IMREAD_GRAYSCALE):
        dist = np.zeros((img.shape[0], img.shape[1]))
        dist[:] = pixel
        dist = abs(dist - img)
        # threshold for the minimum distance required
        cv2.threshold(dist, (12), 255, cv2.THRESH_BINARY_INV, dist)
        return dist

def isImageOnGrayScale(image):
    b, g, r = cv2.split(image)
    aux1 = b - g
    aux2 = g - r
    cv2.bitwise_not(aux1, aux1)
    cv2.bitwise_not(aux2, aux2)
    if((aux1.all()) and (aux2.all())):
        return True
    else:
        return False

def mouseCallBack(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global clicked_flag
        clicked_flag = True
        dist = distanceMatCalculator(img[y][x], img, read_mode)
        img_aux = insertRedByBinary(dist,img,read_mode)
        if(read_mode == cv2.IMREAD_ANYCOLOR):
            print(CBOLD+"row: ", str(x), " column: ", str(y), CBLUE+" B: ",
                  str(img[y][x][0]), CGREEN+" G: ", str(img[y][x][1]), CRED+"R: ", str(img[y][x][2])+CEND)
        else:
            print(CBOLD+"row: ", str(x), " column: ",
                  str(y), NEG+"Gray: ", str(img[y][x])+CEND)
        cv2.namedWindow('Painted')
        cv2.imshow('Painted', img_aux)

if __name__ == "__main__":
    image_name = input("What is the image's name: ")
    print(image_name)
    if(not(path.isfile("./"+image_name))):
        exit("File doesn't exist or isn't in the local directory")
    img = cv2.imread(image_name, cv2.IMREAD_ANYCOLOR)
    if(isImageOnGrayScale(img)):
        print("Grayscale detected!")
        read_mode = cv2.IMREAD_GRAYSCALE
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        print("RGB")
        read_mode = cv2.IMREAD_ANYCOLOR
    cv2.namedWindow('Original')
    cv2.setMouseCallback('Original', mouseCallBack)
    cv2.imshow('Original', img)
    while(1):
        if cv2.waitKey(20) == 27:
            break
    cv2.destroyAllWindows()
