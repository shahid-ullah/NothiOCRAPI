# faceapp/api.py
# import cv2
import face_recognition
# from PIL import Image
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FaceCompareSerializer


class FaceCompare(APIView):
    """
    View to compare two faces.

    * Requires no authentication.
    * public API
    """

    def get(self, request, format=None):
        serializer = FaceCompareSerializer(data=request.data)
        if serializer.is_valid():
            nidcard = serializer.validated_data['nidcard_image']
            webcam = serializer.validated_data['webcam_image']
            try:
                nidcard = face_recognition.load_image_file(nidcard)
                webcam = face_recognition.load_image_file(webcam)

                nid_encoding_list = face_recognition.face_encodings(nidcard)
                webcam_encoding_list = face_recognition.face_encodings(webcam)

                # nidcard = cv2.rotate(nidcard, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # nid_encoding_list = face_recognition.face_encodings(nidcard)
                # webcam = cv2.rotate(webcam, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # webcam_encoding_list = face_recognition.face_encodings(webcam)

                # Handling special case, if nidcard image is not correct rotation
                # checked = 0
                # while not nid_encoding_list and checked < 3:
                #     nidcard = cv2.rotate(nidcard, cv2.ROTATE_90_COUNTERCLOCKWISE)
                #     nid_encoding_list = face_recognition.face_encodings(nidcard)
                #     checked = checked + 1

                # # Handling special case, if webcam image is not correct rotation
                # checked = 0
                # while not webcam_encoding_list and checked < 3:
                #     print(
                #         'webcam_encoding_list ',
                #         len(webcam_encoding_list),
                #         'checked ',
                #         checked + 1,
                #     )
                #     print()
                #     webcam = cv2.rotate(webcam, cv2.ROTATE_90_COUNTERCLOCKWISE)
                #     webcam_encoding_list = face_recognition.face_encodings(webcam)
                #     checked = checked + 1

                # webcam = cv2.rotate(webcam, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # webcam_encoding_list = face_recognition.face_encodings(webcam)

                if not nid_encoding_list or not webcam_encoding_list:
                    print('cannot detect any face')
                    return Response(
                        {'same': False, 'error': 'Cannot detect any face'},
                        status=status.HTTP_200_OK,
                    )

                nid_encoding = nid_encoding_list[0]
                webcam_encoding = webcam_encoding_list[0]

                results = face_recognition.compare_faces(
                    [nid_encoding], webcam_encoding
                )
                if results[0] == True:
                    return Response({'same': True}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'same': False, 'error': 'Not same people'},
                        status=status.HTTP_200_OK,
                    )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
