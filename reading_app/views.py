# reading_app/views.py
import os
import re

import pytesseract as tess
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from PIL import Image
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ImageUploadForm
from .serializers import UploadImageSerializer

os.environ['OMP_THREAD_LIMIT'] = '1'

header1_regex = re.compile(r'গণপ্রজাতন্ত্(.*)')
header2_regex = re.compile(r'Government(.*)')
header3_regex = re.compile(r'NATIONA(.*)')


name_eng_regex = re.compile(r'Name(.*)')
name_bng_regex = re.compile(r'নাম(.*)')
# date_of_birth_regex = re.compile(r'Date of Birth:\s*\d*\s*\w*\s*\d*')
date_of_birth_regex = re.compile(r'Date(.*)')
id_no_regex = re.compile(r'ID\s*NO:\s*\d*')
father_name_regx = re.compile(r'পিতা(.*)')
mother_name_regx = re.compile(r'মাতা(.*)')

footer1_regex = re.compile(r'এই(.*)')
footer2_regex = re.compile(r'কোথা(.*)')

footer3_regex = re.compile(r'ঠিকানা(.*)')
footer4_regex = re.compile(r'ঢাকা(.*)')


def I2TNID(request):
    """
    NID Image to Text Converter.
    """
    if request.method == "GET":
        form = ImageUploadForm(initial={'language': 'ben+eng'})

    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            try:
                image_path = instance.image.path
                image_object = Image.open(image_path)
                text = tess.image_to_string(image_object, instance.language)
                not_matching_object, response = extract_nid_info(str(text))
            except Exception as e:
                response = ""
                return HttpResponseBadRequest()
            return render(
                request,
                'i2tnid.html',
                context={
                    'form': form,
                    'display': True,
                    'response': response,
                    'not_matching_object': not_matching_object,
                },
            )

    return render(request, 'i2tnid.html', context={'form': form, 'display': False})


class OCRAPIView(APIView):
    """
    API: Return Image to text
    """

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
        # breakpoint()
        serializer = UploadImageSerializer(data=request.data)
        response = {}

        if serializer.is_valid():
            instance = serializer.save()
            try:
                image_path = instance.image.path
                image_object = Image.open(image_path)
                text = tess.image_to_string(image_object, instance.language)
                response['text'] = str(text)
                instance.save()
            except Exception as e:
                response['error'] = str(e)
                instance.text = str(e)
                instance.save()
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def extract_nid_info(text):

    not_matching_object = 0
    # Search Text
    header1_mo = header1_regex.search(text)
    if header1_mo:
        header1 = header1_mo.group()
    else:
        header1 = ''
        not_matching_object += 1

    header2_mo = header2_regex.search(text)
    if header1_mo:
        header2 = header2_mo.group()
    else:
        header2 = ''
        not_matching_object += 1

    header3_mo = header3_regex.search(text)
    if header3_mo:
        header3 = header3_mo.group()
    else:
        header3 = ''
        not_matching_object += 1

    name_bng_mo = name_bng_regex.search(text)
    if name_bng_mo:
        name_bng = name_bng_mo.group()
    else:
        name_bng = ''
        not_matching_object += 1

    name_eng_mo = name_eng_regex.search(text)
    if name_eng_mo:
        name_eng = name_eng_mo.group()
    else:
        name_eng = ''
        not_matching_object += 1

    father_name_mo = father_name_regx.search(text)
    if father_name_mo:
        father_name = father_name_mo.group()
    else:
        father_name = ''
        not_matching_object += 1

    mother_name_mo = mother_name_regx.search(text)
    if mother_name_mo:
        mother_name = mother_name_mo.group()
    else:
        mother_name = ''
        not_matching_object += 1

    date_of_birth_mo = date_of_birth_regex.search(text)
    if date_of_birth_mo:
        date_of_birth = date_of_birth_mo.group()
    else:
        date_of_birth = ''
        not_matching_object += 1

    id_no_mo = id_no_regex.search(text)
    if id_no_mo:
        id_no = id_no_mo.group()
    else:
        id_no = ''
        not_matching_object += 1

    footer1_mo = footer1_regex.search(text)
    if footer1_mo:
        footer1 = footer1_mo.group()
    else:
        footer1 = ''
        not_matching_object += 1

    footer2_mo = footer2_regex.search(text)
    if footer2_mo:
        footer2 = footer2_mo.group()
    else:
        footer2 = ''
        not_matching_object += 1

    footer3_mo = footer3_regex.search(text)
    if footer3_mo:
        footer3 = footer3_mo.group()
    else:
        footer3 = ''
        not_matching_object += 1

    footer4_mo = footer4_regex.search(text)
    if footer4_mo:
        footer4 = footer4_mo.group()
    else:
        footer4 = ''
        not_matching_object += 1

    dic = {
        'header1': header1,
        'header2': header2,
        'header3': header3,
        'name_bng': name_bng,
        'name_eng': name_eng,
        'father_name': father_name,
        'mother_name': mother_name,
        'date_of_birth': date_of_birth,
        'id_no': id_no,
        'footer1': footer1,
        'footer2': footer2,
        'footer3': footer3,
        'footer4': footer4,
    }

    return not_matching_object, dic


# def read_view(request):
#     form = ImageUploadForm()
#     text = None
#     instance = None
#     all_data = None
#     language = 'ben'
#     upload_msg = None
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)

#         if form.is_valid():
#             data = form.save()
#             # path = data.image
#             all_data = ImageUpload.objects.all()
#             instance = ImageUpload.objects.get(id=data.id)
#             update_path = instance.image.path
#             img = Image.open(update_path)
#             language = request.POST.get('language')
#             print(language)
#             text = tess.image_to_string(img, lang=language)
#             instance.text = text
#             instance.save()
#             upload_msg = 1

#     return render(
#         request,
#         'home.html',
#         {
#             'form': form,
#             'text': text,
#             'current_img': instance,
#             'all_img': all_data,
#             'up_msg': upload_msg,
#         },
#     )
