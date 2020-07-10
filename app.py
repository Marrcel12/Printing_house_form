from flask import Flask, render_template, request,session
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

def bazkie_produkty(sql):
    conn = psycopg2.connect(database="Print_house", user = "postgres", password = "qaz123", host = "127.0.0.1", port = "5432")
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
    conn = psycopg2.connect(database="Print_house", user = "postgres", password = "qaz123", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows



@app.route("/")
def index():
  
   return "hello"

@app.route('/start')
def start():
    products= bazkie_produkty('select name from public."Produkty"')
    return render_template('start.html', products=products)    

@app.route('/products/<url>')
def products(url):
    
    produkt=url
    session["product"] = produkt
    details = bazkie_produkty_route('select "Produkty".name as name_produkty,"Material".name as name_material, "Wykonczenie".name as name_wykonczenie,"Material".name as name_material, "Material".opis as opis_material, "Wykonczenie".opis as opis_wykonczenie from public."Produkty_Material" inner join "Produkty" ON  "Produkty".id = public."Produkty_Material"."Produkty_id" inner join "Material" ON public."Produkty_Material"."Material_id" ="Material".id inner join public."Material_Wykonczenie" ON public."Material_Wykonczenie".id_material="Material".id inner join public."Wykonczenie" on public."Wykonczenie".id  = public."Material_Wykonczenie".id_wykonczenie inner join public."Wykonczenie_Model" on public."Wykonczenie_Model".id_wykonczenie = public."Wykonczenie".id inner join public."Model" on public."Model".id = public."Wykonczenie_Model".id_model where "Produkty".name =\'itemname\';',produkt)
    session['details'] = details
    materials = []
    for x in details:
        materials.append([x[1], x[4]])
    return render_template('products.html',materials=materials )

@app.route('/products/materials/<url>' )
def materials(url):
    
    material=url
    session["material"] = material
    methods=""
    if material == 'Frontlit':
        methods=["ZGRZEW","DOCIĘTE NA WYMIAR"]
    if material == 'MESH (SIATKA)':
        methods=["ZGRZEW + OCZKA"]
    if material == 'BLOCKOUT':
        methods=['DOCIĘTE NA WYMIAR']
    if material == 'POLIESTER 205g':
        methods=['OBSZYCIE']
    if material == 'Poliester 115g':
        methods=['DOCIĘTE NA WYMIAR','OBSZYCIE + OCZKA']
    return render_template('materials.html',material=material,methods=methods )


@app.route('/products/materials/methods/<url>')
def methods(url):
    method=url
    session['method'] = method
    item =session['product']
    if item == 'baner':
        sizing = "0"
    if item !='baner':
        sizing = ['220x20', '300x30']
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
    print(urlSplitted)
    return render_template('submit.html')


app.run()
