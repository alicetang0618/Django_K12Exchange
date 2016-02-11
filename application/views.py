from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django import forms
from PIL import Image as PImage
from os.path import join as pjoin
from datetime import datetime, timedelta
from nltk import word_tokenize
import pylab as plt
from django.shortcuts import get_object_or_404
from filetransfers.api import serve_file

from forms import *
from models import *
from util import *
from search import build_search_engine

search_engine = build_search_engine()


# Main Page
def home(request):
    if request.method == 'POST' and request.POST.get('search'):
        form = SearchForm(request.POST)
        if form.is_valid():  
            search = form.save(commit = False)
            if request.user.is_authenticated():
                search.user = request.user.profile # if the user is logged in
            search.save()  
            return redirect("/search/"+str(search.id))
    else:
        form = SearchForm()  
    c = {
        'form':form
        }   
    return render(request,'home.html',c)


# User Account Functions
def join(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = UserCreateForm(request.POST, request.FILES)
            if form.is_valid():
                new_user = UserProfile(picture =request.FILES['profile_picture'])
                new_user = form.save()
                return redirect("/login/")
        else:
            form = UserCreateForm()
        c = {
            'form': form
        }
    else:
        c={}
    return render(request, "join.html", c, context_instance = RequestContext(request))


def login(request):
    if request.user.is_authenticated():
        return render(request,'login.html',{})
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect("/")
                else:
                    return redirect("/login/")
            else:
                return redirect("/login/")
        else:
            return render_to_response('login.html', {}, RequestContext(request))

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        return render(request, 'logout.html', {})
    else:
        return redirect("/")

# User Functions
def my_profile(request):
    if request.user.is_authenticated():
        user = request.user.profile
        c = {
            'user': user
        }
    else:
        return redirect("/login/")
        c={}
    return render(request,"my_profile.html", c)


def modify_profile(request):
    if request.method == 'POST' and request.POST.get('profile'):
        form = UserModifyForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('/my_profile/')
    else:
        form = UserModifyForm(instance=request.user.profile)
    c = {
        'form': form
    }
    return render(request, 'modify_profile.html', c)


def profile(request, user_id):
    viewuser = UserProfile.objects.get(id=user_id)
    materials = Material.objects.filter(uploader=viewuser)
    ratings = Rating.objects.filter(rated=viewuser)
    if request.method == 'POST' and request.POST.get('rate_submit'):
        rateform = RateForm(request.POST)       
        if rateform.is_valid(): 
            rate = rateform.save() 
            rate.rater = request.user.profile 
            rate.rated = viewuser
            rate.save()
    else:
        rateform = RateForm()
    if request.method == 'POST' and request.POST.get('message_submit'):
        messageform = MessageForm(request.POST)       
        if messageform.is_valid(): 
            message = messageform.save() 
            message.sender = request.user.profile 
            message.receiver = viewuser
            message.save()
    else:
        messageform = MessageForm()
    c = {
        'viewuser': viewuser,
        'materials': materials,
        'num_material': len(materials),
        'rateform': rateform,
        'ratings': ratings,
        'messageform': messageform,
        'num_rating': len(ratings)
    }
    return render(request,"profile.html",c)


def my_materials(request):
    if not request.user.is_authenticated():
        return redirect("/login/")
    materials = Material.objects.filter(uploader=request.user.profile)
    num = len(materials)
    c = {
        'materials':materials,
        'num':num
    }
    return render(request, "my_materials.html", c)


def upload(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = AddMaterialForm(request.POST, request.FILES)
            if form.is_valid():
                material = Material(doc = request.FILES['doc'])
                material = form.save()
                material.uploader=request.user.profile
                material.save()
                search_engine = build_search_engine()
                return redirect("/my_materials/")
        else:
            form = AddMaterialForm()
        c = {
            'form': form
        }
        return render(request, 'upload.html', c)
    else:
        return redirect("/login/")


def material(request, material_id):
    try:
        material = Material.objects.get(id=material_id)
    except material.DoesNotExist:
        raise Http404('Material does not exist')

    if request.method == 'POST' and request.POST.get('remove'):
        material.delete()
        return redirect('/my_materials/')

    if request.method == 'POST' and request.POST.get('like'):
        if not request.user.is_authenticated():
            return redirect("/login/")
        if request.user.profile not in material.liked_by.all():
            material.liked_by.add(request.user.profile)
            material.save()
        return redirect("/material/"+str(material_id))

    ratings = Rating.objects.filter(material = material)
    averagerating = avgrating(material)

    liked = False
    if request.user.is_authenticated() and request.user.profile in material.liked_by.all():
        liked = True

    downloader = False
    if request.user.is_authenticated():
        if Download.objects.filter(user = request.user.profile).filter(material = material)!=[]:
            downloader = True

    if request.method == 'POST' and request.POST.get('rate_submit'):
        form = RateForm(request.POST)       
        if form.is_valid(): 
            rate = form.save() 
            rate.rater = request.user.profile 
            rate.material = material
            rate.save()
            return redirect("/material/"+str(material_id))
    else:
        form = RateForm() 

    if request.method == 'POST' and request.POST.get('download'):
        return download(request, material_id)

    c = {
        'material': material,
        'liked': liked,
        'downloader': downloader,
        'ratings': ratings,
        'num_rating': len(ratings),
        'avgrating':averagerating,
        'rateform': form,
        'downloads': len(Download.objects.filter(material=material).filter(time__gte=datetime.now()-timedelta(weeks=12)))
    }

    return render(request, "material.html", c)


def download(request, material_id):
    download=Download.objects.create(material=Material.objects.get(id=material_id))
    if request.user.is_authenticated():
        download.user=request.user.profile
        download.save()
    object = get_object_or_404(Material, pk=material_id)
    return serve_file(request, object.doc)


def my_downloads(request):
    if not request.user.is_authenticated():
        return redirect("/login/")
    user=request.user.profile
    downloads=Download.objects.filter(user=user).order_by('time').reverse()
    num = len(downloads)
    c={
        'downloads': downloads,
        'num': num
    }
    return render(request, "my_downloads.html", c)


def like(request):
    user = request.user.profile
    like = []
    for material in Material.objects.all():
        if user in material.liked_by.all():
            like.append(material)
    c={
        "likes": like,
        "num": len(like)
    }
    return render(request,"like.html",c)


def my_messages(request):
    if not request.user.is_authenticated():
        return redirect("/login/")
    messages = Message.objects.filter(receiver=request.user.profile).order_by('time').reverse()
    sent = Message.objects.filter(sender=request.user.profile).order_by('time').reverse()
    c={
        "receive": messages,
        "num_rece": len(messages),
        "sent": sent,
        "num_sent": len(sent)
    }
    return render(request,"my_messages.html",c)


def message(request, message_id):
    message=Message.objects.get(id=message_id)
    if request.method == 'POST':
        messageform = MessageForm(request.POST)      
        if messageform.is_valid():
            reply = messageform.save()
            reply.sender = request.user.profile
            if message.sender == request.user.profile:
                reply.receiver = message.receiver
            else:
                reply.receiver = message.sender
            reply.save()
    else:
        messageform = MessageForm()
        reply = None
    c = {
        'message': message,
        'reply': reply,
        'messageform': messageform
    }
    return render(request,"message.html",c)


def search(request, search_id):
    search = Search.objects.get(id = search_id)
    materials = filter(lambda x: x.category==search.category, search_engine(search))

    if request.method == "POST" and request.POST.get('rating'):
        materials = order_by_rating(materials)
    if request.method == "POST" and request.POST.get('popularity'):
        materials = order_by_popularity(materials)
    ratings= [(material, avgrating(material)) for material in materials]
    
    if request.method == 'POST' and request.POST.get('search'):
        form = SearchForm(request.POST)
        if form.is_valid():  
            search = form.save(commit = False)
            if request.user.is_authenticated():
                search.user = request.user.profile # if the user is logged in
            search.save()  
            return redirect("/search/"+str(search.id))
    else:
        form = SearchForm()  

    c = {
        'num': len(materials),
        'ratings': ratings,
        'form':form
    }

    return render(request, "search.html", c)


def contact(request):
    c={}
    return render(request, "contact.html", c)


def terms(request):
    c={}
    return render(request, "terms.html", c)


def privacy(request):
    c={}
    return render(request, "privacy.html", c)