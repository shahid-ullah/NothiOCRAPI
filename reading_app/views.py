# reading_app/views.py

# sys import
import sys

# third-party import
# import cv2
import imageio
import pytesseract as tess
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from PIL import Image
from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

# local import
from .forms import ImageUploadForm
from .models import ImageUpload, UploadImage
from .serializers import UploadImageSerializer


def read_view(request):
    form=ImageUploadForm()
    text=None
    instance=None
    all_data=None
    language='ben'
    upload_msg=None
    if request.method == 'POST':
        form=ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
           data = form.save()
           path = data.image
           all_data = ImageUpload.objects.all()
           instance=ImageUpload.objects.get(id=data.id)
           update_path = instance.image.path
           img=Image.open(update_path)
           language=request.POST.get('language')
           print(language)
           text=tess.image_to_string(img,lang=language)
           instance.text=text
           instance.save()
           upload_msg=1


    return render(request,'home.html',{'form':form,'text':text,'current_img':instance,'all_img':all_data,'up_msg':upload_msg})


class OCRAPIView(APIView):
    """
    API: Return Image to text
    """
    parser_classes = [JSONParser, FormParser, MultiPartParser,]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request, *args, **kwargs):
        # breakpoint()
        serializer = UploadImageSerializer(data=request.data)

        if serializer.is_valid():
            try:
                instance = serializer.save()
                # Defining response dictionay
                response = {}
                image_path = instance.image.path
                image_object = Image.open(image_path)
                text=tess.image_to_string(image_object ,instance.language)
                response['text'] = str(text)
                instance.text = str(text)
                instance.save()
            except :
                the_type, the_value, the_traceback = sys.exc_info()
                response['error'] = str(the_value)
                instance.text = str(the_value)
                instance.save()
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
