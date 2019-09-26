import io
import csv
import random
import string
import os
from rest_framework import status
from rest_framework.response import Response
from category_data.models import OriginalImage
from data_management.loader import load_credential
import boto3


def load_csv_data(csv_file):
    csv_file = csv_file.read().decode("utf-8")
    io_string = io.StringIO(csv_file)
    reader = csv.reader(io_string, delimiter=',')
    header = next(reader)
    print(header)
    print('0-------0')
    bag_url_list = []
    for line in reader:
        status = is_jpg(line)
        if is_jpg(line[0]):
            bag_url_list.append(line[0])
    return bag_url_list


def is_jpg(url):
    jpg = '.jpg'
    if jpg in url:
        return True


def generate_filename(n):
    KEY_SOURCE = string.ascii_letters + string.digits
    return ''.join(random.choice(KEY_SOURCE) for _ in range(n))


def load_to_s3(folder_name):
    # Create an S3 Client
    s3 = boto3.client('s3')

    current_path = os.getcwd()
    folder_path = current_path + folder_name
    file_list = os.listdir(folder_path)

    for image in file_list:
        filename = generate_filename(10)
        s3.upload_file(folder_path + image, 'original-bag-images-dev', filename)
        s3_image_url = 'http://s3-ap-northeast-2.amazonsaws.com/original-bag-images-dev' + filename
        OriginalImage.objects.create(s3_image_url=s3_image_url)
    return Response({}, status=status.HTTP_201_CREATED)
