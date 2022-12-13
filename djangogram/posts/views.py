from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse

from djangogram.users.models import User as user_model
from . import models, serializers
from.forms import CreatePostForm, CommentForm, UpdatePostForm

# Create your views here.
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            comment_form = CommentForm()
            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                # 팔로잉 하는 유저들과 포스팅한 유저를 가져옴 Q객체는 공식문서에서 다시보자
                Q(author__in=following) | Q(author=user)
            ).order_by("updated_at") 
            # Post클래스가 상속받는 TimeStamedModel의 필드값임. -붙이면 내림차순 정렬

            serializer = serializers.PostSerializer(posts, many=True)

            return render(
                request,
                'posts/main.html', 
                # 템플릿에서 참조 할 이름을 ""로 명시
                {"posts" : serializer.data, "comment_form" : comment_form}
            )

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
            #요청받은 포스트 데이터와 파일을 폼에 넘겨주고 새 폼을 생성한 후에 저장
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

def post_update(request, post_id):
    if request.user.is_authenticated:        
        # 작성자 체크
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user != post.author:
            return redirect(reverse('posts:index'))

        # 수정을 위한 페이지를 리턴

        if request.method == 'GET':
            # instance에 위에서 추출한 post 데이터를 인자로 넣어줌으로써
            # 해당 post 내용이 표기 될 수 있음.
            # 값을 가지고 있는 인스턴스를 넘겨줌으로써
            # 해당 form 의 필드에 값이 알아서 채워진다고 생각하면 된다.
            form = UpdatePostForm(instance=post)
            return render(
                request,
                'posts/post_update.html',
                {"form" : form, "post" : post}
            )
        elif request.method == 'POST':
            form = UpdatePostForm(request.POST)
            if form.is_valid():
                post.caption = form.cleaned_data['caption']
                post.save()
            
            return redirect(reverse('posts:index'))
            

    else:
        return render(request, 'users/main.html')
    
def comment_create(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.posts = post
            comment.save()

            return redirect(reverse('posts:index') + "#comment-" + str(comment.id))
        else:
            return render(request, 'users/main.html')


def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()

        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')

def post_like(request, post_id):
    response_body = {"result": ""}

    if request.user.is_authenticated:
        if request.method == "POST":
            
            post = get_object_or_404(models.Post, pk=post_id)        
            existed_user = post.image_likes.filter(pk=request.user.id).exists()

            if existed_user:
                #이미 좋아요 눌렀으면 취소
                post.image_likes.remove(request.user)
                response_body["result"] = "dislike"
            else:
                post.image_likes.add(request.user)
                response_body["result"] = "like"
                #아니면 좋아요 승인
                
            post.save()
            return JsonResponse(status=200, data=response_body)
    else:
        return JsonResponse(status=403, data=response_body)


def search(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            searchKeyword = request.GET.get("q", "")
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                # 팔로잉 하는 유저들과 포스팅한 유저를 가져옴 Q객체는 공식문서에서 다시보자
                (Q(author__in=following) | Q(author=user)) & Q(caption__contains=searchKeyword)
            ).order_by("updated_at")
            # Post클래스가 상속받는 TimeStamedModel의 필드값임. -붙이면 내림차순 정렬

            serializer = serializers.PostSerializer(posts, many=True)
            print(serializer.data)

            return render(
                request,
                'posts/main.html', 
                # 템플릿에서 참조 할 이름을 ""로 명시
                {"posts" : serializer.data, "comment_form" : comment_form}
            )
    else:
        return render(request, 'users/main.html')