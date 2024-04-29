from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from .models import *
import random

def index(request):
    context = { 'news_list': Post.objects.all() }
    return render(request, 'news/index.html', context=context)


def get_rec_songs(request):
    total_num = Anisong.objects.all().count()
    rand_num = []
    while len(rand_num) < 10:
        temp = random.randint(0,total_num-1)
        if temp not in rand_num:
            rand_num.append(temp)
    temp_res=Anisong.objects.all()
    response = []
    for i in rand_num:
        res = temp_res[i:i+1:1]
        res = res[0]
        song_info = {}
        song_info['type'] = res.type
        song_info['name'] = res.name
        song_info['song_id'] = res.song_id
        song_info['subject_id'] = res.subject_id
        song_info['images'] = res.images
        response.append(song_info)
    return JsonResponse(response,safe=False)
