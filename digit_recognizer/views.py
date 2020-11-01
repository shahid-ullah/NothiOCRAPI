import sys

from django.shortcuts import render
from PIL import Image
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONOpenAPIRenderer, JSONRenderer, BrowsableAPIRenderer

from .serializers import UploadImageSerializer
from .test_model import image_to_digits


# Create your views here.
class DigitRecognizerView(APIView):
    """
    API: Return Image to digit/digits
    """
    parser_classes = [JSONParser, FormParser, MultiPartParser,]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        # breakpoint()
        serializer = UploadImageSerializer(data=request.data)
        response = {}

        if serializer.is_valid():
            instance = serializer.save()
            image_path = instance.image.path
            try:
                prediction = image_to_digits(image_path)
                response['digits'] = str(prediction)
            except :
                the_type, the_value, the_traceback = sys.exc_info()
                response['error'] = str(the_value)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
