import json
import cv2
import datetime
import numpy as np
import base64
from django.views.generic import FormView, TemplateView, View
from django.core.files.base import ContentFile

from django.shortcuts import redirect, render, HttpResponseRedirect
from django.conf import settings

from Irisrecognition.models import PictureUpload

import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


class TestView(TemplateView):
    template_name = 'snapshot5.html'


class ImageParser(TemplateView):
    template_name = 'snapshot5.html'

    def post(self, request):
        image = json.loads(request.body)

        # read captured image
        image = image['imageString']
        img = image.split(',')[-1]
        # with open("imageToSave.png", "wb") as fh:
        #     fh.write(base64.b64decode(img))
        format, imgstr = image.split(';base64,')
        ext = format.split('/')[-1]
        file_name = str(get_random_string(8))+str(datetime.datetime.now())
        name = file_name + '.' + 'jpg'
        data = ContentFile(base64.b64decode(imgstr), name=name)  # You can save this as file instance.
        img_obj = PictureUpload.objects.create(name=file_name, image=data) # save captured image in DB
        img_obj.save()
        face_cascade = cv2.CascadeClassifier('Cascades2/haarcascade_frontalface.xml')
        eye_cascade = cv2.CascadeClassifier('Cascades2/parojos.xml')
        # save the image(i) in the same directory
        img = cv2.imread(img_obj.image.path)
        # img = cv2.imread("imageToSave.png")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            # eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                yei_gray = gray[ey:ey + eh, ex:ex + ew]

        path = settings.PROCESSSED_IMAGE_ROOT
        cv2.imwrite(path+"/eye.jpg", img)

        with open(path+"/eye.jpg", "rb")as img_file:
            my_string = base64.b64encode(img_file.read())
        name = file_name + '.' + 'jpg'
        data = ContentFile(base64.b64decode(my_string), name=name)

        img_obj.identified_image = data  #save identified image in DB
        img_obj.save()
        cv2.imshow('img', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


        return render(request, self.template_name, {})
