from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase



class TestPosts(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username = 'good', email = 'gmadf@vera.com', password='1234'
        )
    
    def test_get_posts_page(self):
        url = reverse('posts:post_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

    def test_post_creating_posts(self):
        login = self.client.login(username='good',password='1234')
        self.assertTrue(login)

        url = reverse('posts:post_create')
        # 서버에 이미지 올릴필요 없이 간단하게 업로드 테스트 할 수 있도록 해줌
        image = SimpleUploadedFile("test.jpg", b"whatevercontents")
        response = self.client.post(
            url,
            {"image":image, "caption": 'test test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/base.html")

    def test_post_posts_not_login(self):
        url = reverse('posts:post_create')
        # 서버에 이미지 올릴필요 없이 간단하게 업로드 테스트 할 수 있도록 해줌
        image = SimpleUploadedFile("test.jpg", b"whatevercontents")
        response = self.client.post(
            url,
            {"image":image, "caption": 'test test'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/main.html")

    