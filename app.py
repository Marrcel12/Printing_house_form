from flask import Flask, render_template, request
from test import SignUpForm
app = Flask(__name__)
app.config['SECRET_KEY']= 'qaz123'
app.config['TEMPLATES_AUTO_RELOAD'] = "True"

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/start')
def test():
    return render_template('start.html')

@app.route('/products/<url>')
def products(url):
    product=url
    if product == 'baner':
        materials=[['FRONTLIT',"Idealny do zastosowania na zewnątrz"],['MESH (SIATKA)','Idealny do zastosowania na zewnątrz, na dużych powierzchniach lub miejscach o dużym nasileniu wiatru'],['BLOCKOUT', 'Idealny do wyeksponowania oferty po dwóch stronach baneru'],['POLIESTER 205g','Idealny do zastosowania wewnątrz'],['Poliester 115g','Idealny do zastosowania wewnątrz i do flag']]
    if product == 'sticker':
        materials=[['FOLIA BłYSZCZĄCA'],['FOLIA MATOWA'],['EASY DOT', "Folia umożliwiająca przeniesienie wydruku w inne miejsce bez utraty właściwości klejących materiału"], ["MAGNEZ BŁYSZCZĄCY"]]
    if product == 'pad':
        materials=[['DYWAN','Idealny do zastosowania np. jako wycieraczka'],['FLOORPROMOTOR','Idealny do zastosowania np. jako podkładka pod myszkę']]
    if product == 'poster':
        materials=[['PAPIER 150g', 'Idealny do drukowania plakató lub ulotek (druk jednostronny)'],['PAPIER 200g','Idealny do drukowania dyplomów']]
    if product == 'flag':
        materials=['POLIESTER 115g',['POLYFLAG','Idealny do zastosowania w miejscach o dużym nasileniu wiatru']]
    
    return render_template('products.html',product=product,materials=materials )

@app.route('/products/materials/<url>' )
def materials(url):
    return(url)

app.run()