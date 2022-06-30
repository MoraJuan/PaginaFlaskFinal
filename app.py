from flask import Flask, render_template, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from usuario import ClaseUsuario

__sesionactual = ClaseUsuario()

app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import Ingrediente, db
from models import Usuario, Receta

@app.route('/')
def usuario():
    return render_template('Iniciar.html')

@app.route('/bienvenida',methods = ['GET','POST'])
def bienvenida():
    return render_template('bienvenida.html')

@app.route('/incio_sesion', methods = ['GET','POST'])
def iniciar_sesion():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            return render_template('error.html')
        else:
            usuario_actual = Usuario.query.filter_by(correo = request.form['email']).first()
            if usuario_actual is None:
                return render_template('error.html')
            else:
                clave_cifrada = hashlib.md5(bytes(request.form['password'], encoding = "utf-8"))
                if clave_cifrada.hexdigest() == usuario_actual.clave:
                    __sesionactual.addusuario(usuario_actual)
                    return render_template('bienvenida.html')
                else:
                    return render_template('error.html')
    else:
        return render_template('receta.html')

@app.route('/recetas', methods = ['GET', 'POST'])
def recetas():
    if request.method == 'POST':
        if request.form['nombre'] and request.form['tiempo'] and request.form['elaboracion']:
            nueva_receta = Receta(nombre=request.form['nombre'],tiempo=request.form['tiempo'] ,elaboracion=request.form['elaboracion'],cantidadmegusta = 0,fecha = datetime.now(), usuarioid = __sesionactual.getUsuario().id)
            db.session.add(nueva_receta)
            db.session.commit()
            receta_actual = Receta.query.filter_by(nombre = request.form['nombre']).first()
            __sesionactual.addreceta(receta_actual.usuarioid)
            print(receta_actual.id)
            return render_template('ingredientes.html', cantidad_ingrediente=0, receta = receta_actual.id)
        else:
            return render_template('error.html')
    else:
        return render_template('receta.html')

@app.route('/ingredientes' , methods = ['GET', 'POST'])
def ingredientes():
    if request.method == 'POST':
        if request.form['nombre'] and request.form['Cantidad'] and request.form['Unidad']:            
            cant=request.form['i']
            cant = int(cant)
            id = request.form['id']
            print(id)
            nuevo_ingrediente = Ingrediente(nombre=request.form['nombre'],cantidad=request.form['Cantidad'] ,unidad=request.form['Unidad'], recetaid = id)
            db.session.add(nuevo_ingrediente)
            db.session.commit()
            if cant<9:
                cant = cant + 1
                return render_template('ingredientes.html', cantidad_ingrediente=cant, receta = id)
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    else:
        return render_template('ingredientes.html')

@app.route('/ranking', methods = ['POST', 'GET'])
def lista_ranking():
    return render_template('rankings.html', receta = Receta.query.order_by(desc(Receta.cantidadmegusta)).limit(5).all())

@app.route('/listar_tiempo', methods = ['POST', 'GET'])
def listar_tiempo():
    if request.method ==  'POST':
        if request.form['tiempo']:
            return render_template('listar_tiempo2.html', tiempo = request.form['tiempo'], receta = Receta.query.filter(Receta.tiempo < int(request.form['tiempo'] )).all())
    else:
        return render_template('listar_tiempo.html')

@app.route('/incrementarMeGusta', methods = ['POST', 'GET'])
def incrementar():
    if request.method == 'POST':
        if request.form['megusta']:
                receta_actual = Receta.query.get(request.form['recetaid'])
                receta_actual.cantidadmegusta+=1
                db.session.commit()
                return render_template('aviso.html')
    return render_template('listar_tiempo2.html')

@app.route('/listar_ingrediente', methods = ['GET', 'POST'])
def listar_ingredientes():
    if request.method == 'POST':
        if request.form['ingredientes']:
            ing = request.form['ingredientes']
            search = "%{}%".format(ing)
            return render_template('listar_ingrediente2.html', ingrendientes = request.form['ingredientes'], Ingrediente =  Ingrediente.query.filter(Ingrediente.nombre.like(search)).all(), sesion = __sesionactual.getUsuario().id)
    else:
        return render_template('listar_ingrediente.html', ingrediente = None)

@app.route('/incrementarMeGusta', methods = ['POST', 'GET'])
def incrementar2():
    if request.method == 'POST':
        if request.form['megusta']:
                receta_actual = Receta.query.get(request.form['recetaid'])
                receta_actual.cantidadmegusta+=1
                db.session.commit()
                return render_template('aviso.html')
    return render_template('listar_ingrediente2.html')

@app.route('/informacion_receta', methods = ['GET', 'POST'])
def inforeceta():
    if request.method == 'POST':
        if request.form['ver']:
            receta_actual = Receta.query.get(request.form['recetaid'])
            return render_template('inforeceta.html', receta = receta_actual, sesion = __sesionactual.getUsuario().id)
    else:
        return render_template('inforeceta.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)