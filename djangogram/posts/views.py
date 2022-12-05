from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model

from . import models, serializers
from.forms import CreatePostForm

# Create your views here.
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                # 팔로잉 하는 유저들과 포스팅한 유저를 가져옴 Q객체는 공식문서에서 다시보자
                Q(author__in=following) | Q(author=user)
            )

            serializer = serializers.PostSerializer(posts, many=True)

            return render(request, 'posts/main.html', {"posts" : serializer.data})    
    

def post_create(request):
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form":form})

    elif request.method == 'POST': 
        #유저 인증 절차
        if request.user.is_authenticated:
            # user.id를 이용해서 유저 참조
            user = get_object_or_404(user_model, pk=request.user.id)
            #사용자로부터 생성 요청받은 이미지와 캡션
            # image = request.FILES['image']
            # caption = request.POST['caption']

            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )

            # new_post.save()

            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                # commit False 하면 일단은 DB에 저장되지 않는 상태임
                post = form.save(commit=False)
                post.author = user
                post.save()
            else:
                print(form.errors)

            return render(request, 'posts/main.html')
        else:
            return render(request, 'users/main.html')
