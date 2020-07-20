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
    return render_template('size.html', sizing=sizing)

@app.route('/products/materials/methods/file/<url>', methods=['GET','POST'])
def file(url):
    size = url.split('!')[0]
    quantity = url.split('!')[1]
    session['size'] = size
    session['quantity'] = quantity
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
    if session['project']=='on':
        projekt="tak"
    if session['dane'][6] == True:
        newss="tak"
    if session['plikType'] == 'link':
        print
        text='Cześć masz nowe zlecenie! \n Produkt ' +session['product']+'\n Material '+session['material']+'\n Wykonczenie '+session['method']+'\n Rozmiar '+session['size'] +'\n Plik '+session["file"]+'\n Ilosc '+session['quantity']+'\n Imie nazwisko zamawiajacego '+session['dane'][0]+'\n Nazwa firmy '+session['dane'][1]+'\n NIP '+session['dane'][2]+ "\n Adres "+session['dane'][3]+ " "+session['dane'][4]+" "+session['dane'][5]+"\n Czy newsletter " +newss+"\n Mail "+session['dane'][7]+'\n Numer tel '+session['dane'][8]+'\n Dodatkowy projekt '+projekt
        msg = Message("Zlecenie",  recipients=['adi.jobda@gmail.com'])
        msg.body = text
        mail.send(msg)
    if session['plikType'] == 'plik':
        text='Cześć masz nowe zlecenie! \n Produkt ' +session['product']+'\n Material '+session['material']+'\n Wykonczenie '+session['method']+'\n Rozmiar '+session['size'] +'\n Ilosc '+session['quantity']+'\n Imie nazwisko zamawiajacego '+session['dane'][0]+'\n Nazwa firmy '+session['dane'][1]+'\n NIP '+session['dane'][2]+ "\n Adres "+session['dane'][3]+ " "+session['dane'][4]+" "+session['dane'][5]+"\n Czy newsletter " +newss+"\n Mail "+session['dane'][7]+'\n Numer tel '+session['dane'][8]+'\n Dodatkowy projekt '+projekt
        msg = Message("Zlecenie",  recipients=['adi.jobda@gmail.com'])
        msg.body = text
        with app.open_resource(os.path.join('G:\githubReps\Printing_house_form\\temp',session['file'])) as fp:
            msg.attach(session['file'], session['mimetype'], fp.read())
        mail.send(msg)
        os.remove(os.path.join('G:\githubReps\Printing_house_form\\temp',session['file']))
    
    return render_template('submit.html')
# adminpage
@app.route('/login', methods= ['GET','POST'])
def login():
    if request.method =='POST':
        potencial_password = request.form['password']
        passwords=login_database('select password from public."passwords"')
       
        if potencial_password in passwords:
            return redirect(url_for('adminpanel'))
        else:
            session['login']=0
            return render_template('login.html', wrong=1)
            
    return render_template('login.html', wrong=0)

@app.route('/adminpanel')
def adminpanel():
        products= bazkie_produkty('select name from public."Produkty"')
        session["login"]=1
        return render_template('adminpanel.html' ,produkty = products)


@app.route('/addproduct',methods=['GET'])
def addproduct():
    if session['login']==1:
        product_name=request.args.get('name', None)
        product_name="'"+product_name+"'"
        table='"Produkty"'
        sql=f"INSERT INTO public.{table} (id, name)	VALUES (DEFAULT ,{product_name});"
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',dodany=zmiany)
    else:
        return render_template('login.html', wrong=0)
@app.route('/delproduct',methods=['GET'])
def delproduct():
    if session['login']==1:
        product_id=request.args.get('id', None)
        table='"Produkty"'
        sql=f'DELETE FROM public.{table}	WHERE "Produkty".id={product_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
    else:
        return render_template('login.html', wrong=0)

@app.route('/addmaterial',methods=['GET']) 
def addmaterial():
    if session['login']==1:
        material_name="'"+request.args.get('name',None)+"'"    
        material_desc="'"+request.args.get('desc',None)+"'"   
        table='"Material"'
        sql=f'INSERT INTO public.{table}(id, name, opis)	VALUES (DEFAULT, {material_name}, {material_desc});'
        zmiany=bazkie_add_del(sql,table)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delmaterial',methods=['GET']) 
def delmaterial():
    if session['login']==1:
        material_id=request.args.get('id', None)    
        table='"Material"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={material_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)

@app.route('/addwykonczenie',methods=['GET']) 
def addwykonczenie():
    if session['login']==1:
        wykonczenie_name="'"+request.args.get('name',None)+"'"    
        wykonczenie_desc="'"+request.args.get('desc',None)+"'"   
        table='"Wykonczenie"'
        sql=f'INSERT INTO public.{table}(id, name, opis)	VALUES (DEFAULT, {wykonczenie_name}, {wykonczenie_desc});'
        zmiany=bazkie_add_del(sql,table)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delwykonczenie',methods=['GET']) 
def delwykonczenie():
    if session['login']==1:
        wykonczenie_id=request.args.get('id', None)    
        table='"Wykonczenie"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={wykonczenie_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)

# @app.route('/addmaterial',methods=['GET']) 
# def addMaterial():
#     if session['login']==1:
#         material_name="'"+request.args.get('name',None)+"'"    
#         material_desc="'"+request.args.get('desc',None)+"'"   
#         table='"Material"'
#         sql=f'INSERT INTO public.{table}(id, name, opis)	VALUES (DEFAULT, {wykonczenie_name}, {wykonczenie_desc});'
#         zmiany=bazkie_add_del(sql,table)
#         return render_template('addproduct.html',usuniety=zmiany)
# @app.route('/delmaterial',methods=['GET']) 
# def delMaterial():
#     if session['login']==1:
#         material_id=request.args.get('id', None)    
#         table='"Material"'
#         sql=f'DELETE FROM public.{table} WHERE {table}.id={wykonczenie_id};'
#         zmiany=bazkie_add_del(sql,table)
#         print(zmiany)
#         return render_template('addproduct.html',usuniety=zmiany)

@app.route('/addmodel',methods=['GET']) 
def addModel():
    if session['login']==1:
        model_name="'"+request.args.get('name',None)+"'"     
        table='"Model"'
        sql=f'INSERT INTO public.{table}(id, name)	VALUES (DEFAULT, {model_name});'
        zmiany=bazkie_add_del(sql,table)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delmodel',methods=['GET']) 
def delModel():
    if session['login']==1:
        model_id=request.args.get('id', None)    
        table='"Model"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={model_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
# add relations
@app.route('/addProdukty_Material',methods=['GET'])
def addProdukty_Material():
    if session['login']==1:
        id_produkty=request.args.get('id_produkty', None)
        id_material=request.args.get('id_material', None) 
        table='"Produkty_Material"'
        sql=f'INSERT INTO public."Produkty_Material"(id, "id_material", "id_produkty")VALUES (DEFAULT, {id_material}, {id_produkty});'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delProdukty_Material',methods=['GET'])
def delProdukty_Material():
    if session['login']==1:
        Produkty_Material_id=request.args.get('id', None)    
        table='"Produkty_Material"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={Produkty_Material_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)

@app.route('/addMaterial_Wykonczenie',methods=['GET'])
def addMaterial_Wykonczenie():
    if session['login']==1:
        id_wykonczenie=request.args.get('id_wykonczenie', None)
        id_material=request.args.get('id_material', None) 
        table='"Material_Wykonczenie"'
        sql=f'INSERT INTO public."Material_Wykonczenie"(id, "id_material", "id_wykonczenie")VALUES (DEFAULT, {id_material}, {id_wykonczenie});'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delMaterial_Wykonczenie',methods=['GET'])
def delMaterial_Wykonczenie():
    if session['login']==1:
        Material_Wykonczenie_id=request.args.get('id', None)    
        table='"Material_Wykonczenie"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={Material_Wykonczenie_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)

@app.route('/addcena_material',methods=['GET'])
def addcena_material():
    if session['login']==1:
        cena_za_metr=request.args.get('cena_za_metr', None)
        id_material=request.args.get('id_material', None) 
        table='"cena_material"'
        sql=f'INSERT INTO public.{table}(id, "id_material", "cena_za_metr")VALUES (DEFAULT, {id_material}, {cena_za_metr});'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delcena_material',methods=['GET'])
def delcena_material():
    if session['login']==1:
        Material_Wykonczenie_id=request.args.get('id', None)    
        table='"cena_material"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={Material_Wykonczenie_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)

@app.route('/addcena_model',methods=['GET'])
def addcena_model():
    if session['login']==1:
        cena=request.args.get('cena', None)
        id_model=request.args.get('id_model', None) 
        table='"cena_model"'
        sql=f'INSERT INTO public.{table}(id, "id_model", "cena")VALUES (DEFAULT, {id_model}, {cena});'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/delcena_model',methods=['GET'])
def delcena_model():
    if session['login']==1:
        Material_Wykonczenie_id=request.args.get('id', None)    
        table='"cena_model"'
        sql=f'DELETE FROM public.{table} WHERE {table}.id={Material_Wykonczenie_id};'
        zmiany=bazkie_add_del(sql,table)
        print(zmiany)
        return render_template('addproduct.html',usuniety=zmiany)
@app.route('/selectquery_id',methods=['GET'])
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
@app.route('/kodyselect',methods=['GET'])
def kody():
    kod_nazwa=request.args.get('nazwa',None)
    sql=f"SELECT procent FROM public.kody where public.kody.nazwa = '{kod_nazwa}'"
    kod=bazkie_produkty(sql)
    print(kod[0])
    return render_template('addproduct.html') 
@app.route('/addkody',methods=['GET'])
def addkody():
    kod_nazwa=request.args.get('nazwa',None)
    procent=request.args.get('procent',None)
    table="kody"
    sql=f"INSERT INTO public.kody(	nazwa, procent)	VALUES ('{kod_nazwa}', {procent});"
    zmiany=bazkie_add_del(sql,table)
    print(zmiany)
    
    return render_template('addproduct.html') 
@app.route('/delkody',methods=['GET'])
def delkody():
    kod_nazwa=request.args.get('nazwa',None)
    table="kody"
    sql=f"DELETE FROM public.{table} WHERE {table}.nazwa='{kod_nazwa}';"
    zmiany=bazkie_add_del(sql,table)
    print(zmiany)
    return render_template('addproduct.html') 

app.run()
