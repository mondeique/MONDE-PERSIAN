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
        return image.id

    def color_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.filter(categories__color_source__isnull=True).order_by('pk').first()
        return image.id

    def shape_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.filter(categories__shape_source__isnull=True).order_by('pk').first()
        return image.id

    def handle_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.filter(categories__handle_source__isnull=True).order_by('pk').first()
        return image.id

    def charm_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.filter(categories__charm_source__isnull=True).order_by('pk').first()
        return image.id

    def deco_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_images.filter(categories__deco_source__isnull=True).order_by('pk').first()
        return image.id

    def pattern_labeling_image_id(self):
        user = self.get_object()
        image = user.assigned_cropped_imagesfilter(categories__pattern_source__isnull=True).order_by('pk').first()
        return image.id


# 알바 관리 page 버튼을 눌렀을 때 호출되는 API
class WorkerManageRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = MyUser.objects.filter(is_admin=False)
    serializer_class = WorkerManageRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs['user_id']
        worker = self.queryset.get(pk=id)
        serializer = self.serializer_class(worker)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Boxing 할당받기 버튼을 눌렀을 때 호출되는 API
class BoxingAssignAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OriginalImage.objects.all()

    def post(self, request, **kwargs):
        user = request.user
        unassigned_images = self.queryset.filter(assigned_user__isnull=True).exclude(image="")
        images = unassigned_images.order_by('pk')[:ASSIGN_SIZE]
        for image in images:
            image.assigned_user = user
            image.save_origin_valid()
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
        id = self.kwargs['original_image_id']
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
        serializer = self.serializer_class(data=request.data, context={'origin_source':self.get_object()})
        serializer.is_valid()
        serializer.save()
        original_image.valid = True
        original_image.save()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        original_image = self.get_object()
        cropped_image = self.queryset.get(origin_source=original_image)
        serializer = self.serializer_class(data=request.data)
        cropped_image.update(serializer.data)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

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


# Color Labeling 화면 url 입력 시 호출되는 API
class ColorLabelingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ColorLabelingRetrieveSerializer
    queryset = CroppedImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        images, image = self.get_image()
        left_images = images.filter(categories__color_source__isnull=False).exclude(image="")
        image_url = self.get_image_url().data
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images,
                                                               'image': image,
                                                               'image_url': image_url})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retry
    def get_image_url(self):
        _, image = self.get_image()
        image_url = image.image.url
        return Response(image_url, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images

    def get_image(self, **kwargs):
        id = self.kwargs['cropped_image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        return images, image


# Shape Labeling 화면 url 입력 시 호출되는 API
class ShapeLabelingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShapeLabelingRetrieveSerializer
    queryset = CroppedImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        images, image = self.get_image()
        left_images = images.filter(categories__shape_source__isnull=False).exclude(image="")
        image_url = self.get_image_url().data
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images,
                                                               'image': image,
                                                               'image_url': image_url})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retry
    def get_image_url(self):
        _, image = self.get_image()
        image_url = image.image.url
        return Response(image_url, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images

    def get_image(self, **kwargs):
        id = self.kwargs['cropped_image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        return images, image


# Handle Labeling 화면 url 입력 시 호출되는 API
class HandleLabelingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HandleLabelingRetrieveSerializer
    queryset = CroppedImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        images, image = self.get_image()
        left_images = images.filter(categories__handle_source__isnull=False).exclude(image="")
        image_url = self.get_image_url().data
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images,
                                                               'image': image,
                                                               'image_url': image_url})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retry
    def get_image_url(self):
        _, image = self.get_image()
        image_url = image.image.url
        return Response(image_url, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images

    def get_image(self, **kwargs):
        id = self.kwargs['cropped_image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        return images, image


# Charm Labeling 화면 url 입력 시 호출되는 API
class CharmLabelingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CharmLabelingRetrieveSerializer
    queryset = CroppedImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        images, image = self.get_image()
        left_images = images.filter(categories__charm_source__isnull=False).exclude(image="")
        image_url = self.get_image_url().data
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images,
                                                               'image': image,
                                                               'image_url': image_url})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retry
    def get_image_url(self):
        _, image = self.get_image()
        image_url = image.image.url
        return Response(image_url, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images

    def get_image(self, **kwargs):
        id = self.kwargs['cropped_image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        return images, image


# Deco Labeling 화면 url 입력 시 호출되는 API
class DecoLabelingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DecoLabelingRetrieveSerializer
    queryset = CroppedImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        images, image = self.get_image()
        left_images = images.filter(categories__deco_source__isnull=False).exclude(image="")
        image_url = self.get_image_url().data
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images,
                                                               'image': image,
                                                               'image_url': image_url})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retry
    def get_image_url(self):
        _, image = self.get_image()
        image_url = image.image.url
        return Response(image_url, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images

    def get_image(self, **kwargs):
        id = self.kwargs['cropped_image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        return images, image


# Pattern Labeling 화면 url 입력 시 호출되는 API
class PatternLabelingRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PatternLabelingRetrieveSerializer
    queryset = CroppedImage.objects.all()

    def retrieve(self, request, *args, **kwargs):
        images, image = self.get_image()
        left_images = images.filter(categories__pattern_source__isnull=False).exclude(image="")
        image_url = self.get_image_url().data
        if image:
            serializer = self.serializer_class(image, context={'left_images': left_images,
                                                               'images': images,
                                                               'image': image,
                                                               'image_url': image_url})
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @retry
    def get_image_url(self):
        _, image = self.get_image()
        image_url = image.image.url
        return Response(image_url, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        images = self.queryset.filter(assigned_user=user)
        return images

    def get_image(self, **kwargs):
        id = self.kwargs['cropped_image_id']
        images = self.get_queryset()
        image = images.filter(pk=id).last()
        return images, image


# Labeling Image 삭제 시 호출되는 API
class LabelingDestroyAPIView(generics.DestroyAPIView):
    """
    labeling image 삭제
    """
    permission_class = (IsAuthenticated,)
    queryset = CroppedImage.objects.all()

    def post(self, request, *args, **kwargs):
        return super(LabelingDestroyAPIView, self).destroy(request,*args,**kwargs)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        return self.queryset.get(pk=id)


# Color Label 생성 및 업데이트 시 호출되는 API
class ColorLabelCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.filter(color_source__isnull=True).all()
    serializer_class = ColorLabelCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        color_data = self.get_category_data()
        cropped_image.categories.color_source.objects.create(**color_data)
        cropped_image.save_valid()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        category = cropped_image.categories.color_source.last()
        cropped_image.categories.color_source.objects.update(color_source=category)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        cropped_image = CroppedImage.objects.get(pk=id)
        return cropped_image

    def get_category_data(self):
        data = self.request.data
        cropped_image = self.get_object()
        color_data = {
            'color': int(data['color']),
            'cropped_image': cropped_image
                      }
        return color_data


# Shape Label 생성 및 업데이트 시 호출되는 API
class ShapeLabelCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.filter(shape_source__isnull=True).all()
    serializer_class = ShapeLabelCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        shape_data = self.get_category_data()
        cropped_image.categories.shape_source.objects.create(**shape_data)
        cropped_image.save_valid()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        category = cropped_image.categories.shape_source.last()
        cropped_image.categories.shape_source.objects.update(shape_source=category)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        cropped_image = CroppedImage.objects.get(pk=id)
        return cropped_image

    def get_category_data(self):
        data = self.request.data
        cropped_image = self.get_object()
        shape_data = {
            'shape': int(data['shape']),
            'cropped_image': cropped_image
                      }
        return shape_data


# Handle Label 생성 및 업데이트 시 호출되는 API
class HandleLabelCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.filter(handle_source__isnull=True).all()
    serializer_class = HandleLabelCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        handle_data = self.get_category_data()
        cropped_image.categories.handle_source.objects.create(**handle_data)
        cropped_image.save_valid()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        category = cropped_image.categories.handle_source.last()
        cropped_image.categories.handle_source.objects.update(handle_source=category)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        cropped_image = CroppedImage.objects.get(pk=id)
        return cropped_image

    def get_category_data(self):
        data = self.request.data
        cropped_image = self.get_object()
        handle_data = {
            'handle': int(data['handle']),
            'cropped_image': cropped_image
                      }
        return handle_data


# Charm Label 생성 및 업데이트 시 호출되는 API
class CharmLabelCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.filter(charm_source__isnull=True).all()
    serializer_class = CharmLabelCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        charm_data = self.get_category_data()
        cropped_image.categories.charm_source.objects.create(**charm_data)
        cropped_image.save_valid()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        category = cropped_image.categories.charm_source.last()
        cropped_image.categories.charm_source.objects.update(charm_source=category)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        cropped_image = CroppedImage.objects.get(pk=id)
        return cropped_image

    def get_category_data(self):
        data = self.request.data
        cropped_image = self.get_object()
        charm_data = {
            'charm': int(data['charm']),
            'cropped_image': cropped_image
                      }
        return charm_data


# Deco Label 생성 및 업데이트 시 호출되는 API
class DecoLabelCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.filter(deco_source__isnull=True).all()
    serializer_class = DecoLabelCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        deco_data = self.get_category_data()
        cropped_image.categories.deco_source.objects.create(**deco_data)
        cropped_image.save_valid()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        category = cropped_image.categories.deco_source.last()
        cropped_image.categories.deco_source.objects.update(deco_source=category)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        cropped_image = CroppedImage.objects.get(pk=id)
        return cropped_image

    def get_category_data(self):
        data = self.request.data
        cropped_image = self.get_object()
        deco_data = {
            'deco': int(data['deco']),
            'cropped_image': cropped_image
                      }
        return deco_data


# Pattern Label 생성 및 업데이트 시 호출되는 API
class PatternLabelCreateUpdateAPI(GenericAPIView, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.filter(pattern_source__isnull=True).all()
    serializer_class = PatternLabelCreateUpdateSerializer

    def post(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        pattern_data = self.get_category_data()
        cropped_image.categories.pattern_source.objects.create(**pattern_data)
        cropped_image.save_valid()
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        cropped_image = self.get_object()
        category = cropped_image.categories.pattern_source.last()
        cropped_image.categories.pattern_source.objects.update(pattern_source=category)
        return Response({}, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_object(self):
        id = self.kwargs['cropped_image_id']
        cropped_image = CroppedImage.objects.get(pk=id)
        return cropped_image

    def get_category_data(self):
        data = self.request.data
        cropped_image = self.get_object()
        pattern_data = {
            'pattern': int(data['pattern']),
            'cropped_image': cropped_image
                      }
        return pattern_data

