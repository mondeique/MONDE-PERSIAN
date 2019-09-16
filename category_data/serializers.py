from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

VERSION = 1


# 회원가입 시리얼라이저
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["password"]
        )
        return user


# 접속 유지중인지 확인할 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", "username")


# 로그인 시리얼라이저
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


# Home(Main 화면) 조회 시리얼라이저
class UserHomeRetrieveSerializer(serializers.ModelSerializer):
    total_boxing_worked_count = serializers.SerializerMethodField()
    total_labeling_worked_count = serializers.SerializerMethodField()
    boxing_image_id = serializers.SerializerMethodField()
    color_labeling_image_id = serializers.SerializerMethodField()
    shape_labeling_image_id = serializers.SerializerMethodField()
    handle_labeling_image_id = serializers.SerializerMethodField()
    charm_labeling_image_id = serializers.SerializerMethodField()
    deco_labeling_image_id = serializers.SerializerMethodField()
    pattern_labeling_image_id = serializers.SerializerMethodField()
    boxing_worked_count = serializers.ReadOnlyField()
    boxing_assigned_count = serializers.ReadOnlyField()
    color_labeling_worked_count = serializers.ReadOnlyField()
    color_labeling_assigned_count = serializers.ReadOnlyField()
    shape_labeling_worked_count = serializers.ReadOnlyField()
    shape_labeling_assigned_count = serializers.ReadOnlyField()
    handle_labeling_worked_count = serializers.ReadOnlyField()
    handle_labeling_assigned_count = serializers.ReadOnlyField()
    charm_labeling_worked_count = serializers.ReadOnlyField()
    charm_labeling_assigned_count = serializers.ReadOnlyField()
    deco_labeling_worked_count = serializers.ReadOnlyField()
    deco_labeling_assigned_count = serializers.ReadOnlyField()
    pattern_labeling_worked_count = serializers.ReadOnlyField()
    pattern_labeling_assigned_count = serializers.ReadOnlyField()

    class Meta:
        model = MyUser
        fields = ['username',
                  'id',
                  'boxing_assigned_count',
                  'labeling_assigned_count',
                  'total_boxing_worked_count',
                  'total_labeling_worked_count',
                  'color_labeling_worked_count',
                  'shape_labeling_worked_count',
                  'handle_labeling_worked_count',
                  'charm_labeling_worked_count',
                  'deco_labeling_worked_count',
                  'pattern_labeling_worked_count',
                  'boxing_image_id',
                  'color_labeling_image_id',
                  'shape_labeling_image_id',
                  'handle_labeling_image_id',
                  'charm_labeling_image_id',
                  'deco_labeling_image_id',
                  'pattern_labeling_image_id',]

    def get_boxing_assigned_count(self, myuser):
        count = myuser.assigned_original_images.count()
        return count

    def get_labeling_assigned_count(self, myuser):
        count = myuser.assigned_cropped_images.count()
        return count

    def get_total_boxing_worked_count(self, myuser):
        count = myuser.assigned_original_images.filter(valid=True).count()
        return count

    def get_total_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.filter(valid=True).count()
        return count

    def get_color_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.filter(color_source__isnull=False).count()
        return count

    def get_shape_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.filter(shape_source__isnull=False).count()
        return count

    def get_handle_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.filter(handle_source__isnull=False).count()
        return count

    def get_charm_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.filter(charm_source__isnull=False).count()
        return count

    def get_deco_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.filter(deco_source__isnull=False).count()
        return count

    def get_pattern_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.filter(pattern_source__isnull=False).count()
        return count

    def get_boxing_image_id(self, validated_data):
        return self.context['boxing_image_id']

    def get_color_labeling_image_id(self, validated_data):
        return self.context['color_labeling_image_id']

    def get_shape_labeling_image_id(self, validated_data):
        return self.context['shape_labeling_image_id']

    def get_handle_labeling_image_id(self, validated_data):
        return self.context['handle_labeling_image_id']

    def get_charm_labeling_image_id(self, validated_data):
        return self.context['charm_labeling_image_id']

    def get_deco_labeling_image_id(self, validated_data):
        return self.context['deco_labeling_image_id']

    def get_pattern_labeling_image_id(self, validated_data):
        return self.context['pattern_labeling_image_id']


# 알바 관리 page 조회 시리얼라이저
class WorkerManageRetrieveSerializer(serializers.ModelSerializer):
    total_boxing_worked_count = serializers.SerializerMethodField()
    total_labeling_worked_count = serializers.SerializerMethodField()
    color_labeling_worked_count = serializers.ReadOnlyField()
    shape_labeling_worked_count = serializers.ReadOnlyField()
    handle_labeling_worked_count = serializers.ReadOnlyField()
    charm_labeling_worked_count = serializers.ReadOnlyField()
    deco_labeling_worked_count = serializers.ReadOnlyField()
    pattern_labeling_worked_count = serializers.ReadOnlyField()

    class Meta:
        model = MyUser
        fields = ['username',
                  'color_labeling_worked_count',
                  'shape_labeling_worked_count',
                  'handle_labeling_worked_count',
                  'charm_labeling_worked_count',
                  'deco_labeling_worked_count',
                  'pattern_labeling_worked_count',
                  'total_boxing_worked_count',
                  'total_labeling_worked_count',
                  ]

    def get_total_boxing_worked_count(self, myuser):
        count = myuser.assigned_original_images.filter(valid=True).count()
        return count

    def get_total_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.filter(valid=True).count()
        return count

    def get_color_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.color_source.filter(null=False).count()
        return count

    def get_shape_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.shape_source.filter(null=False).count()
        return count

    def get_handle_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.handle_source.filter(null=False).count()
        return count

    def get_charm_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.charm_source.filter(null=False).count()
        return count

    def get_deco_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.deco_source.filter(null=False).count()
        return count

    def get_pattern_labeling_worked_count(self, myuser):
        count = myuser.assigned_cropped_images.categories.pattern_source.filter(null=False).count()
        return count


# Original Image 조회 시리얼라이저
class OriginalImageRetrieveSerializer(serializers.ModelSerializer):
    original_image_id = serializers.ImageField(source='id')

    class Meta:
        model = OriginalImage
        fields = ['original_image_id','image_url']


# Original Image 생성 시리얼라이저
class OriginalImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OriginalImage
        fields = ['image_url']


# Boxing 화면 조회 시리얼라이저
class BoxingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    box_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OriginalImage
        fields =['id',
                 'image_url',
                 'box_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',]

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_box_info(self, image):
        cropped_image = image.cropped_images.last()
        if cropped_image:
            left = cropped_image.left
            right = cropped_image.right
            top = cropped_image.top
            bottom = cropped_image.bottom
            data = {
                'left': left,
                'top': top,
                'right': right,
                'bottom': bottom}
        else:
            data = None
        return data


# Boxing 생성 시리얼라이저
class BoxCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CroppedImage
        fields = ['id',
                  'left',
                  'top',
                  'right',
                  'bottom']


# Color Labeling 화면 조회 시리얼라이저
class ColorLabelingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    color_label_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField()
    origin_id = serializers.SerializerMethodField()

    class Meta:
        model = CroppedImage
        fields =['id',
                 'image_url',
                 'color_label_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',
                 'origin_id',
                 ]

    def get_image_url(self, image):
        image_url = self.context['image_url']
        return image_url

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_origin_id(self, image):
        image = self.context['image']
        origin_id = image.cropped_images.id
        return origin_id

    def get_color_label_info(self, image):
        categories = image.categories.filter(version=VERSION).last()
        if categories:
            color = categories.color_source
            data = {
                'color': color,
            }
        else:
            data = None
        return data


# Shape Labeling 화면 조회 시리얼라이저
class ShapeLabelingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    shape_label_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField()
    origin_id = serializers.SerializerMethodField()

    class Meta:
        model = CroppedImage
        fields =['id',
                 'image_url',
                 'shape_label_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',
                 'origin_id',
                 ]

    def get_image_url(self, image):
        image_url = self.context['image_url']
        return image_url

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_origin_id(self, image):
        image = self.context['image']
        origin_id = image.cropped_images.id
        return origin_id

    def get_shape_label_info(self, image):
        categories = image.categories.filter(version=VERSION).last()
        if categories:
            shape = categories.shape_source
            data = {
                'shape': shape,
            }
        else:
            data = None
        return data


# Handle Labeling 화면 조회 시리얼라이저
class HandleLabelingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    handle_label_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField()
    origin_id = serializers.SerializerMethodField()

    class Meta:
        model = CroppedImage
        fields =['id',
                 'image_url',
                 'handle_label_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',
                 'origin_id',
                 ]

    def get_image_url(self, image):
        image_url = self.context['image_url']
        return image_url

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_origin_id(self, image):
        image = self.context['image']
        origin_id = image.cropped_images.id
        return origin_id

    def get_handle_label_info(self, image):
        categories = image.categories.filter(version=VERSION).last()
        if categories:
            handle = categories.handle_source
            data = {
                'handle': handle,
            }
        else:
            data = None
        return data


# Charm Labeling 화면 조회 시리얼라이저
class CharmLabelingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    charm_label_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField()
    origin_id = serializers.SerializerMethodField()

    class Meta:
        model = CroppedImage
        fields =['id',
                 'image_url',
                 'charm_label_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',
                 'origin_id',
                 ]

    def get_image_url(self, image):
        image_url = self.context['image_url']
        return image_url

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_origin_id(self, image):
        image = self.context['image']
        origin_id = image.cropped_images.id
        return origin_id

    def get_charm_label_info(self, image):
        categories = image.categories.filter(version=VERSION).last()
        if categories:
            charm = categories.charm_source
            data = {
                'charm': charm,
            }
        else:
            data = None
        return data


# Deco Labeling 화면 조회 시리얼라이저
class DecoLabelingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    deco_label_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField()
    origin_id = serializers.SerializerMethodField()

    class Meta:
        model = CroppedImage
        fields =['id',
                 'image_url',
                 'deco_label_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',
                 'origin_id',
                 ]

    def get_image_url(self, image):
        image_url = self.context['image_url']
        return image_url

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_origin_id(self, image):
        image = self.context['image']
        origin_id = image.cropped_images.id
        return origin_id

    def get_deco_label_info(self, image):
        categories = image.categories.filter(version=VERSION).last()
        if categories:
            deco = categories.deco_source
            data = {
                'deco': deco,
            }
        else:
            data = None
        return data


# Pattern Labeling 화면 조회 시리얼라이저
class PatternLabelingRetrieveSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField()
    prev_id = serializers.SerializerMethodField()
    valid_next_id = serializers.SerializerMethodField()
    valid_prev_id = serializers.SerializerMethodField()
    pattern_label_info = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image_url = serializers.SerializerMethodField()
    origin_id = serializers.SerializerMethodField()

    class Meta:
        model = CroppedImage
        fields =['id',
                 'image_url',
                 'pattern_label_info',
                 'next_id',
                 'prev_id',
                 'user',
                 'valid_next_id',
                 'valid_prev_id',
                 'origin_id',
                 ]

    def get_image_url(self, image):
        image_url = self.context['image_url']
        return image_url

    def get_next_id(self, image):
        images = self.context['images']
        next_image = images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_prev_id(self, image):
        images = self.context['images']
        prev_image = images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_valid_next_id(self, image):
        left_images = self.context['left_images']
        next_image = left_images.filter(pk__gt=image.id).order_by('pk').first()
        if next_image:
            return next_image.id
        return None

    def get_valid_prev_id(self, image):
        left_images = self.context['left_images']
        prev_image = left_images.filter(pk__lt=image.id).order_by('pk').last()
        if prev_image:
            return prev_image.id
        return None

    def get_origin_id(self, image):
        image = self.context['image']
        origin_id = image.cropped_images.id
        return origin_id

    def get_pattern_label_info(self, image):
        categories = image.categories.filter(version=VERSION).last()
        if categories:
            pattern = categories.pattern_source
            data = {
                'pattern': pattern,
            }
        else:
            data = None
        return data


# Color Label 생성 및 업데이트 시리얼라이저
class ColorLabelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['color_source']


# Shape Label 생성 및 업데이트 시리얼라이저
class ShapeLabelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['shape_source']


# Handle Label 생성 및 업데이트 시리얼라이저
class HandleLabelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['handle_source']


# Charm Label 생성 및 업데이트 시리얼라이저
class CharmLabelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['charm_source']


# Deco Label 생성 및 업데이트 시리얼라이저
class DecoLabelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['deco_source']


# Pattern Label 생성 및 업데이트 시리얼라이저
class PatternLabelCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['pattern_source']
