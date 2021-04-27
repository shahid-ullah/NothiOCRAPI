# reading_app/views.py
import os

import pytesseract as tess
from PIL import Image
from rest_framework import status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UploadImageSerializer

os.environ['OMP_THREAD_LIMIT'] = '1'


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
