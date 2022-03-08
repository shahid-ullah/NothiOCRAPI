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

registration_number_length = [10, 13, 17]


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
        response['data'].setdefault('registration', {})

        if serializer.is_valid():
            instance = serializer.save()
            image_path = instance.image.path
            obj = Image.open(image_path).convert('L')
            arr = np.array(obj)

            try:
                nid2text_easy_ocr = ''
                nid2text_paddleocr = ''

                # result_paddleocr = ocr.ocr(arr, cls=True)
                # for line in result_paddleocr:
                #     nid2text_paddleocr = nid2text_paddleocr + line[1][
                #         0
                #     ].lower().replace(' ', '')

                result_easy_ocr = reader.readtext(arr)
                for line in result_easy_ocr:
                    nid2text_easy_ocr = nid2text_easy_ocr + line[1].lower().replace(
                        ' ', ''
                    )

                # response['data']['nid_to_text'] = nid2text
                response['data']['nid_to_text_paddle'] = nid2text_paddleocr
                response['data']['nid_to_text_easy'] = nid2text_easy_ocr

                # registration_pattern_groups = registration_pattern.findall(
                #     nid2text_paddleocr
                # )
                # birth_date_pattern_groups = birth_date_pattern.findall(
                #     nid2text_paddleocr
                # )
                registration_pattern_groups = registration_pattern.findall(
                    nid2text_easy_ocr
                )
                birth_date_pattern_groups = birth_date_pattern.findall(
                    nid2text_easy_ocr
                )

                if registration_pattern_groups:
                    pattern = ''
                    for pt in registration_pattern_groups:
                        if len(pt) in registration_number_length:
                            pattern = pt

                    response['data']['registration']['status'] = 'ok'
                    response['data']['registration']['data'] = pattern
                else:
                    response['data']['registration']['status'] = 'failed'
                    response['data']['registration']['data'] = {}

                if birth_date_pattern_groups:

                    pattern = ''
                    for pat in birth_date_pattern_groups:
                        if pat[2:5] in month_list:
                            pattern = pat
                            break

                    if len(pattern) == 9:
                        birth_day_map = {}

                        birth_day_map['day'] = pattern[:2]
                        birth_day_map['month'] = pattern[2:5]
                        birth_day_map['year'] = pattern[5:]

                        response['data']['birth_date']['status'] = 'ok'
                        response['data']['birth_date']['data'] = birth_day_map
                    else:
                        response['data']['birth_date']['status'] = 'failed'
                        response['data']['birth_date']['data'] = {}

                else:
                    response['data']['birth_date']['status'] = 'failed'
                    response['data']['birth_date']['data'] = {}

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
