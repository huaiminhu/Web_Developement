import random
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage

from tapp.models import Account, Topics
from tapp.forms import ChangeForm, ForgetForm, LoginForm, SignUpForm

from rest_framework.response import Response
from rest_framework import status, viewsets
from tapp.serializers import TopicsSerializer

# Create your views here.

# 首頁
def home(request):
    if request.method == "POST": # Method 為 POST : 取得輸入後站內搜尋, 再導向結果頁面
        request.session["search"] = request.POST["search"]
        return redirect("result")
    return render(request, "home.html")

# 結果頁面
def result(request):
    # 顯示Topics資料表中name欄位(標題)包含首頁輸入的資料
    result = Topics.objects.filter(name__icontains = request.session["search"]).order_by("-date")
    data_total_num = len(result) # 顯示符合資料總數量
    page_n = request.GET.get("page", 1)
    p = Paginator(result, 20) # 換頁功能
    try:
        page = p.page(page_n)
    except EmptyPage:
        page = p.page(1)
    return render(request, "result.html", {"word" : request.session["search"],
                                                "data_total_num" : data_total_num,
                                                "page" : page})

# 健康飲食議題頁
def health(request):
    # 找出Topics資料表中分類為健康飲食的資料
    data = Topics.objects.filter(category = "健康飲食").order_by("-date")
    data_total_num = len(data)
    page_n = request.GET.get("page", 1)
    p = Paginator(data, 20)
    try:
        page = p.page(page_n)
    except EmptyPage:
        page = p.page(1)
    return render(request, "health.html", {"data_total_num" : data_total_num,
                                           "page" : page})

# 國際情勢議題頁
def world(request):
    data = Topics.objects.filter(category = "國際情勢").order_by("-date")
    data_total_num = len(data)
    page_n = request.GET.get("page", 1)
    p = Paginator(data, 20)
    try:
        page = p.page(page_n)
    except EmptyPage:
        page = p.page(1)
    return render(request, "world.html", {"data_total_num" : data_total_num,
                                           "page" : page})

# 氣候環境議題頁
def environment(request):
    data = Topics.objects.filter(category = "氣候環境").order_by("-date")
    data_total_num = len(data)
    page_n = request.GET.get("page", 1)
    p = Paginator(data, 20)
    try:
        page = p.page(page_n)
    except EmptyPage:
        page = p.page(1)
    return render(request, "environment.html", {"data_total_num" : data_total_num,
                                           "page" : page})

# 科學科技議題頁
def science(request):
    data = Topics.objects.filter(category = "科學科技").order_by("-date")
    data_total_num = len(data)
    page_n = request.GET.get("page", 1)
    p = Paginator(data, 20)
    try:
        page = p.page(page_n)
    except EmptyPage:
        page = p.page(1)
    return render(request, "science.html", {"data_total_num" : data_total_num,
                                           "page" : page})

# 主功能頁
def main(request):
    if request.session.has_key("username"): # 有username的session才能進入

        user = request.session["username"]
        user = user[:user.find("@")] # 顯示user名稱在頁面上
        return render(request, "main.html", {"user" : user,
                                            })

    return redirect("login") # 沒有session則導向登入頁面

# 註冊頁面
def signup(request):
    if request.method == "POST":
        sign_up_form = SignUpForm(request.POST) # 註冊表單
        username = request.POST["username"] # 取得輸入
        password = request.POST["password"]

        if sign_up_form.is_valid(): # 表單驗證
            account = Account(username = username,
                            password = password
                            )
            account.save() # 創建(Create)帳戶
            return redirect("login") # 創建成功則導向登入頁面
        else: # 驗證失敗則顯示錯誤訊息
            clear_errors = sign_up_form.errors.get("__all__")
            response = render(request, "signup.html", {"form": sign_up_form,
                                                        "username" : username,
                                                       "clear_errors" : clear_errors})
            response.set_cookie("username", username)
            return response

    sign_up_form = SignUpForm()
    return render(request, "signup.html", {"form": sign_up_form,
                                           "username" : ""
                                           })

# 登入頁面
def login(request):

    if request.session.has_key("username"):
        return redirect("main") # 若有username的session則直接導向主功能頁

    if request.method == "POST":
        login_form = LoginForm(request.POST) # 登入表單
        username = request.POST["username"]

        if login_form.is_valid():
            request.session["username"] = username # 表單若通過驗證就建立username的session
            return redirect("main") # 成功登入則導向主功能頁
        else:
            response = render(request, "login.html", {"form": login_form,
                                                      "username" : username})
            response.set_cookie("username", username)
            return response

    login_form = LoginForm()
    return render(request, "login.html", {"form": login_form, "username" : ""})

# 忘記密碼頁面
def forget(request):
    if request.method == "POST":
        forget_form = ForgetForm(request.POST) # 忘記密碼表單
        username = request.POST["username"]

        if forget_form.is_valid():
            # 產生新密碼
            new_password = '{}'.format(chr(random.randint(97, 122)))
            for i in range(3):
                new_password += '{}'.format(random.randint(0, 9))
                new_password += '{}'.format(chr(random.randint(65, 90)))
            new_password += '{}'.format(chr(random.randint(97, 122)))
            # 寄送新密碼給使用者
            res = send_mail("新密碼通知",
                            "你的新密碼:{}".format(new_password),
                            "hankhuwm@gmail.com", [username])
            if res == 1:
                user = Account.objects.get(username = username)
                user.password = new_password # 把使用者原密碼改為新產生的密碼
                user.save()
                return render(request, "forget.html", {"form" : forget_form,
                                            "username" : username,
                                            "message" : "新密碼寄到你的信箱溜~"})
            else:
                return render(request, "forget.html", {"form" : forget_form,
                                            "username" : username,
                                            "message" : "新密碼寄送失敗 !"})
        else:
            response = render(request, "forget.html", {"form": forget_form,
                                                        "username" : username,
                                                       "message" : ""})
            response.set_cookie("username", username)
            return response

    forget_form = ForgetForm()
    return render(request, "forget.html", {"form" : forget_form,
                                           "username" : "",
                                           "message" : ""})

# 更改密碼頁面
def change(request):
    if request.session.has_key("username"): # 有username的session才能進入
        if request.method == "POST":
            change_form = ChangeForm(request.POST) # 更改密碼表單
            origin = request.POST["origin"] # 取得輸入的原密碼
            new_password = request.POST["newpw"] # 取得輸入的新密碼
            if change_form.is_valid():
                user = Account.objects.get(password = origin)
                user.password = new_password
                user.save()
                return redirect("login") # 經驗證後成功修改密碼並導向登入頁面
            else:
                clear_errors = change_form.errors.get("__all__")
                return render(request, "change.html", {"form" : change_form,
                                                    "clear_errors" : clear_errors})
        change_form = ChangeForm()
        return render(request, "change.html", {"form" : change_form})
    return redirect("login")

# 登出頁面
def logout(request):
    if request.session.has_key("username"):
        try:
            del request.session["username"] # 刪除username的session後登出
        except:
            pass
        return render(request, "logout.html")
    return redirect("login")

from rest_framework.permissions import IsAuthenticated

# RESTful API
class TopicsViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = TopicsSerializer

    def get_permissions(self): # CUD方法需經驗證才能使用
        if self.action in ('create',"update", "delete", ):
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def post(self, request): # POST METHOD
        serializer = TopicsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get_topic_by_pk(self, pk): # 找出主鍵與EndPoint符合的資料
        try:
            return Topics.objects.get(self.queryset, pk = pk)
        except:
            return Response({
                "error" : "沒有這個ID的資料!"
                }, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk): # GET METHOD
        topic = self.get_topic_by_pk(pk)
        serializer = TopicsSerializer(topic)
        return Response(serializer.data)

    def put(self, request, pk): # PUT METHOD
        topic = self.get_topic_by_pk(pk)
        serializer = TopicsSerializer(topic, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk): # DELETE METHOD
        topic = self.get_topic_by_pk(pk)
        topic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)