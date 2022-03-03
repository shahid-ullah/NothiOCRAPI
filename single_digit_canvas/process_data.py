# single_digit_canvas/process_data.py
import cv2
import numpy as np
from imutils import contours
from keras.preprocessing.image import img_to_array, load_img

from digit_recognizer.apps import DigitRecognizerConfig

model = DigitRecognizerConfig.model_HCR


def image_to_digit(image_path):

    image = cv2.imread(image_path)
    image = image[
        70:-70,
    ]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=4)
    cnts, hierarchy = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    cnts, _ = contours.sort_contours(cnts, method="left-to-right")

    # avgCntArea = np.mean([cv2.contourArea(k) for k in cnts])

    Roi_number = 0
    for contour in cnts:
        # print(Roi_number, " is", cv2.contourArea(contour))
        if cv2.contourArea(contour) < 1000:
            continue
        mask = np.zeros(gray.shape, dtype="uint8")

        (x, y, w, h) = cv2.boundingRect(contour)
        hull = cv2.convexHull(contour)
        cv2.drawContours(mask, [hull], -1, 255, -1)
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        ROI = mask[y : y + h, x : x + w]

        cv2.imwrite('nuraz/ROI_{}.png'.format(Roi_number), ROI)

        Roi_number += 1

    prediction = []
    for i in range(0, Roi_number):
        image_path_test = 'nuraz/ROI_{}.png'.format(i)
        test_img = load_img(image_path_test, target_size=(50, 50))
        t = []
        test_img = img_to_array(test_img)
        t.append(test_img)
        test_img = np.array(t)
        predictions = model.predict(test_img[:])
        max = np.max(predictions)
        max = float(max) * 100
        max = "{:.2f}".format(max)

        pred = np.argmax(predictions, axis=1)
        pred = int(pred)

        map = {'value': pred, 'accuracy': max}
        prediction.append(map)

        # prediction.append(np.argmax(predictions, axis=1)[0])

    return prediction
