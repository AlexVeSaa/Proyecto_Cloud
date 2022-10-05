from calendar import c
from re import A
from flask import Flask, render_template, request,flash,redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
 
#Add Database local
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/proyectos"

#Database concectado a Amazon WS
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://Alex:Admin1234@44.202.81.95/examen"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SECRET_KEY']='My super secret that no one is supposed to know'

#Initialize the Database
db =SQLAlchemy(app)

#Create Model LIBROS
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False) 
    regionNacimiento = db.Column(db.String(100))
    ranking= db.relationship('Ranking', backref='autor', lazy=True)

class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(100))
    titulo = db.Column(db.String(100))
    ranking= db.relationship('Ranking', backref='libros', lazy=True)

class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor_id=db.Column(db.Integer,db.ForeignKey('autor.id'),nullable=False)
    libros_id=db.Column(db.Integer,db.ForeignKey('libros.id'),nullable=False)

#FORMULARIOS 
class AutorForm(FlaskForm):
    nombreAutor =StringField('Nombre', validators=[DataRequired()])
    apellidoAutor =StringField('Apellido', validators=[DataRequired()])
    regionAutor =StringField('Lugar de Nacimiento', validators=[DataRequired()])

class LibrosForm(FlaskForm):
    generoLibros =StringField('Genero', validators=[DataRequired()])
    tituloLibros =StringField('Titulo', validators=[DataRequired()])
    

@app.route('/nav')
def nav():
    return render_template('prueba.html')

@app.route('/login')
def login():
    return render_template('index1.html')

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/insertar',methods=['GET','POST'])
def insertar():
    form_libros = LibrosForm()
    form_autor = AutorForm()
    libros = None
    autor = None

    if form_libros.validate_on_submit():
        libros = Libros.query.filter_by(id = form_libros.id.data).first()
        if libros is None:
            libros = Libros(genero = form_libros.generoLibros.data, titulo = form_libros.tituloLibros.data)
            db.session.add(libros)
            db.session.commit()
    else: return render_template('insertar.html', form_autor=form_autor)
    
    if form_autor.validate_on_submit():
        autor = Autor.query.filter_by(id = form_autor.id.data).first()
        if autor is None:
            autor = Autor(nombre = form_autor.nombreAutor.data, apellido = form_autor.apellidoAutor.data,regionNacimiento = form_autor.regionAutor.data)
            db.session.add(autor)
            db.session.commit()
        flash("Usuario añadido con exito")
    else: return render_template('insertar.html',form_libros=form_libros)

    autor_id = Autor.query.filter_by(codigo=autor.codigo).first().id
    db.session.add(Ranking(autor_id=autor_id))
    db.session.commit()
    return redirect(url_for('ranking'))

@app.route('/Libros')
def libros():
    form_libros = LibrosForm()
    libros = None

    if form_libros.validate_on_submit():
        libros = Libros.query.filter_by(codigo = form_libros.codigoLibros.data).first()
        if libros is None:
            libros = Libros(codigo = form_libros.codigoLibros.data, fechaPublicacion = form_libros.fecPublicLibros.data,
            genero = form_libros.generoLibros.data, titulo = form_libros.tituloLibros.data)
            db.session.add(libros)
            db.session.commit()
    else: return render_template('libros.html',form_libros=form_libros)
    libros_id = Libros.query.filter_by(codigo=libros.codigo).first().id
    db.session.add(Ranking(libros_id=libros_id))
    db.session.commit()
    return redirect(url_for('ranking'))

@app.route('/Nosotros')
def nosotros():
    return render_template('users/Nosotros.html')

@app.route('/Contacto')
def contacto():
    return render_template('users/Contacto.html')

@app.route('/ranking')
def ranking():
    rankings=Ranking.query.order_by(Ranking.id)
    lista=[]
    for ranking in rankings:
        autor = Autor.query.filter_by(id=ranking.autor_id).first()
        libros = Libros.query.filter_by(id=ranking.libros_id).first()
        lista.append({
            "codigoAutor":autor.codigo,
            "codigoLibros":libros.codigo
        })
    return render_template('ranking.html',lista=lista)

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)



