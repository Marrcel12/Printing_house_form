from flask import Flask, render_template, request,session,redirect,url_for
from flask_mail import Mail, Message
import base64
import psycopg2
import os
import random
app = Flask(__name__)
app.config['SECRET_KEY']= 'qaz123'
app.config['TEMPLATES_AUTO_RELOAD'] = True
# mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'polishprinthouse72@gmail.com'  
app.config['MAIL_DEFAULT_SENDER'] = 'polishprinthouse72@gmail.com' 
app.config['MAIL_PASSWORD'] = 'y5?r/)Dyy6\/' 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# login 
def login_database(sql):
    conn = psycopg2.connect(database="drukarnia", user = "postgres", password = "qaz123", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    passwords=[]
    for row in rows:
        passwords.append(row[0])
    conn.close()
    return passwords
    
# database
def bazkie_produkty(sql):
    conn = psycopg2.connect(database="drukarnia", user = "postgres", password = "qaz123", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    products=[]
    for row in rows:
        products.append(row[0])
    conn.close()
    return products
def bazkie_produkty_route(sql,product):
    sql= sql.replace('itemname',product)
    conn = psycopg2.connect(database="drukarnia", user = "postgres", password = "qaz123", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows
def bazkie_add_del(sql,table):
    conn =psycopg2.connect(database="drukarnia", user = "postgres", password = "qaz123", host = "127.0.0.1", port = "5432")
    # check1
    sql_count = 'SELECT count(*) from '+table+';'
    cur = conn.cursor()
    cur.execute(sql_count)
    result_before = cur.fetchone()
    # main
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    # check2
    cur = conn.cursor()
    cur.execute(sql_count)
    result_after = cur.fetchone()
    conn.close()
    return(result_before!=result_after)


@app.route('/')
def index():
    products= bazkie_produkty('select name from public."Produkty"')
    lista_produktow =[]
    for x in products:
        lista_produktow.append((x, "/static/img/products/{}.png".format(x)))
    return render_template('start.html', produkty=lista_produktow)    

@app.route('/products/<url>')
def products(url):
    produkt=url
    session["product"] = produkt
    details = bazkie_produkty_route('select"Produkty".name as name_produkty,"Material".name as name_material,"Wykonczenie".name as name_wykonczenie,public."Model".name as model_name,"Material".name as name_material,"Material".opis as opis_material,"Wykonczenie".opis as opis_wykonczenie,cena from public."Produkty_Material"inner join"Produkty"ON"Produkty".id=public."Produkty_Material"."Produkty_id"inner join"Material"ON public."Produkty_Material"."Material_id"="Material".id inner join public."Material_Wykonczenie"ON public."Material_Wykonczenie".id_material="Material".id inner join public."Wykonczenie"on public."Wykonczenie".id=public."Material_Wykonczenie".id_wykonczenie inner join public."Wykonczenie_Model"on public."Wykonczenie_Model".id_wykonczenie=public."Wykonczenie".id inner join public."Model"on public."Model".id=public."Wykonczenie_Model".id_model inner join public.cena_model on public.cena_model.id_model=public."Model".id where "Produkty".name =\'itemname\';',produkt)
    if details[0][7] == '0':
        details = bazkie_produkty_route('select"Produkty".name as name_produkty,"Material".name as name_material,"Wykonczenie".name as name_wykonczenie,public."Model".name as model_name,"Material".name as name_material,"Material".opis as opis_material,"Wykonczenie".opis as opis_wykonczenie,cena_za_metr from public."Produkty_Material"inner join"Produkty"ON"Produkty".id=public."Produkty_Material"."Produkty_id"inner join"Material"ON public."Produkty_Material"."Material_id"="Material".id inner join public."Material_Wykonczenie"ON public."Material_Wykonczenie".id_material="Material".id inner join public."Wykonczenie"on public."Wykonczenie".id=public."Material_Wykonczenie".id_wykonczenie inner join public."Wykonczenie_Model"on public."Wykonczenie_Model".id_wykonczenie=public."Wykonczenie".id inner join public."Model"on public."Model".id=public."Wykonczenie_Model".id_model inner join public.cena_material on public.cena_material.id_material=public."Material".id where "Produkty".name =\'itemname\';',produkt)
    session['details'] = details
    materials = []
    for x in details:
        i=0
        for k in materials:
            if (x[1]==k[0]):
                i=i+1
        if i == 0:
            materials.append((x[1], x[5]))
    return render_template('products.html',materials=materials )

@app.route('/products/materials/<url>' )
def materials(url):
    material=url
    session["material"] = material
    details = (session["details"])
    methods=[]
    for x in details:
        if(x[0]==session['product']):
            if(material in x[1]):
                i=0
                for k in methods:
                    if k in x[2]:
                        i=i+1
                if i==0:
                    methods.append(x[2])
    if('none' in methods[0]):
        return redirect("/products/materials/methods/Nie dotyczy")
                    
    return render_template('materials.html',methods=methods, product=session["product"] )


@app.route('/products/materials/methods/<url>')
def methods(url):
    method=url
    session['method'] = method
    item =session['product']
    sizing =[]
    details = session["details"]
    for x in details:
        if(session['product'] in x[0]):
            if(session['material'] in x[1]):
                if(method in x[2]):
                    wymiar = x[3].split("_")
                    sizing.append((wymiar[0], x[7]))
                if(method == "Nie dotyczy"):
                    wymiar = x[3].split("_")
                    sizing.append((wymiar[0], x[7]))
    print(sizing)
    return render_template('size.html', sizing=sizing)

@app.route('/products/materials/methods/file/<url>', methods=['GET','POST'])
def file(url):
    size = url.split('!')[0]
    quantity = url.split('!')[1]
    code = url.split('!')[2]
    session['size'] = size
    session['quantity'] = quantity
    session['saveCode'] = code
    return render_template('file.html')





@app.route('/products/materials/methods/file/data/', methods=['GET', 'POST'])
def data():
    
    if('projekt' in request.form):
        session['project'] = 'on'
    else:
        session['project'] = 'off'
    if(request.form['link']==""):
        session['plikType'] = 'plik'
        plik = (request.files['img'])
        session['mimetype'] = plik.content_type
        nazwaOst = str((random.random()*1000000000))[:8]
        nazwa = plik.filename
        nazwaSplitted = nazwa.split('.')
        plik.save(os.path.join('G:\githubReps\Printing_house_form\\temp', '{}.{}'.format(nazwaOst, nazwa.split('.')[1])))
        session['file'] = '{}.{}'.format(nazwaOst, nazwaSplitted[1])
    else:
        session['plikType'] = 'link'
        session["file"] = request.form['link']
    return render_template('data.html')






@app.route('/products/materials/methods/file/data/submit/<url>')
def submit(url):
    urlSplitted = url.split("!")
    session['dane']=urlSplitted
    projekt="nie"
    newss='nie'
    address = bazkie_produkty("Select address from public.sending_mail;")
    if session['project']=='on':
        projekt="tak"
    if session['dane'][6] == True:
        newss="tak"
    if session['plikType'] == 'link':
        print
        text='Cześć masz nowe zlecenie! \n Produkt ' +session['product']+'\n Material '+session['material']+'\n Wykonczenie '+session['method']+'\n Rozmiar '+session['size'] +'\n Plik '+session["file"]+'\n Ilosc '+session['quantity']+'\n Kod rabatowy '+session['saveCode']+'\n Imie nazwisko zamawiajacego '+session['dane'][0]+'\n Nazwa firmy '+session['dane'][1]+'\n NIP '+session['dane'][2]+ "\n Adres "+session['dane'][3]+ " "+session['dane'][4]+" "+session['dane'][5]+"\n Czy newsletter " +newss+"\n Mail "+session['dane'][7]+'\n Numer tel '+session['dane'][8]+'\n Dodatkowy projekt '+projekt
        msg = Message("Zlecenie",  recipients=address)
        msg.body = text
        mail.send(msg)
    if session['plikType'] == 'plik':
        text='Cześć masz nowe zlecenie! \n Produkt ' +session['product']+'\n Material '+session['material']+'\n Wykonczenie '+session['method']+'\n Rozmiar '+session['size'] +'\n Ilosc '+session['quantity']+'\n Kod rabatowy '+session['saveCode']+'\n Imie nazwisko zamawiajacego '+session['dane'][0]+'\n Nazwa firmy '+session['dane'][1]+'\n NIP '+session['dane'][2]+ "\n Adres "+session['dane'][3]+ " "+session['dane'][4]+" "+session['dane'][5]+"\n Czy newsletter " +newss+"\n Mail "+session['dane'][7]+'\n Numer tel '+session['dane'][8]+'\n Dodatkowy projekt '+projekt
        msg = Message("Zlecenie",  recipients=address)
        msg.body = text
        with app.open_resource(os.path.join('G:\githubReps\Printing_house_form\\temp',session['file'])) as fp:
            msg.attach(session['file'], session['mimetype'], fp.read())
        mail.send(msg)
        os.remove(os.path.join('G:\githubReps\Printing_house_form\\temp',session['file']))
    
    return render_template('submit.html')
# adminpage
@app.route('/login', )
def login():
    session['login']=0
    return render_template('login.html', wrong=0)

@app.route('/adminpanel', methods= ['GET','POST'])
def adminpanel():
    if session["login"]==1:
        return render_template('adminpanel.html')
    if request.method =='POST':
        potencial_password = request.form['password']
        passwords=login_database('select password from public."passwords"')
       
        if potencial_password in passwords:
            session["login"]=1
            return render_template('adminpanel.html')
        else: 
            return render_template('login.html', wrong=1)
    else:
        return render_template('login.html', wrong=0)
    
    return render_template('adminpanel.html')

@app.route('/adminproduct')
def adminproduct():
    if session['login']==1:
        return render_template('adminproduct.html')
    else:
        return render_template('login.html', wrong=0)

@app.route('/addproductstart')
def addproductstart():
    if session['login']==1:
        return render_template('addproductstart.html')
    else:
        return render_template('login.html', wrong=0)
    

@app.route('/addproduct',methods=['GET', 'POST'])
def addproduct():
    if session['login']==1:
        plik = (request.files['img'])
        nazwa = (request.form['nazwa'])
        plikSplitted = plik.filename.split('.')
        plik.save(os.path.join('G:\githubReps\Printing_house_form\\static\img\products', '{}.{}'.format(nazwa, plikSplitted[1])))
        product_name="'"+nazwa+"'"
        table='"Produkty"'
        sql=f"INSERT INTO public.{table} (id, name)	VALUES (DEFAULT ,{product_name});"
        zmiany=bazkie_add_del(sql,table)
        sql = "select id from \"Produkty\" where name = '{}'".format(nazwa)
        session['addProductName'] = nazwa
        session['product_id']=(bazkie_produkty(sql))
        return render_template('addmaterials.html', nazwa = nazwa)
    else:
        return render_template('login.html', wrong=0)
    
@app.route('/delproduct',methods=['GET', 'POST'])
def delproduct():
    if session['login']==1:
        products= bazkie_produkty('select name from public."Produkty"')
        return render_template('delproduct.html',produkty=products)
    else:
        return render_template('login.html', wrong=0)

@app.route('/addmaterial',methods=['GET', 'POST']) 
def addmaterial():
    if session['login']==1:
        materials = (request.form.getlist('material'))
        session['materialsList'] = materials
        desc = (request.form.getlist('desc'))
        materials_id = []
        table='"Material"'
        for x in materials:
            product_name = "'"+x+"'"
            opis = "'"+desc[materials.index(x)]+"'"
            sql=f"INSERT INTO public.{table} (id, name, opis)	VALUES (DEFAULT ,{product_name}, {opis});"
            zmiany=bazkie_add_del(sql,table)
            sql = "select id from \"Material\" where name = '{}'".format(x)
            materials_id.append(max(bazkie_produkty(sql)))
        session['material_id'] = materials_id
        for k in materials_id:
            sql = 'INSERT INTO public."Produkty_Material" (id, "Material_id", "Produkty_id") VALUES (DEFAULT, {}, {});'.format(k, session['product_id'][0])
            bazkie_add_del(sql, '"Produkty_Material"')
        return render_template('addmethods.html', materials = materials)
    else:
        return render_template('login.html', wrong=0)
    
@app.route('/addwykonczenie',methods=['GET', 'POST']) 
def addwykonczenie():
    if session['login']==1:
        session['finishId']=[]
        nazwaWykonczenia = (request.form.getlist('finish'))
        pliki = (request.files.getlist('img'))
        for x in pliki:
            if x.filename != '':
                plikSplitted = x.filename.split('.')
                x.save(os.path.join('G:\githubReps\Printing_house_form\\static\img\\finishing', '{}.{}'.format('{}_{}'.format(session['addProductName'],nazwaWykonczenia[pliki.index(x)]), plikSplitted[1])))
                
        for x in session['materialsList']:
            i=0+((session['materialsList'].index(x))*5)
            finishId = []
            table='"Wykonczenie"'
            while i<(5+((session['materialsList'].index(x))*5)):
                if(nazwaWykonczenia[i]!=''):
                    product_name = "'"+nazwaWykonczenia[i]+"'"
                    sql=f"INSERT INTO public.{table} (id, name, opis)	VALUES (DEFAULT ,{product_name}, null);"
                    zmiany=bazkie_add_del(sql,table)
                    sql = "select id from \"Wykonczenie\" where name = '{}'".format(nazwaWykonczenia[i])
                    finishId.append(max(bazkie_produkty(sql)))
                    for k in finishId:
                        session['finishId'].append(k)
                        sql = 'INSERT INTO public."Material_Wykonczenie" (id, "id_material", "id_wykonczenie") VALUES (DEFAULT, {}, {});'.format(session['material_id'][session['materialsList'].index(x)], k)
                        bazkie_add_del(sql, '"Produkty_Material"')
                i=i+1
            wykonczeniaNazwy = []
            for p in nazwaWykonczenia:
                if p != '':
                    wykonczeniaNazwy.append(p)
            session['wykonczeniaNazwy'] = wykonczeniaNazwy
        materialy = []
        for x in session['material_id']:
            materialy.append(bazkie_produkty("select name from \"Material\" where id = {}".format(x)))
        
        return render_template('addsizes.html', wyk = wykonczeniaNazwy, mat = materialy)
    
@app.route('/addcenamaterial',methods=['GET', 'POST']) 
def addCena():
    if session['login']==1:
        if(request.form.get('model')=='custom'):
            wykonczeniaId = []
            for k in session['wykonczeniaNazwy']:
                sql = "select id from \"Wykonczenie\" where name = '{}'".format(k)
                wykonczeniaId.append(max(bazkie_produkty(sql)))
            for t in wykonczeniaId:
                sql = 'INSERT INTO public."Wykonczenie_Model" (id, "id_wykonczenie", "id_model") VALUES (DEFAULT, {}, 1);'.format(t)
                bazkie_add_del(sql, '"Wykonczenie_Model"')
            for x in session['material_id']:
                sql = 'INSERT INTO public."cena_material" (id, "cena_za_metr", "id_material") VALUES (DEFAULT, {}, {});'.format(request.form.getlist('price')[session['material_id'].index(x)],x)
                bazkie_add_del(sql, '"cena_material"')
        if(request.form.get('model')=='set'):
            wykonczenieCenaRozmiar = []
            for x in request.form.getlist('finish'):
                i = 0+request.form.getlist('finish').index(x)*4
                while i<4+request.form.getlist('finish').index(x)*4:
                    if request.form.getlist('price')[i] != '':
                        if request.form.getlist('size')[i] != '':
                            wykonczenieCenaRozmiar.append((x, '{}_{}'.format(request.form.getlist('size')[i], x), request.form.getlist('price')[i]))
                    i=i+1
            for k in wykonczenieCenaRozmiar:
                sql= 'INSERT INTO public."Model"(id, name) VALUES (DEFAULT, \'{}\');'.format(k[1])
                bazkie_add_del(sql,'\"Model\"')
                finish_id = max(bazkie_produkty('Select id from "Wykonczenie" where name = \'{}\''.format(k[0])))
                model_id = max(bazkie_produkty('Select id from "Model" where name = \'{}\''.format(k[1])))
                sql = 'INSERT INTO public."Wykonczenie_Model" (id, id_wykonczenie, id_model) VALUES (DEFAULT, {}, {});'.format(finish_id, model_id)
                bazkie_add_del(sql, '\"Wykonczenie_Model\"')
                sql = 'INSERT INTO public."cena_model" (id, cena, id_model) VALUES (DEFAULT, {}, {});'.format(k[2], model_id)
                bazkie_add_del(sql, '\"cena_model\"')
                
        
        return render_template('addsuccess.html')
    
@app.route('/delproducts/<url>')
def delproducts(url):
    if session['login']==1:
        produkt = url
        details = bazkie_produkty_route('select"Produkty".name as name_produkty,"Produkty".id as id_produkty,"Material".id as id_material,"Wykonczenie".id as id_wykonczenie,public."Model".id as id_model,cena from public."Produkty_Material"inner join"Produkty"ON"Produkty".id=public."Produkty_Material"."Produkty_id"inner join"Material"ON public."Produkty_Material"."Material_id"="Material".id inner join public."Material_Wykonczenie"ON public."Material_Wykonczenie".id_material="Material".id inner join public."Wykonczenie"on public."Wykonczenie".id=public."Material_Wykonczenie".id_wykonczenie inner join public."Wykonczenie_Model"on public."Wykonczenie_Model".id_wykonczenie=public."Wykonczenie".id inner join public."Model"on public."Model".id=public."Wykonczenie_Model".id_model inner join public.cena_model on public.cena_model.id_model=public."Model".id where "Produkty".name =\'itemname\';',produkt)
        if details[0][5] == '0':
            details = bazkie_produkty_route('select"Produkty".name as name_produkty,"Produkty".id as id_produkty,"Material".id as id_material,"Wykonczenie".id as id_wykonczenie,public."Model".id as id_model,cena_za_metr from public."Produkty_Material"inner join"Produkty"ON"Produkty".id=public."Produkty_Material"."Produkty_id"inner join"Material"ON public."Produkty_Material"."Material_id"="Material".id inner join public."Material_Wykonczenie"ON public."Material_Wykonczenie".id_material="Material".id inner join public."Wykonczenie"on public."Wykonczenie".id=public."Material_Wykonczenie".id_wykonczenie inner join public."Wykonczenie_Model"on public."Wykonczenie_Model".id_wykonczenie=public."Wykonczenie".id inner join public."Model"on public."Model".id=public."Wykonczenie_Model".id_model inner join public.cena_material on public.cena_material.id_material=public."Material".id where "Produkty".name =\'itemname\';',produkt)
            for x in details:
                sql = "DELETE FROM public.\"cena_material\" WHERE id_material = {};".format(x[2])
                bazkie_add_del(sql, '"cena_material"')
                sql = "DELETE FROM public.\"Wykonczenie_Model\" WHERE id_wykonczenie = {};".format(x[3])
                bazkie_add_del(sql, '"Wykonczenie_Model"')
                sql = "DELETE FROM public.\"Wykonczenie\" WHERE id = {};".format(x[3])
                bazkie_add_del(sql, '"Wykonczenie"')
                sql = "DELETE FROM public.\"Material_Wykonczenie\" WHERE id_material = {};".format(x[2])
                bazkie_add_del(sql, '"Material_Wykonczenie"')
                sql = "DELETE FROM public.\"Material\" WHERE id = {};".format(x[2])
                bazkie_add_del(sql, '"Material"')
                sql = "DELETE FROM public.\"Produkty_Material\" WHERE \"Material_id\" = {};".format(x[2])
                bazkie_add_del(sql, '"Produkty_Material"')
                sql = "DELETE FROM public.\"Produkty\" WHERE id = {};".format(x[1])
                bazkie_add_del(sql, '"Produkty"')
        else:
            for x in details:
                print(x)
                sql = "DELETE FROM public.\"cena_model\" WHERE id_model = {};".format(x[4])
                bazkie_add_del(sql, '"cena_model"')
                sql = "DELETE FROM public.\"Model\" WHERE id = {};".format(x[4])
                bazkie_add_del(sql, '"Model"')
                sql = "DELETE FROM public.\"Wykonczenie_Model\" WHERE id_wykonczenie = {} ".format(x[3])
                bazkie_add_del(sql, '"Wykonczenie_Model"')
                sql = "DELETE FROM public.\"Wykonczenie\" WHERE id = {};".format(x[3])
                bazkie_add_del(sql, '"Wykonczenie"')
                sql = "DELETE FROM public.\"Material_Wykonczenie\" WHERE id_material = {}".format(x[2])
                bazkie_add_del(sql, '"Material_Wykonczenie"')
                sql = "DELETE FROM public.\"Material\" WHERE id = {};".format(x[2])
                bazkie_add_del(sql, '"Material"')
                sql = "DELETE FROM public.\"Produkty_Material\" WHERE \"Material_id\" = {}".format(x[2])
                bazkie_add_del(sql, '"Produkty_Material"')
                sql = "DELETE FROM public.\"Produkty\" WHERE id = {};".format(x[1])
                bazkie_add_del(sql, '"Produkty"')
        return render_template('delsuccess.html')

@app.route('/selectquery_id',methods=['GET', 'POST'])
def selectquery_id():
    if session['login']==1:
        table=request.args.get('table',None)
        table='"'+table+'"'
        where_item=request.args.get('where_item',None)
        where_value=request.args.get('where_value',None)
        sql=f"Select * from public.{table} where {table}.{where_item}='{where_value}'"
        print(bazkie_produkty(sql))
        return render_template('addproduct.html') 
# kody
@app.route('/kodyselect',methods=['GET', 'POST'])
def kody():
    if session['login']==1:
        kod_nazwa=request.args.get('nazwa',None)
        sql=f"SELECT procent FROM public.kody where public.kody.nazwa = '{kod_nazwa}'"
        kod=bazkie_produkty(sql)
        return '{}'.format(kod[0])

@app.route('/addkody')
def addkody():
    if session['login']==1:
        return render_template('addcode.html')

@app.route('/addkodyrequest',methods=['GET', 'POST'])
def addkodyrequest():
    if session['login']==1:
        kod_nazwa=request.args.get('nazwa',None)
        procent=request.args.get('procent',None)
        table="kody"
        sql=f"INSERT INTO public.kody(	nazwa, procent)	VALUES ('{kod_nazwa}', {procent});"
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return 'ok'

@app.route('/delkody',methods=['GET', 'POST'])
def delkody():
    if session['login']==1:
        kod_nazwa=request.args.get('nazwa',None)
        table="kody"
        sql=f"DELETE FROM public.{table} WHERE {table}.nazwa='{kod_nazwa}';"
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return 'ok'

@app.route('/showkody')
def showkody():
    if session['login']==1:
        codes= bazkie_produkty_route('select * from public.kody', "")
        print(codes)
        return render_template('delcode.html', kody = codes)

@app.route('/kodyadmin')
def kodyadmin():
    if session['login']==1:
        return render_template('codes.html')

@app.route('/changepass')
def changepass():
    if session['login']==1:
        kod_nazwa=request.args.get('nazwa',None)
        table = 'passwords'
        sql=f"UPDATE public.passwords set password ='{kod_nazwa}' WHERE id=1;"
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return 'ok'

@app.route('/adminpassword')
def adminpassword():
    if session['login']==1:
        return render_template('changepassword.html')
    
@app.route('/adminmail')
def adminmail():
    if session['login']==1:
        mail = bazkie_produkty("Select address from public.sending_mail;")
        return render_template('adminmail.html', mail=mail)
    

app.run()
