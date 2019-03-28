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
        if(read_mode == cv2.IMREAD_ANYCOLOR):
            print(CBOLD+"row: ", str(y), " column: ", str(x), CBLUE+" B: ",
                  str(img[y][x][0]), CGREEN+" G: ", str(img[y][x][1]), CRED+"R: ", str(img[y][x][2])+CEND)
        elif(read_mode == cv2.IMREAD_GRAYSCALE):
            print(CBOLD+"row: ", str(y), " column: ",
                  str(x), NEG+"Gray: ", str(img[y][x])+CEND)

if __name__ == "__main__":
    image_name = input("What's the image's name: ")
    print(image_name)
    if(not(path.isfile("./"+image_name))):
        exit("File doesn't exist")
    img = cv2.imread(image_name, cv2.IMREAD_ANYCOLOR)
    if(isImageOnGrayScale(img)):
        print("Grayscale detected!")
        read_mode = cv2.IMREAD_GRAYSCALE
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        print("RGB")
        read_mode = cv2.IMREAD_ANYCOLOR
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', mouseCallBack)
    cv2.imshow('image', img)
    while(1):
        if cv2.waitKey(20) == 27:
            break
    cv2.destroyAllWindows()
