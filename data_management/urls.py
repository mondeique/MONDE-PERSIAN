"""data_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from category_data.views import *

app_name = 'category'

urlpatterns = [
    path('api/import/original-images', OriginalImageCreateAPIView.as_view(), name='import_image'),
    path('api/home', HomeRetrieveAPIView.as_view(), name='home'),
    #TODO : 한번에 보는게 좋을것 같아서 수정함
    path('api/worker', WorkerManageRetrieveAPIView.as_view(), name='worker'),
    path('api/boxing/<int:original_image_id>', BoxingRetrieveAPIView.as_view()),
    path('api/colorlabeling/<int:cropped_image_id>', ColorLabelingRetrieveAPIView.as_view()),
    path('api/shapelabeling/<int:cropped_image_id>', ShapeLabelingRetrieveAPIView.as_view()),
    path('api/handlelabeling/<int:cropped_image_id>', HandleLabelingRetrieveAPIView.as_view()),
    path('api/charmlabeling/<int:cropped_image_id>', CharmLabelingRetrieveAPIView.as_view()),
    path('api/decolabeling/<int:cropped_image_id>', DecoLabelingRetrieveAPIView.as_view()),
    path('api/patternlabeling/<int:cropped_image_id>', PatternLabelingRetrieveAPIView.as_view()),
    path('api/boxing/assign', BoxingAssignAPIView.as_view()),
    path('api/labeling/assign', LabelingAssignAPIView.as_view()),
    path('api/box/<int:original_image_id>', BoxCreateUpdateAPI.as_view()),
    path('api/colorlabel/<int:cropped_image_id>', ColorLabelCreateUpdateAPI.as_view()),
    path('api/shapelabel/<int:cropped_image_id>', ShapeLabelCreateUpdateAPI.as_view()),
    path('api/handlelabel/<int:cropped_image_id>', HandleLabelCreateUpdateAPI.as_view()),
    path('api/charmlabel/<int:cropped_image_id>', CharmLabelCreateUpdateAPI.as_view()),
    path('api/decolabel/<int:cropped_image_id>', DecoLabelCreateUpdateAPI.as_view()),
    path('api/patternlabel/<int:cropped_image_id>', PatternLabelCreateUpdateAPI.as_view()),
    path('api/image/delete/<int:original_image_id>', BoxingDestroyAPIView.as_view()),
    path('api/cropimage/delete/<int:cropped_image_id>', LabelingDestroyAPIView.as_view()),
    path('import/', TemplateView.as_view(template_name='working_page/import_csv.html')),

    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/register', RegistrationAPI.as_view()),
    ]
