from django.db import models

class ProductModel(models.Model):
    # 產品名稱
    pname = models.CharField(max_length=100, default='')

    # 產品價格
    pprice = models.IntegerField(default=0)

    # 產品圖片
    pimages = models.CharField(max_length=100, default='')

    # 產品描述
    pdescription = models.TextField(blank=True, default='')

    def __str__(self):
        return self.pname



class DetailModel(models.Model):
    # 訂單關聯：這是一個外部鍵，將詳細資料關聯到相應的訂單。
    dorder = models.ForeignKey('OrdersModel', on_delete=models.CASCADE)
    
    # 產品名稱
    pname = models.CharField(max_length=100, default='')

    # 單價
    unitprice = models.IntegerField(default=0)

    # 數量
    quantity = models.IntegerField(default=0)

    # 明細總金額
    dtotal = models.IntegerField(default=0)

    def __str__(self):
        return self.pname
    
    
class OrdersModel(models.Model):
    # 訂單小計
    subtotal = models.IntegerField(default=0)
    
    # 運費
    shipping = models.IntegerField(default=0)
    
    # 訂單總金額
    grandtotal = models.IntegerField(default=0)
    
    # 客戶姓名
    customname = models.CharField(max_length=100, default='')

    # 客戶電子郵件
    customemail = models.CharField(max_length=100, default='')

    # 客戶地址
    customaddress = models.CharField(max_length=100, default='')

    # 客戶電話號碼
    customphone = models.CharField(max_length=100, default='')

    # 付款類型
    paytype = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.customname