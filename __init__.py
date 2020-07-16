from flask import Flask, render_template, request,session,redirect,url_for
from test import SignUpForm
from flask_mail import Mail, Message
import base64
import psycopg2
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



@app.route("/")
def index():
  
   return "hello"

@app.route('/start')
def start():
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
    print(sizing)
    return render_template('size.html', sizing=sizing)

@app.route('/products/materials/methods/file/<url>', methods=['GET','POST'])
def file(url):
    size = url.split('!')[0]
    quantity = url.split('!')[1]
    session['size'] = size
    session['quantity'] = quantity
    return render_template('file.html')

@app.route('/products/materials/methods/file/data/<url>')
def data(url):
    urlSplitted = url.split("!")
    session["project"] =urlSplitted[0]
    if(urlSplitted[1]=='l'):
        session['plikType'] = 'link'
        plik = bytearray.fromhex(urlSplitted[2]).decode()
    else:
        session['plikType'] = 'file'
        plik = urlSplitted[2]

    session["file"] = plik
    return render_template('data.html', plik = plik)
@app.route('/products/materials/methods/file/data/submit/<url>')
def submit(url):
    urlSplitted = url.split("!")
    session['dane']=urlSplitted
    projekt="nie"
    newss='nie'
    if session['project']==True:
        projekt="tak"
    if session['dane'][6] == True:
        newss="tak"
    text='Cześć masz nowe zlecenie! \n Produkt ' +session['product']+'\n Material '+session['material']+'\n Wykonczenie '+session['method']+'\n Rozmiar '+session['size'] +'\n Plik '+session["file"]+'\n Ilosc '+session['quantity']+'\n Imie nazwisko zamawiajacego '+session['dane'][0]+'\n Nazwa firmy '+session['dane'][1]+'\n NIP '+session['dane'][2]+ "\n Adres "+session['dane'][3]+ " "+session['dane'][4]+" "+session['dane'][5]+"\n Czy newsletter " +newss+"\n Mail "+session['dane'][7]+'\n Numer tel '+session['dane'][8]+'\n Dodatkowy projekt '+projekt
    msg = Message("Zlecenie",  recipients=['marcel72press@gmail.com'])
    msg.body = text
    mail.send(msg)
    return render_template('submit.html')

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
    

@app.route('/addproduct')
def addproduct():
    if session['login']==1:
        return render_template('addproduct.html')
    else:
        return render_template('login.html', wrong=0)
    
app.run()
