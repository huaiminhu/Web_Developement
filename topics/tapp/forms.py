from django import forms
from django.core.exceptions import ValidationError
from tapp.models import Account
import re

# 登入表單
class LoginForm(forms.Form):

    username = forms.CharField(max_length=20)
    password = forms.CharField(widget = forms.PasswordInput())

    def clean_username(self): # 使用者驗證
        username = self.cleaned_data["username"]
        dbuser = Account.objects.filter(username = username)

        if not dbuser:
            raise ValidationError("查無此人")

    def clean_password(self): # 密碼驗證
        password = self.cleaned_data["password"]
        dbuser = Account.objects.filter(password = password)

        if not dbuser:
            raise ValidationError("密碼打錯了 !")

# 註冊表單
class SignUpForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(min_length=8, widget = forms.PasswordInput())
    pws_check = forms.CharField(min_length=8, widget = forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"]
        dbuser = Account.objects.filter(username = username)

        if dbuser:
            raise ValidationError("這名稱有人用過了 !")

    def clean(self): # 驗證兩次輸入的密碼有無一致
        password = self.cleaned_data.get("password")
        pws_check = self.cleaned_data.get("pws_check")
        pattern1 = "[A-Z]+"
        try:
            pattern_check1 = re.findall(pattern1, password)
            pattern_check2 = re.findall(pattern1, pws_check)
        except:
            return

        if len(pattern_check1) < 1 or len(pattern_check2) < 1:
            raise ValidationError("密碼要有大寫英文字母 !")
        elif password != pws_check:
            raise ValidationError("兩次密碼不一樣 !")

# 忘記密碼表單
class ForgetForm(forms.Form):

    username = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        dbuser = Account.objects.filter(username = username)

        if "@" not in username:
            raise ValidationError("格式不對 !")
        elif not dbuser:
            raise ValidationError("這個username沒有帳戶 !")

# 更改密碼表單
class ChangeForm(forms.Form):

    origin = forms.CharField(widget = forms.PasswordInput())
    newpw = forms.CharField(min_length=8, widget = forms.PasswordInput())
    again = forms.CharField(min_length=8, widget = forms.PasswordInput())

    def clean_origin(self): # 驗證輸入的原密碼有無存在於資料庫
        origin = self.cleaned_data["origin"]
        dbpw = Account.objects.filter(password = origin)

        if not dbpw:
            raise ValidationError("密碼錯了 !")

    def clean(self):
        cleaned_data = super().clean()
        newpw = cleaned_data.get("newpw")
        again = cleaned_data.get("again")
        pattern2 = "[A-Z]+"
        try:
            pattern_check1 = re.findall(pattern2, newpw)
            pattern_check2 = re.findall(pattern2, again)
        except:
            return

        if len(pattern_check1) < 1 or len(pattern_check2) < 1:
            raise ValidationError("密碼要有大寫英文字母 !")
        elif newpw != again:
            raise ValidationError("兩次密碼不一樣 !")