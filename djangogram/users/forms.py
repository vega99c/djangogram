from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField


User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

#직접 만든 폼
class SignUpForm(django_forms.ModelForm):
    # 사용할 모델 and 화면에 보여질 필드들을 추가해준다.
    class Meta:
        model = User
        fields =[
            'email',
            'name',
            'username',
            'password'
        ]
        # labels = {
        #     'email':'이메일주소',
        #     'name':'성명',
        #     'username':'사용자 이름',
        #     'password':'비밀번호'
        # }
        #비번 *로 처리
        widgets = {
            # 'password' : django_forms.PasswordInput(),
            'email' : django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'name' : django_forms.TextInput(attrs={'placeholder': '성명'}),
            'username' : django_forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password' : django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
