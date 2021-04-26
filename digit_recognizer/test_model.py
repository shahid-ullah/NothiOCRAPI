# digit_recognizer/test_model.py
import cv2
import numpy as np
from imutils import contours
from keras.preprocessing.image import img_to_array, load_img

from .apps import DigitRecognizerConfig


def image_to_digits(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=4)
    cnts, hierarchy = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    cnts, _ = contours.sort_contours(cnts, method="left-to-right")

    Roi_number = 0
    for contour in cnts:
        mask = np.zeros(gray.shape, dtype="uint8")

        (x, y, w, h) = cv2.boundingRect(contour)
        hull = cv2.convexHull(contour)
        cv2.drawContours(mask, [hull], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        ROI = mask[y : y + h, x : x + w]

        cv2.imwrite('roi/ROI_{}.png'.format(Roi_number), ROI)
        Roi_number += 1

    prediction = []
    # model = load_model('nuraz_single_canvas_50.h5')
    model = DigitRecognizerConfig.model_HCR
    for i in range(0, Roi_number):
        image_path_test = 'roi/ROI_{}.png'.format(i)
        test_img = load_img(image_path_test, target_size=(50, 50))
        t = []
        test_img = img_to_array(test_img)
        t.append(test_img)
        test_img = np.array(t)
        predictions = model.predict(test_img[:])
        prediction.append(np.argmax(predictions, axis=1)[0])

    return prediction
