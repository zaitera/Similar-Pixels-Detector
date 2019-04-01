import cv2
import numpy as np
from sys import exit
from os import path
import time

CEND    = '\33[0m'
CBOLD   = '\33[1m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CBLUE   = '\33[34m'
NEG = '\033[5;37;40m'
NEGEND = '\033[0;37;40m'

def insertRedByBinary(binary_img, image, read_mode):
    if(read_mode == cv2.IMREAD_GRAYSCALE):
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    b, g, r = cv2.split(image)
    binary_img = binary_img.astype(np.uint8)
    cv2.bitwise_or(r, binary_img, r)
    cv2.bitwise_not(binary_img,binary_img)
    cv2.bitwise_and(b, binary_img, b)
    cv2.bitwise_and(g, binary_img, g)
    return cv2.merge((b,g,r))

def distanceMatCalculator(pixel,image, read_mode):
    if(read_mode == cv2.IMREAD_ANYCOLOR):
        img_aux = np.zeros((img.shape[0],img.shape[1],img.shape[2]))
        img_aux[:] = pixel #solid color image made of the clicked color
        img_aux = img_aux - img  
        b, g, r = cv2.split(img_aux)
        dist = np.zeros((img.shape[0],img.shape[1]))
        dist = (b**2 + g**2 + r**2) #euclidian distance
        cv2.threshold(dist,(13**2)-1,255,cv2.THRESH_BINARY_INV,dist) #threshold for the minimum distance required
        return dist
    elif(read_mode == cv2.IMREAD_GRAYSCALE):             
        dist = np.zeros((img.shape[0],img.shape[1]))
        dist[:] = pixel
        dist = abs(dist - img)        
        cv2.threshold(dist,(12),255,cv2.THRESH_BINARY_INV,dist) #threshold for the minimum distance required
        return dist

def mouseCallBack(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:    
        global clicked_flag
        global current_pixel_reference
        clicked_flag = True
        current_pixel_reference = img[y][x]
        if(read_mode == cv2.IMREAD_ANYCOLOR):
            print(CBOLD+"row: ",str(x), " column: ", str(y), CBLUE+" B: ",str(img[y][x][0]),CGREEN+" G: ",str(img[y][x][1]),CRED+"R: ",str(img[y][x][2])+CEND)
        else:    
            print(CBOLD+"row: ",str(x), " column: ", str(y), NEG+"Gray: ",str(img[y][x])+CEND)
        pass

def isImageInGrayScale(image):
    b, g, r = cv2.split(image)
    aux1 = b - g
    aux2 = g - r
    cv2.bitwise_not(aux1, aux1)
    cv2.bitwise_not(aux2, aux2)
    if((aux1.all()) and (aux2.all())):
        return True
    else:
        return False

def init():
    webcam = False
    file_name = None
    cam_number = None
    file_type = input("For Video press 1 and for image press 2: ")
    print(file_type)
    if(not(file_type == "1" or file_type == "2")):
        exit("Invalid option")  
    if file_type == "1":
        aux = input("For webcam press 1 for a specific video file press 2: ")
        if aux == "1":
            webcam = True
            cam_number = int(input("Enter the webcam camera number as your system identifies it: "),10)
        else:
            webcam = False
        pass
    if(not(webcam)):
        file_name = input("What is the file's name: ")
        print(file_name)
        if(not(path.isfile("./"+file_name))):
            exit("File doesn't exist or isn't in the local directory")
    return file_type, file_name, webcam, cam_number

if __name__ == "__main__":
    file_type, file_name, webcam, cam_number = init()
    if(file_type == "1"):
        if webcam :
            cap = cv2.VideoCapture(cam_number)    
        else:
            cap = cv2.VideoCapture(file_name)    
        
        flag, img = cap.read()
        if (not (flag)):
            exit("Error while reading the video, try again.")
    else:
        img = cv2.imread(file_name, cv2.IMREAD_ANYCOLOR)
    if(isImageInGrayScale(img)):
        print("Grayscale detected!")
        read_mode = cv2.IMREAD_GRAYSCALE
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        print("RGB")
        read_mode = cv2.IMREAD_ANYCOLOR
    cv2.namedWindow('Original')
    cv2.setMouseCallback('Original',mouseCallBack)
    if(file_type == "2"):
        cv2.imshow('Original', img)
    clicked_flag = False
    while True:
        if(file_type == "1"):
            flag, img = cap.read()
            if flag:
                # The frame is ready and already captured
                if(read_mode == cv2.IMREAD_GRAYSCALE):
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imshow('Original', img)           
                pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                if(clicked_flag):
                    distance = distanceMatCalculator(current_pixel_reference, img, read_mode)
                    result = insertRedByBinary(distance, img, read_mode)
                    cv2.namedWindow('Painted')
                    cv2.imshow('Painted', result)
                #print (str(pos_frame)+" frames ", clicked_flag)
            else:
                # The next frame is not ready, so we try to read it again
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
                print ("frame is not ready")
                # It is better 1to wait for a while for the next frame to be ready
                cv2.waitKey(10)
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                # If the number of captured frames is equal to the total number of frames,
                # we stop
                break
        if(file_type == "2" and clicked_flag):
            start = time.time()
            distance = distanceMatCalculator(current_pixel_reference, img, read_mode)
            result = insertRedByBinary(distance, img, read_mode)
            end = time.time()
            clicked_flag = False
            print(end - start)
            cv2.namedWindow('Painted')
            cv2.imshow('Painted',result)
        if cv2.waitKey(25) == 27:
            break
