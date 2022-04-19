from django.shortcuts import render
import pymongo
from django.core.paginator import Paginator
from pymongo import MongoClient
from django.db.models import Q
# Create your views here.

id = 'ttony0321'
password = 'pang0228!'
url = 'mongodb+srv://'+id+':'+password+'@boardlist.lfr3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

client = pymongo.MongoClient(url)
db = client.boardList



def index(request):
    page = request.GET.get('page', '1')
    a_posts = db.All.find({}).sort('date', -1)
    a_l_posts = list(a_posts)
    #MongoDB는 Cursor 타입, paginator은 지원 안됨
    mdb = request.GET.get('mdb', '')#검색하기위하여 입력한 값
    if mdb:
        a_l_posts = list(db.All.find({"title":{'$regex':mdb,'$options':'i'}}))
    paginator = Paginator(a_l_posts, 10)
    page_obj = paginator.get_page(page)
    print(type(a_l_posts))
    context = {'a_posts':page_obj, 'mdb':mdb}
    return render(request, 'board_list/board_list.html', context)

def comments_index(request):
    page = request.GET.get('page', '1')
    a_posts = db.All.find({}).sort('comments', -1)
    a_l_posts = list(a_posts)
    #MongoDB는 Cursor 타입, paginator은 지원 안됨
    mdb = request.GET.get('mdb','')
    if mdb:
        a_l_posts = list(db.All.find({"title":{'$regex':mdb,'$options':'i'}}))
    paginator = Paginator(a_l_posts, 10)
    page_obj = paginator.get_page(page)
    print(type(a_l_posts))
    context = {'a_posts':page_obj, 'mdb':mdb}
    return render(request, 'board_list/board_list_com.html', context)

def view_index(request):
    page = request.GET.get('page', '1')
    a_posts = db.All.find({}).sort('viewers', -1)
    a_l_posts = list(a_posts)
    #MongoDB는 Cursor 타입, paginator은 지원 안됨
    mdb = request.GET.get('mdb', '')
    if mdb:
        a_l_posts = list(db.All.find({"title": {'$regex': mdb,'$options':'i'}}))
    paginator = Paginator(a_l_posts, 10)
    page_obj = paginator.get_page(page)
    print(type(a_l_posts))
    context = {'a_posts':page_obj, 'mdb':mdb}
    return render(request, 'board_list/board_list_vie.html', context)

def theqoo(request):
    posts = db.Theqoo.find({}).sort('date', -1)
    l_posts = list(posts)
    mdb = request.GET.get('mdb', '')
    if mdb:
        l_posts = list(db.Theqoo.find({"title": {'$regex': mdb,'$options':'i'}}))
    paginator = Paginator(l_posts, 10)
    page = request.GET.get('page', '1')
    page_obj = paginator.get_page(page)
    context = {'l_posts':page_obj, 'mdb':mdb}
    return render(request, 'board_list/board_list_Theqoo.html', context)

def fmkorea(request):
    page = request.GET.get('page', '1')
    f_posts = db.FMKorea.find({}).sort('date', -1)
    f_l_posts = list(f_posts)
    mdb = request.GET.get('mdb', '')
    if mdb:
        f_l_posts = list(db.FMKorea.find({"title": {'$regex': mdb,'$options':'i'}}))
    paginator = Paginator(f_l_posts, 10)
    page_obj = paginator.get_page(page)
    context = {'f_l_posts': page_obj, 'mdb':mdb}
    return render(request, 'board_list/board_list_FmKorea.html', context)

def humor(request):
    page = request.GET.get('page', '1')
    h_posts = db.Humoruni.find({}).sort('date', -1)
    h_l_posts = list(h_posts)
    mdb = request.GET.get('mdb', '')
    if mdb:
        h_l_posts = list(db.Humoruni.find({"title": {'$regex': mdb,'$options':'i'}}))
    paginator = Paginator(h_l_posts, 10)
    page_obj = paginator.get_page(page)
    context = {'h_l_posts': page_obj, 'mdb':mdb}
    return render(request, 'board_list/board_list_Humor.html', context)

