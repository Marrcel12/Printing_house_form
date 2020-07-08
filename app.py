from flask import Flask, render_template, request,session
from test import SignUpForm
import base64
import psycopg2

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
    return rows

app = Flask(__name__)
app.config['SECRET_KEY']= 'qaz123'
app.config['TEMPLATES_AUTO_RELOAD'] = "True"
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/start')
def start():
    return render_template('start.html')    

@app.route('/products/<url>')
def products(url):
    
    product=url
    session["product"] = product 

    if product == 'baner':
        materials=[['FRONTLIT',"Idealny do zastosowania na zewnątrz"],['MESH (SIATKA)','Idealny do zastosowania na zewnątrz, na dużych powierzchniach lub miejscach o dużym nasileniu wiatru'],['BLOCKOUT', 'Idealny do wyeksponowania oferty po dwóch stronach baneru'],['POLIESTER 205g','Idealny do zastosowania wewnątrz'],['Poliester 115g','Idealny do zastosowania wewnątrz i do flag']]
    if product == 'sticker':
        materials=[['FOLIA BłYSZCZĄCA'],['FOLIA MATOWA'],['EASY DOT', "Folia umożliwiająca przeniesienie wydruku w inne miejsce bez utraty właściwości klejących materiału"], ["MAGNEZ BŁYSZCZĄCY"], ["MAGNES MATOWY"]]
    if product == 'pad':
        materials=[['DYWAN','Idealny do zastosowania np. jako wycieraczka'],['FLOORPROMOTOR','Idealny do zastosowania np. jako podkładka pod myszkę']]
    if product == 'poster':
        materials=[['PAPIER 150g', 'Idealny do drukowania plakató lub ulotek (druk jednostronny)'],['PAPIER 200g','Idealny do drukowania dyplomów']]
    if product == 'flag':
        materials=['POLIESTER 115g',['POLYFLAG','Idealny do zastosowania w miejscach o dużym nasileniu wiatru']]
    
    return render_template('products.html',product=product,materials=materials )

@app.route('/products/materials/<url>' )
def materials(url):
    
    material=url
    session["material"] = material
    methods=""
    if material == 'FRONTLIT':
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