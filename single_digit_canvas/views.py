# from django.shortcuts import render
import sys

# import cv2
# import numpy as np
# from keras.preprocessing.image import img_to_array, load_img
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .process_data import image_to_digit
# from .apps import SingleDigitCanvasConfig
from .serializers import SingleDigitCanvasModelSerializer


class NurazDigitCanvasAPI(APIView):
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
        serializer = SingleDigitCanvasModelSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            try:
                instance = serializer.save()
                image_path = instance.image.path
                prediction = image_to_digit(image_path)
                response['digits'] = str(prediction)
            except Exception as e:
                the_type, the_value, the_traceback = sys.exc_info()
                response['error'] = str(the_value)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
