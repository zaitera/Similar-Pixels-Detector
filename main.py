import cv2
from sys import exit
from os import path

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CBLUE   = '\33[34m'
NEG = '\033[5;37;40m'
NEGEND = '\033[0;37;40m'

def mouseCallBack(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:   
        if(read_mode == cv2.IMREAD_ANYCOLOR):
            print(CBOLD+"row: ",str(y), " column: ", str(x), CBLUE+" B: ",str(img[y][x][0]),CGREEN+" G: ",str(img[y][x][1]),CRED+"R: ",str(img[y][x][2])+CEND)
        elif(read_mode == cv2.IMREAD_GRAYSCALE):             
            print(CBOLD+"row: ",str(y), " column: ", str(x), NEG+"Gray: ",str(img[y][x])+CEND)   

if __name__ == "__main__":
    image_name = input("What's the image's name: ")
    print(image_name)
    if(not(path.isfile("./"+image_name))):
        exit("File doesn't exist")
    read_mode = input("For RGB click 1, for GrayScale click 2: ")
    if(read_mode == "1"):
        read_mode = cv2.IMREAD_ANYCOLOR
    elif (read_mode == "2"):
        read_mode = cv2.IMREAD_GRAYSCALE
    else:
        exit("Invalid Mode")
    print(read_mode)    
    img = cv2.imread(image_name, read_mode)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',mouseCallBack)
    cv2.imshow('image',img)
    while(1):        
        if cv2.waitKey(20) == 27:
            break
    cv2.destroyAllWindows()