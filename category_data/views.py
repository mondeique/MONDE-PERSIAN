from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import mixins, status
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from knox.models import AuthToken


ASSIGN_SIZE = 50
VERSION = 1


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data["username"])
        if len(request.data["username"]) < 3 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid 호출 시 data 형식이 맞는지 확인하게 된다.
        serializer.is_valid(raise_exception=True)
        # serializer.save를 호출하면 serializers 안에 있는 create가 호출이 된다 or data가 존재하면 update가 호출이 된다.
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class HomeRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MyUser.objects.all()
    serializer_class = UserHomeRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        print('get')
        serializer = self.serializer_class(user, context={'boxing_image_id':self.boxing_image_id(),
                                                          'color_labeling_image_id':self.color_labeling_image_id(),
                                                          'shape_labeling_image_id':self.shape_labeling_image_id(),
                                                          'handle_labeling_image_id':self.handle_labeling_image_id(),
                                                          'charm_labeling_image_id':self.charm_labeling_image_id(),
                                                          'deco_labeling_image_id':self.deco_labeling_image_id(),
                                                          'pattern_labeling_image_id':self.pattern_labeling_image_id()})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return self.request.user

    def boxing_image_id(self):
        user = self.get_object()
        image = user.assigned_original_images.filter(valid=None).order_by('pk').first()
        print(image)
        if image:
            return image.id
        return None

    def color_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.categories.color_source.filter(null=True).order_by('pk').first()
        if image:
            return image.id
        return None

    def shape_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.categories.shape_source.filter(null=True).order_by('pk').first()
        if image:
            return image.id
        return None

    def handle_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.categories.handle_source.filter(null=True).order_by('pk').first()
        if image:
            return image.id
        return None

    def charm_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.categories.charm_source.filter(null=True).order_by('pk').first()
        if image:
            return image.id
        return None

    def deco_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.categories.deco_source.filter(null=True).order_by('pk').first()
        if image:
            return image.id
        return None

    def pattern_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.categories.pattern_source.filter(null=True).order_by('pk').first()
        if image:
            return image.id
        return None
