from knox.auth import TokenAuthentication
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
from .helpers import load_csv_data

ASSIGN_SIZE = 50
VERSION = 1


# username과 password를 입력하고 회원가입 버튼을 눌렀을 때 호출되는 API
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
        # serializer.save를 호출하면 instance 여부에 따라 update를 호출할지 create를 호출할지 결정하게 된다.
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


# username과 password를 입력하고 로그인 버튼을 눌렀을 때 호출되는 API
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


# User 자체에 대한 접근을 하기 위한 API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Home (Main 화면) 으로 넘어갔을 때 호출되는 API
class HomeRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MyUser.objects.all()
    serializer_class = UserHomeRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        print('get')
        serializer = self.serializer_class(user, context={'boxing_image_id': self.boxing_image_id(),
                                                          'color_labeling_image_id': self.color_labeling_image_id(),
                                                          'shape_labeling_image_id': self.shape_labeling_image_id(),
                                                          'handle_labeling_image_id': self.handle_labeling_image_id(),
                                                          'charm_labeling_image_id': self.charm_labeling_image_id(),
                                                          'deco_labeling_image_id': self.deco_labeling_image_id(),
                                                          'pattern_labeling_image_id': self.pattern_labeling_image_id()})
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


# Boxing 할당받기 버튼을 눌렀을 때 호출되는 API
class BoxingAssignAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OriginalImage.objects.all()

    def post(self, request, **kwargs):
        user = request.user
        unassigned_images = self.queryset.filter(assigned_user__isnull=True).exclude(imge="")
        images = unassigned_images.order_by('pk')[:ASSIGN_SIZE]
        for image in images:
            image.assigned_user = user
            image.save_valid()
        return Response(status=status.HTTP_201_CREATED)


# Labeling 할당받기 버튼을 눌렀을 때 호출되는 API
class LabelingAssignAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CroppedImage.objects.all()

    def post(self, request, **kwargs):
        user = request.user
        unassigned_images = self.queryset.filter(assigned_user__isnull=True).exclude(image="")
        images = unassigned_images.order_by('pk')[:ASSIGN_SIZE]
        for image in images:
            image.assigned_user = user
            image.save_valid()
        return Response(status=status.HTTP_201_CREATED)


#  Original Image 생성 시 호출되는 API (미리 upload 되어 있어야 함)
class OriginalImageCreateAPIView(generics.CreateAPIView):
    """
    csv file upload
    """
    serializer_class = OriginalImageCreateSerializer
    queryset = OriginalImage.objects.all()

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['csv_file']
        bag_url_list = load_csv_data(csv_file)
        objs = [OriginalImage(image_url=url) for url in bag_url_list]
        OriginalImage.objects.bulk_create(objs)

        return redirect("/admin")


# Boxing 화면 url 입력 시 호출되는 API
class BoxingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoxingRetrieveSerializer
    queryset = OriginalImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        left_images = images.filter(valid=None)
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images


def retry(func):
    def retried_func(*args, **kwargs):
        MAX_TRIES = 5
        tries = 0
        while True:
            resp = func(*args,**kwargs)
            print('---resp code---')
            print(resp.status_code)
            if resp.status_code != 200 and tries < MAX_TRIES:
                tries += 1
                print(tries)
                continue
            break
        return resp
    return retried_func


# Box 생성 및 업데이트 시 호출되는 API
class BoxCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = CroppedImage.objects.all()
    serializer_class = BoxCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        original_image = self.get_object()
        left, right, top, bottom = self.get_ltrb()
        # client에서 put으로 보내지 못한경우 : update의 경우
        # 이 경우는 원본이미지 저장 X
        if original_image.cropped_images.last():
            cropped_image = self.queryset.get(origin_source=original_image)
            cropped_image.update(left, top, right, bottom)
            return Response({},status=status.HTTP_206_PARTIAL_CONTENT)

        CroppedImage.objects.create(origin_source=original_image,
                                    left=left,
                                    top=top,
                                    right=right,
                                    bottom=bottom)
        original_image.valid = True
        original_image.save()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        original_image = self.get_object()
        cropped_image = self.queryset.get(origin_source=original_image)
        left, right, top, bottom = self.get_ltrb()
        cropped_image.update(left, top, right, bottom)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_ltrb(self):
        data = self.request.data
        left = data['left']
        right = data['right']
        top = data['top']
        bottom = data['bottom']
        if left and right and top and bottom:
            return (float(left), float(right), float(top), float(bottom))
        else:
            print('원본')
            return (0, 1, 0, 1)

    def get_serializer_context(self, *args, **kwargs):
        id = self.kwargs['original_image_id']
        original_image = OriginalImage.objects.filter(pk=id).last()
        if original_image:
            return {'request': self.request,
                    'original_image': original_image,}
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        id = self.kwargs['original_image_id']
        original_image = OriginalImage.objects.filter(pk=id).last()
        return original_image


# Box 삭제 시 호출되는 API
class BoxingDestroyAPIView(generics.DestroyAPIView):
    """
    original image 삭제
    """
    permission_classes = (IsAuthenticated,)
    queryset = OriginalImage.objects.all()

    def post(self, request, *args, **kwargs):
        return super(BoxingDestroyAPIView, self).destroy(request, *args, **kwargs)

    def get_object(self):
        id = self.kwargs['original_image_id']
        return self.queryset.get(pk=id)


# Box hold 하고 있을 때 호출되는 API
class BoxingHoldAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = OriginalImage.objects.all()

    def put(self, request, *args, **kwargs):
        image = self.get_object()
        # put이고 updateapiview라 다를듯.
        image.update(valid=False)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['original_image_id']
        return self.queryset.filter(pk=id)
