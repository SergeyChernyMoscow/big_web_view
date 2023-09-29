from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import HttpResponse, Http404, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import ChangeUserInfoForm, RegisterUserForm
from .models import Home, AdvUser, Camera
from .utilities import signer
from django.views.decorators import gzip
from video import apply_yolo_object_detection, draw_object_bounding_box, draw_object_count
import cv2
import numpy as np

def index(request):
    users = AdvUser.objects.all()
    homes = Home.objects.all()
    context = {'users': users, 'homes': homes}
    return render(request, 'index.html', context)

def by_home(request, home_id):
    users = AdvUser.objects.filter(home=home_id)
    cameras = Camera.objects.filter(linked_home=home_id)
    homes = Home.objects.all()
    current_home = Home.objects.get(pk=home_id)
    context = {'users': users, 'homes': homes, 'current_home': current_home, 'cameras': cameras}
    return render(request, 'by_home.html', context)

def by_camera(request, camera_id):
    current_camera = Camera.objects.get(pk=camera_id)
    context = {'current_camera': current_camera}
    return render(request, 'by_camera.html', context)

def other_page(request, page):
    try:
        template= get_template(page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request = request))

class BwcLoginView(LoginView):
    tamplate_name = 'login.html'

@login_required
def profile(request):
    homes = Home.objects.all()
    context = {'homes': homes}
    return render(request, 'profile.html', context)

class BwcLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя изменены'
    def setup (self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request,*args,**kwargs)
    def get_object (self, queryset = None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class BwcPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile')
    success_message = 'Пароль пользователя успешно изменен'

class RergisterUserView(CreateView):
    model = AdvUser
    template_name = 'register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')

class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'user_is_activated.html'
    else:
        template = 'activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('index')
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)
    def get_object(self, queryset = None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://91.77.164.58:554/11')
        self.net = cv2.dnn.readNetFromDarknet("Resources/yolov4-tiny.cfg",
                                         "Resources/yolov4-tiny.weights")
        self.layer_names = self.net.getLayerNames()
        self.out_layers_indexes = self.net.getUnconnectedOutLayers()
        self.out_layers = [self.layer_names[index - 1] for index in self.out_layers_indexes]
        with open("Resources/coco.names") as file:
            self.classes = file.read().split("\n")
        self.look_for = ['car', 'bus', 'person']

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        image = apply_yolo_object_detection(image, self.net, self.out_layers, self.classes, self.look_for)
        ret,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def sub_index(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError:
        print("aborted")