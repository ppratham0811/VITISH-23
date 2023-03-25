from engine import detect, process, recognise, detect_belg, post_process
import cv2
import numpy
import argparse
import os
import glob
import sys
import easyocr
import time
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


parser = argparse.ArgumentParser()
parser.add_argument('--i', '-image', help="Input image path", type= str)
parser.add_argument('--v', '-video', help="Input video path", type= str)


args = parser.parse_args()
abs_path = os.path.dirname(sys.executable)


if args.i:
    start = time.time()
    try:
        os.mkdir('temp')
    except:
        files = glob.glob('tmp')
        for f in files:
            os.remove(f)
    
    input_image = cv2.imread(args.i)
    detection, crops, box1 = detect(input_image)

    i = 1
    for crop in crops:
        crop = process(crop)

        cv2.imwrite('temp/crop' + str(i) + '.jpg', crop)
        recognise('temp/crop' + str(i) + '.jpg', 'temp/crop'+str(i))
        #post_process('temp/crop' + str(i) + '.txt')
        i += 1
    cv2.imwrite('temp/detection.jpg', detection)
    image = cv2.imread('temp/detection.jpg')
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if(box1[0][1]<box1[2][1] and box1[0][0]<box1[2][0]):
        roi = image[box1[0][1]-20:box1[2][1]+20,box1[0][0]:box1[2][0]]
    elif(box1[0][1]>box1[2][1] and box1[0][0]<box1[2][0]):
        roi = image[box1[2][1]-20:box1[0][1]+20,box1[0][0]:box1[2][0]]
    elif(box1[0][1]<box1[2][1] and box1[2][0]>box1[0][0]):
        roi = image[box1[0][1]:box1[2][1],box1[2][0]:box1[0][0]]
    elif(box1[0][1]>box1[2][1] and box1[0][0]>box1[2][0]):
        roi = image[box1[2][1]:box1[0][1],box1[2][0]:box1[0][0]]
    #roi1 = cv2.resize(roi,(350,200))
    cv2.imshow("img",roi)
    
    custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- --psm 6'
    print(pytesseract.image_to_string(roi, config=custom_config))

    # reader = easyocr.Reader(["en"])
    # result = reader.readtext(roi)

    # res = [ele for sub in result for ele in sub if isinstance(ele, str)]
    #print("License Plate : "+ str(res))

    cv2.imshow("License Plate Detection",image)
    finish = time.time()
    print('Time processing >>>>>> '+ str(finish-start))
    cv2.waitKey(0)
    
    
elif args.v:
    cap = cv2.VideoCapture(args.v)

    # Check if camera opened successfully
    if cap.isOpened() == False:
        print("Error opening video stream or file")

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            frame, crop = detect(frame)
            # Display the resulting frame

            cv2.putText(frame, 'Press \'Q\' to exit !',(50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255), 2)
            cv2.imshow('Frame', frame)
            
            
            #roi = frame[box1[0][1]:box1[2][1],box1[0][0]:box1[2][0]]
            #roi1 = cv2.resize(roi,(350,200))
            #cv2.imshow("img",roi)
            # roi = frame[box1[0][1]-10:box1[2][1]+20,box1[0][0]-10:box1[2][0]+20]
            # #roi1 = cv2.resize(roi,(350,200))
            # cv2.imshow("img",roi)
    
            # custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- --psm 6'
            # print(pytesseract.image_to_string(roi, config=custom_config))


            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

else:
	print("--i : input image file path\n--v : input video file path")
	