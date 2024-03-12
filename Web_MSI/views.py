from django.shortcuts import render, redirect
from Web_MSI import models
from django.contrib.auth import authenticate
from django.contrib import auth
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from Web_MSI.forms import RegisterForm


message = ''
cartlist = []        # 購買商品串列
customname = ''      # 購買者姓名
customphone = ''     # 購買者電話
customaddress = ''   # 購買者地址
customemail = ''     # 購買者電子郵件

#已登入
#首頁
def index(request):
	return render(request, "index.html", locals())

#品牌故事
def story(request):
	return render(request, "story.html", locals())


#未登入
#首頁
def index2(request):
	return render(request, "index2.html", locals())

#品牌故事
def story2(request):
	return render(request, "story2.html", locals())

#註冊
def sign_up(request):
    messages = ''
    form = UserCreationForm()  # 使用 UserCreationForm
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # 重新導向到登入畫面
        else:
            messages = '註冊失敗 !'
    context = {
        'form': form,
        'messages': messages,
    }
    return render(request, 'register.html', context)


#會員登入
def memberlogin(request):
    messages = ''  # 初始時清除訊息
    form = RegisterForm()        
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:  # 驗證通過
            if user.is_active:  # 帳號有效
                auth.login(request, user)  # 登入
                return redirect('/') # 導入首頁
            else:  # 帳號密碼錯誤
                messages = '帳號密碼錯誤！'
        else:
            messages = '登入失敗，請先註冊！'
    context = {
        'form': form,
        'messages': messages,
    }
    return render(request, 'login.html', context)

#會員登出
def memberlogout(request):
    logout(request)
    return redirect('/login') #重新導向到登入畫面




# 後台管理登入
"""
def login(request):  
	messages = ''  # 初始時清除訊息
	if request.method == 'POST':  # 如果是以POST方式才處理
		name = request.POST['username'].strip()  # 取得輸入帳號
		password = request.POST['password']  # 取得輸入密碼
		user1 = authenticate(username=name, password=password)  # 驗證
		if user1 is not None:  # 驗證通過
			if user1.is_active:  # 帳號有效
				auth.login(request, user1)  # 登入
				return redirect('/adminmain/')  # 開啟管理頁面
			else:  # 帳號無效
				messages = '帳號尚未啟用！'
		else:  # 驗證未通過
			messages = '登入失敗！'
	#return render(request, "login.html", locals())

# 後台管理登出
def logout(request):  
	auth.logout(request)
	#return redirect('/index/')"""



#購物網站(未登入)
def shop2(request):
	global cartlist
	if 'cartlist' in request.session:              # 若 session中存在cartlist就讀出
		cartlist = request.session['cartlist']
	else:                          # 重新購物
		cartlist = []
	cartnum = len(cartlist)        # 購買商品筆數
	productall = models.ProductModel.objects.all() # 取得資料庫所有商品
	return render(request, "shop2.html", locals())


# 商品詳細頁面(未登入)
def detail2(request, productid=None):                         # 商品詳細頁面
	product = models.ProductModel.objects.get(id=productid)  # 取得商品
	return render(request, "detail2.html", locals())


#購物網站(已登入)
def shop(request):
	global cartlist
	if 'cartlist' in request.session:              # 若 session中存在cartlist就讀出
		cartlist = request.session['cartlist']
	else:                          # 重新購物
		cartlist = []
	cartnum = len(cartlist)        # 購買商品筆數
	productall = models.ProductModel.objects.all() # 取得資料庫所有商品
	return render(request, "shop.html", locals())

def detail(request, productid=None):                         # 商品詳細頁面
	product = models.ProductModel.objects.get(id=productid)  # 取得商品
	return render(request, "detail.html", locals())

def cart(request):                 # 顯示購物車
	global cartlist
	cartlist1 = cartlist           # 以區域變數傳給模版
	total = 0
	for unit in cartlist:          # 計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100       # 加入運費總額
	return render(request, "cart.html", locals())

def addtocart(request, ctype=None, productid=None):
	global cartlist
	if ctype == 'add':           # 加入購物車
		product = models.ProductModel.objects.get(id=productid)
		flag = True              # 設檢查旗標為True
		for unit in cartlist:                    # 逐筆檢查商品是否已存在
			if product.pname == unit[0]:         # 商品已存在
				unit[2] = str(int(unit[2])+ 1)   # 數量加1
				unit[3] = str(int(unit[3]) + product.pprice)  # 計算價錢
				flag = False     # 設檢查旗標為False
				break
		if flag:                 # 商品不存在
			temlist = []         #  暫時串列
			temlist.append(product.pname)        # 將商品資料加入暫時串列
			temlist.append(str(product.pprice))  # 商品價格
			temlist.append('1')                  # 先暫訂數量為1
			temlist.append(str(product.pprice))  # 總價
			cartlist.append(temlist)             # 將暫時串列加入購物車
		request.session['cartlist'] = cartlist   # 將購物車寫入session
		return redirect('/cart/')
	elif ctype == 'update':      # 更新購物車
		n = 0
		for unit in cartlist:
			unit[2] = request.POST.get('qty' + str(n), '1')  # 取得數量
			unit[3] = str(int(unit[1]) * int(unit[2]))       # 取得總價
			n += 1
		request.session['cartlist'] = cartlist
		return redirect('/cart/')
	elif ctype == 'empty':       # 清空購物車
		cartlist = []            # 設定購物車為空串列
		request.session['cartlist'] = cartlist
		return redirect('/shop/')
	elif ctype == 'remove':      # 刪除購物車中的商品
		del cartlist[int(productid)]  # 從購物車串列中移除商品
		request.session['cartlist'] = cartlist
		return redirect('/cart/')

def cartorder(request):          # 按我要結帳鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	cartlist1 = cartlist
	total = 0
	for unit in cartlist:        # 計算商品總金額
		total += int(unit[3])
	grandtotal = total + 100
	customname1 = customname     # 以區域變數傳給模版
	customphone1 = customphone
	customaddress1 = customaddress
	customemail1 = customemail
	message1 = message
	return render(request, "cartorder.html", locals())

def cartok(request):             # 按確認購買鈕
	global cartlist, message, customname, customphone, customaddress, customemail
	total = 0
	for unit in cartlist:
		total += int(unit[3])
	grandtotal = total + 100
	message = ''
	customname = request.POST.get('CustomerName', '')
	customphone = request.POST.get('CustomerPhone', '')
	customaddress = request.POST.get('CustomerAddress', '')
	customemail = request.POST.get('CustomerEmail', '')
	paytype = request.POST.get('paytype', '')
	customname1 = customname
	if customname=='' or customphone=='' or customaddress=='' or customemail=='':
		message = '姓名、電話、住址及電子郵件皆需輸入'
		return redirect('/cartorder/')
	else:
		unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, grandtotal=grandtotal, customname=customname, customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype) # 建立訂單
		for unit in cartlist:         # 將購買的商品寫入資料庫
			total = int(unit[1]) * int(unit[2])
			unitdetail = models.DetailModel.objects.create(dorder=unitorder, pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
		orderid = unitorder.id        # 取得訂單id
		mailfrom="brucek688@gmail.com"   # 帳號
		mailpw="fnkj atfr rnln levx"             # 應用程式密碼
		mailto=customemail            # 收件者
		mailsubject="**購物網-網路購物訂單通知";  # 郵件標題
		mailcontent = "感謝您的光臨，您已經成功的完成訂購程序。\n我們將儘快把您選購的商品寄送給您！ 再次感謝您的支持！\n您的訂單編號為：" + str(orderid) + "，您可以使用這個編號回到網站中查詢訂單的詳細內容。\n**購物網" # 郵件內容
		send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent)  # 寄信
		cartlist = []
		request.session['cartlist'] = cartlist
		return render(request, "cartok.html", locals())

def cartordercheck(request):                    # 查詢訂單
	orderid = request.GET.get('orderid', '')    # 取得輸入的 id
	customemail = request.GET.get('customemail', '')  # 取得輸入的 email
	if orderid == '' and customemail == '':     # 按查詢訂單鈕
		firstsearch = 1
	else:
		order = models.OrdersModel.objects.filter(id=orderid).first()
		if order == None or order.customemail != customemail:  # 找不到資料
			notfound = 1
		else:  # 找到符合的資料
			details = models.DetailModel.objects.filter(dorder=order)
	return render(request, "cartordercheck.html", locals())

def send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent): # 寄信
	global message
	strSmtp = "smtp.gmail.com:587" #主機
	strAccount = mailfrom          # 帳號
	strPassword = mailpw           # 密碼
	msg = MIMEText(mailcontent)
	msg["Subject"] = mailsubject   # 郵件標題
	mailto1 = mailto               # 收件者
	server = SMTP(strSmtp)         # 建立 SMTP 連線
	server.ehlo()                  # 跟主機溝通
	server.starttls()              # TTLS 安全認證
	try:
		server.login(strAccount, strPassword)                 # 登入
		server.sendmail(strAccount, mailto1, msg.as_string()) # 寄信
	except SMTPAuthenticationError:
		message = "無法登入！"
	except:
		message = "郵件發送產生錯誤！"
	server.quit() # 關閉連線



