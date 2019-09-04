from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth import get_user_model
import requests
import random
import string
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


PRECISION = 4
THRESHOLD = 0.1 ** PRECISION
CANDIDATES_COUNT = 100


def equals(f1, f2):
    print(f1-f2)
    return abs(f1 - f2) < THRESHOLD


def get_image_filename(image):
    _First = '_1'

    if image:
        whole_name = image.name
        jpg_name = whole_name.split('/')[1]
        prev_name = jpg_name.split('.')[0]
        name = prev_name.split('_')[0]
        name_order = int(prev_name.split('_')[1])
        next_order = name_order + 1
        rename = name + '_' + str(next_order) + '.jpg'
        print('renamed!')
        return rename
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + \
           random.choice(string.ascii_uppercase) + _First + '.jpg'


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have name.')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    objects = UserManager()

    tag_user = models.IntegerField(null=True, blank=True, verbose_name='Qbase Tag User')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='관리자 여부')

    username = models.CharField(max_length=120, verbose_name='아이디', unique=True)
    name = models.CharField(max_length=30, verbose_name='이름')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def boxing_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_original_images.filter(valid=True).count()
        return images_count

    @property
    def boxing_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_original_images.count()
        return images_count

    @property
    def color_labeling_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.colors.filter(null=False).count()
        return images_count

    @property
    def color_labeling_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.colors.count()
        print(images_count)
        return images_count

    @property
    def shape_labeling_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.shapes.filter(null=False).count()
        return images_count

    @property
    def shape_labeling_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.shapes.count()
        print(images_count)
        return images_count

    @property
    def charm_labeling_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.charms.filter(null=False).count()
        return images_count

    @property
    def charm_labeling_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.charms.count()
        print(images_count)
        return images_count

    @property
    def handle_labeling_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.handles.filter(null=False).count()
        return images_count

    @property
    def handle_labeling_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.handles.count()
        print(images_count)
        return images_count

    @property
    def pattern_labeling_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.patterns.filter(null=False).count()
        return images_count

    @property
    def pattern_labeling_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.patterns.count()
        print(images_count)
        return images_count

    @property
    def deco_labeling_worked_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.decorations.filter(null=False).count()
        return images_count

    @property
    def deco_labeling_assigned_count(self):
        user = MyUser.objects.get(pk=self.pk)
        images_count = user.assigned_cropped_images.categories.decorations.count()
        print(images_count)
        return images_count
    

User = get_user_model()


class OriginalImage(models.Model):
    assigned_user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_original_images')
    image_url = models.URLField(max_length=300)
    valid = models.NullBooleanField()
    # TODO: 이름
    image = models.ImageField(upload_to='', null=True, blank=True)

    def get_image_extension(self):
        return 'jpeg'

    @property
    def prev_id(self):
        return OriginalImage.objects.filter(pk__lt=self.pk).order_by('pk').last().pk

    @property
    def next_id(self):
        next_id = OriginalImage.objects.filter(pk__gt=self.pk).order_by('pk').first().pk
        if next_id:
            return next_id
        return None

    def save(self, *args, **kwargs):
        super(OriginalImage, self).save(*args, **kwargs)
        if not self.image:
            print('save original image')
            self._save_image()

    def save_valid(self, *args, **kwargs):
        #TODO: fix me!
        super(OriginalImage, self).save(*args, **kwargs)

    def _save_image(self):
        #TODO : crop 말고 저장
        from PIL import Image
        resp = requests.get(self.image_url)
        print('request')
        print(resp)
        image = Image.open(BytesIO(resp.content))
        width, height = image.size
        left = width * 0.01
        top = height * 0.01
        right = width * 0.99
        bottom = height * 0.99
        crop_data = image.crop((int(left), int(top), int(right), int(bottom)))
        # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
        crop_io = BytesIO()
        crop_data.save(crop_io, format=self.get_image_extension())
        print('crop save')
        crop_file = InMemoryUploadedFile(crop_io, None, get_image_filename(self.image), 'image/jpeg', len(crop_io.getvalue()), None)
        self.image.save(get_image_filename(self.image), crop_file, save=False)
        # To avoid recursive save, call super.save
        super(OriginalImage, self).save()


class CroppedImage(models.Model):
    assigned_user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE, related_name='assigned_cropped_images')
    origin_source = models.ForeignKey(OriginalImage, null=True, blank=True, related_name='cropped_images', on_delete=models.CASCADE)
    left = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    top = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    right = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    bottom = models.DecimalField(max_digits=PRECISION + 1, decimal_places=PRECISION)
    # TODO : 이름
    image = models.ImageField(upload_to='', null=True, blank=True)
    image_url = models.URLField(null=True,blank=True, max_length=250, verbose_name='aws s3 이미지 url')
    valid = models.BooleanField(default=False)
    usable = models.BooleanField(default=True)

    def validate_coordinates(self):
        if self.left >= self.right:
            raise Exception('left >= right')
        elif self.top >= self.bottom:
            raise Exception('top >= bottom')
        self.left = 0 if self.left < 0 else self.left
        self.top = 0 if self.top < 0 else self.top
        self.right = 1 if self.right > 1 else self.right
        self.bottom = 1 if self.bottom > 1 else self.bottom

    def save(self, *args, **kwargs):
        self.validate_coordinates()
        super(CroppedImage, self).save(*args, **kwargs)
        self._save_cropped_image()

    def save_valid(self, *args, **kwargs):
        super(CroppedImage, self).save(*args, **kwargs)

    def update(self, left, top, right, bottom):
        if not equals(float(self.left), left) or \
                not equals(float(self.top), top) or \
                not equals(float(self.right), right) or \
                not equals(float(self.bottom), bottom):
            self.left = left
            self.top = top
            self.right = right
            self.bottom = bottom
            self.save()
            # return True
        else:
            print('똑같음')
            # return False #to response status

    def __str__(self):
        if self.id:
            return 'B%d' % self.id
        return ''

    @property
    def image_URL(self):
        return self.image.url

    def _save_cropped_image(self):
        from PIL import Image
        resp = requests.get(self.origin_source.image_url)
        image = Image.open(BytesIO(resp.content))
        width, height = image.size
        left = width * self.left
        top = height * self.top
        right = width * self.right
        bottom = height * self.bottom
        crop_data = image.crop((int(left), int(top), int(right), int(bottom)))
        # http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file
        crop_io = BytesIO()
        crop_data.save(crop_io, format=self.origin_source.get_image_extension())
        crop_file = InMemoryUploadedFile(crop_io, None, get_image_filename(self.image), 'image/jpeg', len(crop_io.getvalue()), None)
        self.image.save(get_image_filename(self.image), crop_file, save=False)
        # To avoid recursive save, call super.save
        super(CroppedImage, self).save()


class ColorTag(models.Model):
    color_name = models.CharField(max_length=50)


class ShapeTag(models.Model):
    color_name = models.CharField(max_length=50)


class CharmTag(models.Model):
    color_name = models.CharField(max_length=50)


class HandleTag(models.Model):
    color_name = models.CharField(max_length=50)


class DecoTag(models.Model):
    color_name = models.CharField(max_length=50)


class PatternTag(models.Model):
    color_name = models.CharField(max_length=50)


class Categories(models.Model):
    version = models.IntegerField()
    cropped_image = models.ForeignKey(CroppedImage, on_delete=models.CASCADE, related_name='categories')
    color_source = models.ForeignKey(ColorTag, null=True, on_delete=models.CASCADE, related_name='colors')
    shape_source = models.ForeignKey(ShapeTag, null=True, on_delete=models.CASCADE, related_name='shapes')
    charm_source = models.ForeignKey(CharmTag, null=True, on_delete=models.CASCADE, related_name='chamrs')
    handle_source = models.ForeignKey(HandleTag, null=True, on_delete=models.CASCADE, related_name='handles')
    deco_source = models.ForeignKey(DecoTag, null=True, on_delete=models.CASCADE, related_name='decorations')
    pattern_soruce = models.ForeignKey(PatternTag, null=True, on_delete=models.CASCADE, related_name='patterns')







