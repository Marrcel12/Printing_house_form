from flask import Flask, render_template, request, session
from test import SignUpForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'qaz123'
app.config['TEMPLATES_AUTO_RELOAD'] = 'True'
# root products
products_root={"Baner reklamowy":[['FRONTLIT', 'Idealny do zastosowania na zewnątrz'], ['MESH (SIATKA)', 'Idealny do zastosowania na zewnątrz, na dużych powierzchniach lub miejscach o dużym nasileniu wiatru'], [
            'BLOCKOUT', 'Idealny do wyeksponowania oferty po dwóch stronach baneru'], ['POLIESTER 205g', 'Idealny do zastosowania wewnątrz'], ['Poliester 115g', 'Idealny do zastosowania wewnątrz i do flag']], "Naklejka lub magnez":[['FOLIA BłYSZCZĄCA'], ['FOLIA MATOWA'], [
            'EASY DOT', 'Folia umożliwiająca przeniesienie wydruku w inne miejsce bez utraty właściwości klejących materiału'], ['MAGNEZ BŁYSZCZĄCY']]
    , "Dywan i podkladka":[['DYWAN', 'Idealny do zastosowania np. jako wycieraczka'], [
            'FLOORPROMOTOR', 'Idealny do zastosowania np. jako podkładka pod myszkę']],"Plakat i dyplom":[['PAPIER 150g', 'Idealny do drukowania plakató lub ulotek (druk jednostronny)'], [
            'PAPIER 200g', 'Idealny do drukowania dyplomów']],"Flaga pozioma":['POLIESTER 115g', [
            'POLYFLAG', 'Idealny do zastosowania w miejscach o dużym nasileniu wiatru']}
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/start')
def start():
    global products_root
    print(products_root)
    return render_template('start.html', products = products_root.keys())


@app.route('/products/<url>')
def products(url):

    product = url
    session['product'] = product

    if product == 'baner':
        materials = [['FRONTLIT', 'Idealny do zastosowania na zewnątrz'], ['MESH (SIATKA)', 'Idealny do zastosowania na zewnątrz, na dużych powierzchniach lub miejscach o dużym nasileniu wiatru'], [
            'BLOCKOUT', 'Idealny do wyeksponowania oferty po dwóch stronach baneru'], ['POLIESTER 205g', 'Idealny do zastosowania wewnątrz'], ['Poliester 115g', 'Idealny do zastosowania wewnątrz i do flag']]
    if product == 'sticker':
        materials = [['FOLIA BłYSZCZĄCA'], ['FOLIA MATOWA'], [
            'EASY DOT', 'Folia umożliwiająca przeniesienie wydruku w inne miejsce bez utraty właściwości klejących materiału'], ['MAGNEZ BŁYSZCZĄCY']]
    if product == 'pad':
        materials = [['DYWAN', 'Idealny do zastosowania np. jako wycieraczka'], [
            'FLOORPROMOTOR', 'Idealny do zastosowania np. jako podkładka pod myszkę']]
    if product == 'poster':
        materials = [['PAPIER 150g', 'Idealny do drukowania plakató lub ulotek (druk jednostronny)'], [
            'PAPIER 200g', 'Idealny do drukowania dyplomów']]
    if product == 'flag':
        materials = ['POLIESTER 115g', [
            'POLYFLAG', 'Idealny do zastosowania w miejscach o dużym nasileniu wiatru']]

    return render_template('products.html', product=product, materials=materials)


@app.route('/products/materials/<url>')
def materials(url):

    if "['" in url:
        url = url.replace("['", "")
        url = url.replace("']", "")
    product = url
    session['material'] = product
    methods = ''
    # sticker
    if product == 'FRONTLIT':
        methods = ['ZGRZEW', 'DOCIĘTE NA WYMIAR']
    if product == 'MESH (SIATKA)':
        methods = ['ZGRZEW + OCZKA']
    if product == 'BLOCKOUT':
        methods = ['DOCIĘTE NA WYMIAR']
    if product == 'POLIESTER 205g':
        methods = ['OBSZYCIE']
    if product == 'Poliester 115g':
        methods = ['DOCIĘTE NA WYMIAR', 'OBSZYCIE + OCZKA']
#    magnez
    if product == 'FOLIA BłYSZCZĄCA':
        methods = ['DOCIĘTE NA WYMIARE',
                   'DOCIĘTE NA KSZTAŁT', 'W KSZTAŁCIE KOŁA']
    if product == 'FOLIA MATOWA':
        methods = ['DOCIĘTE NA WYMIARE',
                   'DOCIĘTE NA KSZTAŁT', 'W KSZTAŁCIE KOŁA']
    if product == 'EASY DOT':
        methods = ['DOCIĘTE NA KSZTAŁT']
    if product == 'MAGNES BŁYSZCZĄCY':
        methods = ['DOCIĘTE NA WYMIARE',
                   'DOCIĘTE NA KSZTAŁT', 'W KSZTAŁCIE KOŁA']
    if product == 'MAGNES MATOWY':
        methods = ['DOCIĘTE NA WYMIARE',
                   'DOCIĘTE NA KSZTAŁT', 'W KSZTAŁCIE KOŁA']
# carpet
    if product == "DYWAN":
        methods = ["W KSZTAŁCIE KOŁA",
                   "DOCIĘTE NA WYMIAR", "DOCIĘTE NA KSZTAŁT"]
    if product == "FLOORPROMOTOR":
        methods = ["W KSZTAŁCIE KOŁA",
                   "DOCIĘTE NA WYMIAR", "DOCIĘTE NA KSZTAŁT"]
# Poster
    if product == "PAPIER 150g":
        methods=["DOCIĘTE NA WYMIAR"]
    if product == "PAPIER 200g":
        methods= ["DOCIĘTE NA WYMIAR"]
    
# flag 
    if product == "POLIESTER 115g":
        methods= ["Taśma flagowa z lewej strony, haczyki taśmowe, obszyte boki", "Taśma flagowa z lewej strony karabińczyki flagowe, obszyte boki", "Tunel po lewej, u góry zszyty reszta obszyta"]
    if product == "POLYFLAG": 
        methods= ["Taśma flagowa z lewej strony, haczyki taśmowe, obszyte boki", "Taśma flagowa z lewej strony karabińczyki flagowe, obszyte boki", "Tunel po lewej, u góry zszyty reszta obszyta"]
    return render_template('materials.html', product=product, materials=methods)
@app.route('/products/materials/methods/<url>')
def details(url):
    product = url
    session['method'] = product
    for i in session:
        print('sesion item name:', i)
        print(i, session[i])
    return('hhh')


app.run()
