# nid2text/urls.py
from django.urls import path

from .apis import NID2TextAPI, NIDcardStorageListAPI

urlpatterns = [
    path('v2/nid_list/', NIDcardStorageListAPI.as_view(), name="v2_nid_list"),
    path('v2/nid2text/', NID2TextAPI.as_view(), name="v2_nid2text"),
]
