from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from . import recognition as reg
import logging as log
from django.contrib import messages


# Create your views here.

def page_error(request):
    messages.error(request, "Reselect picture upload !")
    return redirect('/MHealth/upload/')


'''handle login'''


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')
        if uname == 'IAM' and pwd == '123':
            return redirect('/MHealth/upload/')
    return None


def set_log_file():
    log_file_path = './MHealth/chemistry.log'
    log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=log_file_path,
                    filemode='a')


'''show information'''


def index_view(request):
    photo = request.FILES.get('files[]', '')
    if photo == '':
        messages.error(request, "No picture detected ! Please select one picture upload !")
        return HttpResponseRedirect('/MHealth/upload/')
    Photo.objects.create(photo=photo)
    photo_path = './MHealth/imgs/' + photo.name
    print(photo.name)
    # photo_path = './MHealth/test.png'
    set_log_file()
    log.info("Task beginning ......")
    hole1_green, hole2_green, hole3_green = reg.imageProcessing(photo_path)
    rel_hole2_green, rel_hole3_green = reg.getRelativeRGB(hole1_green, hole2_green, hole3_green)
    temp = reg.getWeather('南京')
    enzyme_concentration, PH = reg.calculate(temp, rel_hole2_green, rel_hole3_green)
    if PH >= 8.2 or PH < 5.8:
        messages.error(request, "Test limit exceeded ! Please reselect picture upload !")
        return HttpResponseRedirect('/MHealth/upload/')
    log.info("Hole3 enzyme concentration is {:.2f}".format(enzyme_concentration))
    log.info("Task ending !")
    log.info("*" * 100)
    return render(request, 'index.html', {
        'hole1_green': int(hole1_green),
        'hole2_green': int(hole2_green),
        'hole3_green': int(hole3_green),
        'temp': temp,
        'PH': int(PH),
        'enzyme_concentration': int(enzyme_concentration), })


def upload_photo(request):
    return render(request, 'upload.html')
