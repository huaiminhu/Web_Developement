from django.db import models

# Create your models here.
class Account(models.Model): # 帳戶模型
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    class Meta:
        db_table = "account"

class Topics(models.Model): # 議題模型

    category = models.CharField(max_length=100) # 議題類別
    name = models.CharField(max_length=100) # 標題
    date = models.CharField(max_length=100)
    resource = models.CharField(max_length=100) # 資料來源
    url = models.CharField(max_length=100) # 資料來源網址
    class Meta:
        db_table = "topics"