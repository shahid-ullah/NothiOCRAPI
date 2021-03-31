# from django.shortcuts import render
import cv2
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .apps import SingleDigitCanvasConfig
from .serializers import SingleDigitCanvasModelSerializer


class SingleDigitCanvasAPI(APIView):
    parser_classes = [
        JSONParser,
        FormParser,
        MultiPartParser,
    ]
    renderer_classes = [
        JSONRenderer,
        BrowsableAPIRenderer,
    ]

    def post(self, request, *args, **kwargs):
        model = SingleDigitCanvasConfig.model
        serializer = SingleDigitCanvasModelSerializer(data=request.data)
        # res = {}
        if serializer.is_valid():
            instance = serializer.save()
            path = instance.image.path
            image = cv2.imread(path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_new = gray[70:-70, :]
            gray_new = cv2.bitwise_not(gray_new)
            cv2.imwrite("test.jpg", gray_new)
            image_path_test = 'test.jpg'
            test_img = load_img(image_path_test, target_size=(50, 50))
            t = []
            test_img = img_to_array(test_img)
            t.append(test_img)
            test_img = np.array(t)
            predictions = model.predict(test_img[:])
            predict = np.argmax(predictions, axis=1)
            return Response({f'digit: {predict}'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
