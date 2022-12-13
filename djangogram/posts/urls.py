from django.urls import path
from . import views

app_name = 'posts'

# path 함수 인자를 설명하자면 첫번째 인자는 url패턴을 가진 문자열,
# 두번째는 처리할 뷰, 세번째는 kwargs인데 임의의 키워드 인수들을 뷰에 딕셔너리 형태로 전달
# 그리고 네번째가 name인데 이는 템플릿을 포함한 장고 어디에서나 명확하게 참조가 가능한 속성이다.
# 네번째 인자인 name을 html 템플릿에서 app_name:name 형태로 호출하게 되는것임.
# <예시>
# <a href="{% url 'posts:comment_delete' comment.id %}">
urlpatterns = [
    # /posts/
    path('', views.index, name='index'),

    # /posts/create/
    path('create/', views.post_create, name='post_create'),

    # /posts/1/update/
    path('<int:post_id>/update', views.post_update, name="post_update"),

    # /posts/1/comment_create/ 엘리어스는 3번째 파라미터로 전달
    path('<int:post_id>/comment_create', views.comment_create, name="comment_create"),

    # /posts/1/comment_delete/
    path('<int:comment_id>/comment_delete', views.comment_delete, name="comment_delete"),

    # /posts/5/post_like/
    path('<int:post_id>/post_like', views.post_like, name="post_like"),    

    # /posts/search/
    path('search/', views.search, name="post_search"),
] 