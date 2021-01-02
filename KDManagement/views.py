from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
import pyodbc


def sign(request):
    ctl={}
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if len(username)>10:
            ctl["msg"]="用户名过长，请限制在10字节内"
        else:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from userAndPassword where username='" + username + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 1:
                ctl["msg"] = "该用户名已存在"
            else:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "insert into userAndPassword(username, psw) values('%s', '%s')"
                data = (username, password)
                cursor.execute(sql % data)
                conn.commit()
                sql="insert into personInfo(username,sexy,age,number) values('%s','','','')"
                data=(username)
                cursor.execute(sql % data)
                conn.commit()
                conn.close()
                ctl["msg"] = "注册成功"
    return render(request,"sign.html",ctl)
def mainpage(request):
    return redirect('/login')
def login(request):
    ctl = {}
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select msg from config where getid='1'"
    cursor.execute(sql)
    row = cursor.fetchone()
    row = list(row)[0]
    row = row.split()
    if row:
        row=row[0]
    else:
        row=''
    ctl["info"]=row
    conn.close()
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "update config set username='',psw='',idt='',msg='' where getid='1'"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    if request.POST:
        username=request.POST["username"]
        password=request.POST["password"]
        identity=request.POST["identity"]
        if identity=="用户":
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from userAndPassword where username='"+username+"'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row==1:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select psw from userAndPassword where username='"+username+"'"
                cursor.execute(sql)
                row = cursor.fetchone()
                row=list(row)[0]
                conn.close()
                if row.strip()==password.strip():
                    conn = pyodbc.connect(
                        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                    cursor = conn.cursor()
                    sql = "update config set username='%s',psw='%s',idt='0',msg='' where getid='1'"
                    data=(username,password)
                    cursor.execute(sql % data)
                    conn.commit()
                    conn.close()
                    return redirect('/userMain')
                else:
                    ctl["info"]="密码错误"
            else:
                ctl["info"]="查无此用户"
        elif identity=="快递员":
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from kuaidiyuan where userid='" + username + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 1:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select psw from kuaidiyuan where userid='" + username + "'"
                cursor.execute(sql)
                row = cursor.fetchone()
                row = list(row)[0]
                conn.close()
                if row.strip() == password.strip():
                    conn = pyodbc.connect(
                        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                    cursor = conn.cursor()
                    sql = "update config set username='%s',psw='%s',idt='1',msg='' where getid='1'"
                    data = (username, password)
                    cursor.execute(sql % data)
                    conn.commit()
                    conn.close()
                    return redirect('/kdyMain')
                else:
                    ctl["info"] = "密码错误"
            else:
                ctl["info"] = "查无此快递员"
        elif identity=="管理员":
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from simplemanager where userid='" + username + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 1:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select psw from simplemanager where userid='" + username + "'"
                cursor.execute(sql)
                row = cursor.fetchone()
                row = list(row)[0]
                conn.close()
                if row.strip() == password.strip():
                    conn = pyodbc.connect(
                        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                    cursor = conn.cursor()
                    sql = "update config set username='%s',psw='%s',idt='2',msg='' where getid='1'"
                    data = (username, password)
                    cursor.execute(sql % data)
                    conn.commit()
                    conn.close()
                    return redirect('/adminMain')
                else:
                    ctl["info"] = "密码错误"
            else:
                ctl["info"] = "查无此管理员"
        elif identity=="超管":
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from supermanager where userid='" + username + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 1:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select psw from supermanager where userid='" + username + "'"
                cursor.execute(sql)
                row = cursor.fetchone()
                row = list(row)[0]
                conn.close()
                if row.strip() == password.strip():
                    conn = pyodbc.connect(
                        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                    cursor = conn.cursor()
                    sql = "update config set username='%s',psw='%s',idt='3',msg='' where getid='1'"
                    data = (username, password)
                    cursor.execute(sql % data)
                    conn.commit()
                    conn.close()
                    return redirect('/superadminMain')
                else:
                    ctl["info"] = "密码错误"
            else:
                ctl["info"] = "查无此超管"
    return render(request,"login.html",ctl)
def userMain(request):
    ctl={}
    if confirm(0):
        return render(request,"userMain.html")
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
def personInfo(request):
    if confirm(0):
        ctl = {}
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select username from config where getid='1'"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        username = row
        sql = "select sexy from personInfo where username='%s'"
        cursor.execute(sql % username)
        row = cursor.fetchone()
        row = list(row)[0]
        sexy = row
        sql = "select age from personInfo where username='%s'"
        cursor.execute(sql % username)
        row = cursor.fetchone()
        row = list(row)[0]
        age = row
        sql = "select number from personInfo where username='%s'"
        cursor.execute(sql % username)
        row = cursor.fetchone()
        row = list(row)[0]
        number = row
        ctl["oldName"] = username
        ctl["oldSexy"] = sexy
        ctl["oldAge"] = age
        ctl["oldNumber"] = number
        conn.close()
        if request.POST:
            sexy = request.POST["sexy"]
            sexy = sexy.split()[0]
            age = request.POST["age"]
            age = age.split()[0]
            number = request.POST["number"]
            number = number.split()[0]
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "update personInfo set sexy='%s',age='%s',number='%s' where username='%s'"
            data = (sexy, age, number, username)
            cursor.execute(sql % data)
            conn.commit()
            conn.close()
            ctl["oldSexy"] = sexy
            ctl["oldAge"] = age
            ctl["oldNumber"] = number
            ctl["msg"] = "修改成功！"
        return render(request, "personInfo.html", ctl)
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
def complaint(request):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select username from config where getid='1'"
    cursor.execute(sql)
    row = cursor.fetchone()
    row = list(row)[0]
    username = row
    conn.close()
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select content,respose,condition from complaint where username='%s'"
    cursor.execute(sql % username)
    row = cursor.fetchone()
    ctl = {}
    allContent = []
    while row:
        rowdict = {}
        content = list(row)[0]
        content=content.replace(' ','')
        respose = list(row)[1].split()
        if not respose:
            respose = ''
        else:
            respose=respose[0]
        condition = list(row)[2]
        rowdict["content"] = content
        rowdict["respose"] = respose
        rowdict["condition"] = condition
        allContent.append(rowdict)
        row = cursor.fetchone()
    conn.close()
    ctl["allContent"] = allContent
    if request.POST:
        content = request.POST["content"]
        if content:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "insert into complaint(username, content,respose,condition) values('%s', '%s','','False')"
            data = (username, content)
            cursor.execute(sql % data)
            conn.commit()
            conn.close()
            ctl["msg"]="提交成功！"
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select content,respose,condition from complaint where username='%s'"
            cursor.execute(sql % username)
            row = cursor.fetchone()
            ctl = {}
            allContent = []
            while row:
                rowdict = {}
                content = list(row)[0]
                content = str(content).replace(' ', '')
                respose = list(row)[1].split()
                if not respose:
                    respose = ''
                else:
                    respose = respose[0]
                condition = list(row)[2]
                rowdict["content"] = content
                rowdict["respose"] = respose
                rowdict["condition"] = condition
                allContent.append(rowdict)
                row = cursor.fetchone()
            conn.close()
            ctl["allContent"] = allContent
        else:
            ctl["msg"]="请输入内容！"
    return render(request,"conplaint.html",ctl)
def confirm(idt):
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select idt from config where getid='1'"
    cursor.execute(sql)
    row = cursor.fetchone()
    row = list(row)[0]
    conn.close()
    if row==idt:
        return True
    else:
        return False
    """每当进入一个页面应当做一次身份验证，以确保安全，如果跨类型前往页面，会有idt错误，如果是公用页面，因为提交时需要快递单号或者寄件人姓名，所以无妨
        所以只需要验证私有页面的idt即可"""
def addKD(request):
    ctl={}
    if confirm(0):
        s="<a href='/userMain'>返回个人管理界面</a>"
        ctl["return"]=s
    if confirm(1):
        s="<a href='/kdyMain'>返回快递员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select username from config where getid='1'"
    cursor.execute(sql)
    row = cursor.fetchone()
    conn.close()
    if not row:
        ctl["msg"]="请先登陆！"
        return render(request,"addKD.html",ctl)
    row=list(row)[0]
    if confirm(0):
        ctl["username"]=row
    if request.POST:
        username = request.POST["username"]
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from userAndPassword where username='" + username + "'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row==0:
            ctl["msg"]="请先注册"
            return render(request, "addKD.html", ctl)
        id = request.POST["id"]
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from kuaidi where id='" + id + "'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row==1:
            ctl["msg"]="该单号已存在"
            return render(request,"addKD.html",ctl)
        receiver = request.POST["receiver"]
        sourcePlace = request.POST["sourcePlace"]
        destination = request.POST["destination"]
        content = request.POST["content"]
        a=list()
        a.append(username)
        a.append(id)
        a.append(receiver)
        a.append(sourcePlace)
        a.append(destination)
        a.append(content)
        if not all(a):
            ctl["msg"]="不得空缺"
            return render(request,"addKD.html",ctl)
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "insert into kuaidi(id,username, receiver,sourcePlace,destination,condition,networkName,content,problem) values('%s','%s','%s','%s','%s','已接收','%s','%s','False')"
        data = (id,username,receiver,sourcePlace,destination,sourcePlace,content)
        cursor.execute(sql % data)
        conn.commit()
        conn.close()
        ctl["msg"] = "寄件成功"


    return render(request,"addKD.html",ctl)
def searchKDbyusername(request):
    ctl={}
    meto=[]
    tome=[]
    if not confirm(0):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select username from config where getid='1'"
    cursor.execute(sql)
    name = cursor.fetchone()
    name = list(name)[0]
    sql = "select id,receiver,destination,condition,networkname,content from kuaidi where username='%s'"
    cursor.execute(sql % name)
    row = cursor.fetchone()
    while row:
        rowdict = {}
        id = list(row)[0].split()[0]
        receiver=list(row)[1].split()[0]
        destination=list(row)[2].split()[0]
        condition=list(row)[3].split()[0]
        networkName=list(row)[4].split()[0]
        content=list(row)[5].split()[0]
        rowdict["id"]=id
        rowdict["receiver"]=receiver

        rowdict["destination"]=destination
        rowdict["condition"]=condition
        rowdict["networkName"]=networkName
        rowdict["content"]=content
        row = cursor.fetchone()
        meto.append(rowdict)
    sql = "select id,username,destination,condition,networkname,content from kuaidi where receiver='%s'"
    cursor.execute(sql % name)
    row = cursor.fetchone()
    while row:
        rowdict = {}
        id = list(row)[0].split()[0]
        username = list(row)[1].split()[0]
        destination = list(row)[2].split()[0]
        condition = list(row)[3].split()[0]
        networkName = list(row)[4].split()[0]
        content = list(row)[5].split()[0]
        rowdict["id"] = id
        rowdict["username"] = username
        rowdict["networkName"]=networkName

        rowdict["destination"] = destination
        rowdict["condition"] = condition
        rowdict["content"] = content
        row = cursor.fetchone()
        tome.append(rowdict)
    conn.close()
    ctl["meto"]=meto
    ctl["tome"]=tome
    return render(request,"searchKDbyusername.html",ctl)
def searchKD(request):
    ctl={}
    if confirm(0):
        s="<a href='/userMain'>返回个人管理界面</a>"
        ctl["return"]=s
    if confirm(1):
        s="<a href='/kdyMain'>返回快递员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    if request.POST:
        id=request.POST["id"]
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from kuaidi where id='" + id + "'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row==0:
            ctl["msg"]="查无此单号"
        else:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select username,receiver,sourcePlace,destination,content,condition,networkName from kuaidi where id='%s'"
            cursor.execute(sql % id)
            row = cursor.fetchone()
            ctl["username"]=list(row)[0].split()[0]
            ctl["receiver"]=list(row)[1].split()[0]
            ctl["sourcePlace"]=list(row)[2].split()[0]
            ctl["destination"]=list(row)[3].split()[0]
            ctl["content"]=list(row)[4].split()[0]
            ctl["condition"]=list(row)[5].split()[0]
            ctl["networkName"]=list(row)[6].split()[0]
            conn.close()
    return render(request,"searchKD.html",ctl)
def kdyMain(request):
    ctl = {}
    if confirm(1):
        return render(request, "kdyMain.html")
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
def updateKD(request):
    ctl={}
    if confirm(1):
        s="<a href='/kdyMain'>返回快递员管理界面</a>"
        ctl["return"]=s
    elif confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if request.POST:
        if 'query' in request.POST:
            id = request.POST["id"]
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from kuaidi where id='" + id + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                ctl["msg"] = "查无此单号"
            else:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select username,receiver,sourcePlace,destination,content,condition,networkName,problem from kuaidi where id='%s'"
                cursor.execute(sql % id)
                row = cursor.fetchone()
                ctl["username"] = list(row)[0].split()[0]
                ctl["receiver"] = list(row)[1].split()[0]
                ctl["sourcePlace"] = list(row)[2].split()[0]
                ctl["destination"] = list(row)[3].split()[0]
                ctl["content"] = list(row)[4].split()[0]
                ctl["condition"] = list(row)[5].split()[0]
                ctl["networkName"] = list(row)[6].split()[0]
                ctl["problem"] = list(row)[7]
                ctl["id"]=id
                conn.close()
        if 'update' in request.POST:
            id=request.POST["id"]
            condition=request.POST["condition"]
            networkName=request.POST["networkName"]
            problem=request.POST["problem"]
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "update kuaidi set condition='%s',networkName='%s',problem='%s' where id='%s'"
            data = (condition, networkName,problem,id)
            cursor.execute(sql % data)
            conn.commit()
            conn.close()
            ctl["msg"]="修改成功！"
    return render(request,"updateKD.html",ctl)
def adminMain(request):
    if confirm(2):
        return render(request,"adminMain.html")
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
def addKDY(request):
    ctl={}
    if not (confirm(2) or confirm(3)):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(2):
        s="<a href='/adminMain'>返回管理员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    if request.POST:
        userid=request.POST["userid"]
        psw=request.POST["psw"]
        if len(userid)>20:
            ctl["msg"]="快递员id过长，请限制在10字节内"
        else:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from kuaidiyuan where userid='" + userid + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 1:
                ctl["msg"] = "该id已存在"
            else:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "insert into kuaidiyuan(userid, psw) values('%s', '%s')"
                data = (userid, psw)
                cursor.execute(sql % data)
                conn.commit()
                conn.close()
                ctl["msg"] = "新增成功"
    return render(request,"addKDY.html",ctl)
def updateKDY(request):
    ctl={}
    if not (confirm(2) or confirm(3)):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(2):
        s="<a href='/adminMain'>返回管理员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    if request.POST:
        userid=request.POST["userid"]
        psw=request.POST["psw"]
        if 'query' in request.POST:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from kuaidiyuan where userid='" + userid + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                ctl["msg"] = "该id不存"
                return render(request, "updateKDY.html", ctl)
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select psw from kuaidiyuan where userid='" + userid + "'"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0].split()[0]
            conn.close()
            ctl["msg"]="查询成功"
            ctl["psw"]=row
            ctl["userid"]=userid
        if 'update' in request.POST:
            if psw=='':
                ctl["msg"]="密码不可为空"
                return render(request,"updateKDY.html",ctl)
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "update kuaidiyuan set psw='%s' where userid='%s'"
            data = (psw,userid)
            cursor.execute(sql % data)
            conn.commit()
            conn.close()
            ctl["msg"]="更新成功"
        if 'delete' in request.POST:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from kuaidiyuan where userid='" + userid + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                ctl["msg"] = "该id不存"
                return render(request, "updateKDY.html", ctl)
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "delete from kuaidiyuan where userid='%s'"
            cursor.execute(sql % userid)
            conn.commit()
            conn.close()
            ctl["msg"]="删除成功"

    return render(request,"updateKDY.html",ctl)
def addNetwork(request):
    ctl={}
    if not (confirm(2) or confirm(3)):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(2):
        s="<a href='/adminMain'>返回管理员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    if request.POST:
        network=request.POST["network"]
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from network where networkName='" + network + "'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row == 1:
            ctl["msg"] = "网点已存在！"
            return render(request, "addNetwork.html", ctl)
        else:
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "insert into network(networkName) values('%s')"
            cursor.execute(sql % network)
            conn.commit()
            conn.close()
            ctl["msg"] = "新增成功"
    return render(request,"addNetwork.html",ctl)
def deleteNetwork(request):
    ctl={}
    if not (confirm(2) or confirm(3)):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(2):
        s="<a href='/adminMain'>返回管理员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    if request.POST:
        network=request.POST["network"]
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from network where networkName='" + network + "'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row == 0:
            ctl["msg"] = "网点不存在！"
            return render(request, "deleteNetwork.html", ctl)
        else:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "delete from network where networkName='%s'"
            cursor.execute(sql % network)
            conn.commit()
            conn.close()
            ctl["msg"] = "删除成功"
    return render(request,"deleteNetwork.html",ctl)
def queryNetwork(request):
    ctl={}
    if not (confirm(2) or confirm(3)):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(2):
        s="<a href='/adminMain'>返回管理员管理界面</a>"
        ctl["return"]=s
    if confirm(3):
        s="<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"]=s
    if request.POST:
        network=request.POST["network"]
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from network where networkName='" + network + "'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row == 0:
            ctl["msg"] = "网点不存在！"
            return render(request, "queryNetwork.html", ctl)
        else:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select count(*) from kuaidi where networkName='%s'"
            cursor.execute(sql % network)
            row = cursor.fetchone()
            row = list(row)[0]
            ctl["number"]=row
            sql = "select count(*) from kuaidi where problem='True' and networkName='%s'"
            cursor.execute(sql % network)
            row = cursor.fetchone()
            row = list(row)[0]
            ctl["problem"]=row
            conn.close()

            ctl["msg"] = "查询成功"
    return render(request,"queryNetwork.html",ctl)
def superadminMain(request):
    if confirm(3):
        return render(request, "superadminMain.html")
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
def addAdmin(request):
    ctl = {}
    if not confirm(3):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(3):
        s = "<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"] = s
    if request.POST:
        userid = request.POST["userid"]
        psw = request.POST["psw"]
        if len(userid) > 20:
            ctl["msg"] = "管理员id过长，请限制在10字节内"
        else:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from simplemanager where userid='" + userid + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 1:
                ctl["msg"] = "该id已存在"
            else:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "insert into simplemanager(userid, psw) values('%s', '%s')"
                data = (userid, psw)
                cursor.execute(sql % data)
                conn.commit()
                conn.close()
                ctl["msg"] = "新增成功"
    return render(request, "addAdmin.html", ctl)
def updateAdmin(request):
    ctl = {}
    if not confirm(3):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(3):
        s = "<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"] = s
    if request.POST:
        userid = request.POST["userid"]
        psw = request.POST["psw"]
        if 'query' in request.POST:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from simplemanager where userid='" + userid + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                ctl["msg"] = "该id不存"
                return render(request, "updateAdmin.html", ctl)
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select psw from simplemanager where userid='" + userid + "'"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0].split()[0]
            conn.close()
            ctl["msg"] = "查询成功"
            ctl["psw"] = row
            ctl["userid"] = userid
        if 'update' in request.POST:
            if psw == '':
                ctl["msg"] = "密码不可为空"
                return render(request, "updateAdmin.html", ctl)
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "update simplemanager set psw='%s' where userid='%s'"
            data = (psw, userid)
            cursor.execute(sql % data)
            conn.commit()
            conn.close()
            ctl["msg"] = "更新成功"
        if 'delete' in request.POST:
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from simplemanager where userid='" + userid + "'), 0)"
            cursor.execute(sql)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                ctl["msg"] = "该id不存"
                return render(request, "updateAdmin.html", ctl)
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "delete from simplemanager where userid='%s'"
            cursor.execute(sql % userid)
            conn.commit()
            conn.close()
            ctl["msg"] = "删除成功"

    return render(request, "updateAdmin.html", ctl)
def handleComplaint(request):
    ctl = {}
    if not (confirm(2) or confirm(3)):
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update config set msg='无访问权限！请先登陆' where getid='1'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    if confirm(2):
        s = "<a href='/adminMain'>返回管理员管理界面</a>"
        ctl["return"] = s
    if confirm(3):
        s = "<a href='/superadminMain'>返回超管管理界面</a>"
        ctl["return"] = s
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select isnull((select top(1) 1 from complaint where condition='False'), 0)"
    cursor.execute(sql)
    row = cursor.fetchone()
    row = list(row)[0]
    conn.close()
    if row==0:
        ctl["exist"]=0
        return render(request,"handleCpmplaint.html",ctl)
    else:
        ctl["exist"]=1
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select top 1 username,content from complaint where condition='False'"
        cursor.execute(sql)
        row = cursor.fetchone()
        ctl["username"] = list(row)[0].split()[0]
        ctl["content"]=list(row)[1].replace(' ','')
    if request.POST:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select top 1 username,content from complaint where condition='False'"
        cursor.execute(sql)
        row = cursor.fetchone()
        username = list(row)[0].split()[0]
        content = list(row)[1].replace(' ','')
        respose=request.POST["respose"]
        sql = "update complaint set respose='%s',condition='True' where username='%s' and content='%s' and condition='False'"
        data=(respose,username,content)
        cursor.execute(sql % data)
        conn.commit()
        conn.close()
        ctl["msg"]="处理成功"
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select isnull((select top(1) 1 from complaint where condition='False'), 0)"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row == 0:
            ctl["exist"] = 0
            return render(request, "handleCpmplaint.html", ctl)
        else:
            ctl["exist"] = 1
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=kuaidi;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select top 1 username,content from complaint where condition='False'"
            cursor.execute(sql)
            row = cursor.fetchone()
            ctl["username"] = list(row)[0].split()[0]
            ctl["content"] = list(row)[1].replace(' ','')
    return render(request, "handleCpmplaint.html", ctl)
