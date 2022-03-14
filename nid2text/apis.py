# nid2text/apis.py
import re

import easyocr
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NIDCardStorageModel
from .serializers import NIDCardStorageModelSerializer

registration_pattern = re.compile(r'\d{10,}')
birth_date_pattern = re.compile(r'\d\d\D\D\D\d\d\d\d')

ocr = PaddleOCR(use_angle_cls=True, lang='en')
reader = easyocr.Reader(['en'])
month_list = [
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec',
]

REGISTRATION_NUMBER_LENGTH = [10, 13, 17]


def birth_day_paddleocr_search(image_array):
    birthdate_map = {}
    nid2text = ''
    result_paddle_ocr = ocr.ocr(image_array, cls=True)
    for line in result_paddle_ocr:
        nid2text = nid2text + line[1][0].lower().replace(' ', '')

    birth_date_pattern_groups = birth_date_pattern.findall(nid2text)

    birthday = ''
    for pat in birth_date_pattern_groups:
        if pat[2:5] in month_list:
            birthday = pat
            break

    if len(birthday) == 9:
        birthdate_map = get_year_month_day(birthday)

    return birthdate_map


def get_registration_number_status(pattern_groups):
    registration_number = ''
    registration_status = 'failed'

    for pt in pattern_groups:
        if len(pt) in REGISTRATION_NUMBER_LENGTH:
            registration_number = pt
            registration_status = 'ok'

    return registration_number, registration_status


def get_birth_date_map(birth_date_groups):
    pattern = ''
    birth_date_map = {}
    status = 'failed'

    for pat in birth_date_groups:
        if pat[2:5] in month_list:
            pattern = pat
            break

    if len(pattern) == 9:
        status = 'ok'
        birth_date_map = get_year_month_day(pattern)

    return birth_date_map, status


def get_year_month_day(pattern):
    birth_day_map = {}

    birth_day_map['day'] = pattern[:2]
    birth_day_map['month'] = pattern[2:5]
    birth_day_map['year'] = pattern[5:]

    return birth_day_map


def registration_paddleocr_search(image_array):
    nid_number = ''
    nid2text = ''
    result_paddle_ocr = ocr.ocr(image_array, cls=True)
    for line in result_paddle_ocr:
        nid2text = nid2text + line[1][0].lower().replace(' ', '')
    registration_pattern_groups = registration_pattern.findall(nid2text)

    if registration_pattern_groups:
        for pt in registration_pattern_groups:
            if len(pt) in REGISTRATION_NUMBER_LENGTH:
                nid_number = pt

    return nid_number


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class NIDcardStorageListAPI(ListAPIView):
    queryset = NIDCardStorageModel.objects.all()
    serializer_class = NIDCardStorageModelSerializer
    pagination_class = StandardResultsSetPagination


class NID2TextAPI(APIView):
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
        serializer = NIDCardStorageModelSerializer(data=request.data)
        response = {}
        response.setdefault('status', 'ok')
        response.setdefault('data', {})
        response['data'].setdefault('birth_date', {})
        response['data'].setdefault('nid_number', {})

        if serializer.is_valid():
            instance = serializer.save()
            image_path = instance.image.path
            obj = Image.open(image_path).convert('L')
            image_array = np.array(obj)

            try:
                nid2text = ''

                result_easy_ocr = reader.readtext(image_array)

                for line in result_easy_ocr:
                    nid2text = nid2text + line[1].lower().replace(' ', '')

                response['data']['nid_to_text'] = nid2text

                registration_pattern_groups = registration_pattern.findall(
                    nid2text)
                birth_date_pattern_groups = birth_date_pattern.findall(
                    nid2text)

                rn, rs = get_registration_number_status(
                    registration_pattern_groups)

                if rs == 'ok':
                    response['data']['nid_number']['status'] = 'ok'
                else:
                    response['data']['nid_number']['status'] = 'failed'
                    nid_number = registration_paddleocr_search(image_array)
                    if nid_number:
                        response['data']['nid_number']['status'] = 'ok'
                        rn = nid_number
                response['data']['nid_number']['data'] = rn

                bm, bs = get_birth_date_map(birth_date_pattern_groups)
                if bs == 'ok':
                    response['data']['birth_date']['status'] = 'ok'
                else:
                    response['data']['birth_date']['status'] = 'failed'
                    birthdate = birth_day_paddleocr_search(image_array)
                    if birthdate:
                        response['data']['birth_date']['status'] = 'ok'
                        bm = birthdate

                response['data']['birth_date']['data'] = bm

                response['status'] = 'ok'

            except Exception as e:
                response['error'] = str(e)
                response['status'] = 'failed'
                response['data'] = {}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            return Response(response, status=status.HTTP_200_OK)
        else:
            response['status'] = 'failed'
            response['error'] = str(serializer.errors)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
