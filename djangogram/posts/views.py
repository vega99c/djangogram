from django.shortcuts import render, get_object_or_404
from djangogram.users.models import User as user_model


from . import models

# Create your views here.
def index(request):
    return render(request, 'posts/base.html')

def post_create(request):
    if request.method == 'GET':
        return render(request, 'posts/post_create.html')
    elif request.method == 'POST':
        #유저 인증 절차
        if request.user.is_authenticated:
            # user.id를 이용해서 유저 참조
            user = get_object_or_404(user_model, pk=request.user.id)
            #사용자로부터 생성 요청받은 이미지와 캡션
            image = request.FILES['image']
            caption = request.POST['caption']

            new_post = models.Post.objects.create(
                author = user,
                image = image,
                caption = caption
            )

            new_post.save()

            return render(request, 'posts/base.html')
        else:
            return render(request, 'users/main.html')
