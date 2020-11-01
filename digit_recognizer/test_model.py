import os
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import MobileNetV2
from keras.layers import AveragePooling2D
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense,MaxPool2D
from keras.layers import Input
from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import model_from_json,load_model
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import glob
import numpy as np

import cv2
import imutils
import argparse
import matplotlib.pyplot as plt
from .apps import DigitRecognizerConfig


def image_to_digits(image_path):
    image = cv2.imread(image_path)
    image = imutils.resize(image,width=320)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    blackhat = cv2.morphologyEx(gray,cv2.MORPH_BLACKHAT,kernel)

    _,thresh = cv2.threshold(blackhat,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

    def get_contour_precedence(contour, cols):
        tolerance_factor = 100
        origin = cv2.boundingRect(contour)
        return ((origin[1] // tolerance_factor) * tolerance_factor * cols + origin[0])

    (cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts.sort(key=lambda cnts:get_contour_precedence(cnts, thresh.shape[1]))
    avgCntArea = np.mean([cv2.contourArea(k) for k in cnts])
    digits = []
    boxes = []

    # model=load_model('abcde.h5')

    predicted_result=[]
    Roi_number=0
    for (i,c) in enumerate(cnts):
        if cv2.contourArea(c)<avgCntArea/10:
            continue
        mask = np.zeros(gray.shape,dtype="uint8")
    
        (x,y,w,h) = cv2.boundingRect(c)
        hull = cv2.convexHull(c)
        cv2.drawContours(mask,[hull],-1,255,-1)
        mask = cv2.bitwise_and(thresh,thresh,mask=mask)
        digit = mask[y-8:y+h+8,x-8:x+w+8]
    #     digit = cv2.resize(digit,(28,28))
        ROI = mask[y:y+h, x:x+w+10]
        #ROI=ROI.reshape(1,20,20,1)
        # print(ROI.shape)
        dim=(20,20)
        resized = cv2.resize(ROI, dim, interpolation = cv2.INTER_AREA)
        resized=resized.reshape(1,20,20,1)
        # predictions=model.predict(resized[:2])
        predictions=DigitRecognizerConfig.model_HDR.predict(resized[:2])
        f_predictions = np.argmax(predictions,axis=1)
        f_predictions = f_predictions[0]
        predicted_result.append(f_predictions)
        Roi_number+=1

    return predicted_result
        

    print(predicted_result)


