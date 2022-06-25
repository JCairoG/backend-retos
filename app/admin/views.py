from flask import Flask,render_template,redirect,url_for,session,flash

from . import admin
from .forms import LoginForm, BiografiaForm,ProyectosForm

import pyrebase
from app.firebaseConfig import firebaseConfig

from app import fb

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

####LOGIN######
@admin.route('/')
def index():
  if ('token' in session):
    return render_template('admin/index.html')
  else:
    return redirect(url_for('admin.login'))

@admin.route('/login',methods=["GET","POST"])
def login():
  login_form = LoginForm()
  context = {
      'login_form':login_form
  }

  if login_form.validate_on_submit():
    usuarioData=login_form.usuario.data
    passwordData=login_form.password.data
    try:
      usuario = auth.sign_in_with_email_and_password(usuarioData,passwordData)
      dataUsuarioValido = auth.get_account_info(usuario['idToken'])
      session['token'] = usuario['idToken']
      return redirect(url_for('admin.index'))
    except:
      flash("Usuario o Paswword inválidos")

  return render_template('admin/login.html',**context)

@admin.route('/logout')
def logout():
  session.pop('token')
  return redirect(url_for('admin.login'))


####PANEL ADMIN######
@admin.route('/biografia',methods=["GET","POST"])
def biografia():
  if ('token' in session):
    dataBio = fb.getDocument('biografia','DieLgrgLjpktYnx852OA')  
    biografia_form = BiografiaForm(data=dataBio)

    if biografia_form.validate_on_submit():
      dataBio = {
        "nombre" : biografia_form.nombre.data,
        "resumen" : biografia_form.resumen.data,
        "rol" : biografia_form.rol.data,
        "foto" : biografia_form.foto.data,
        "ubicacion" : biografia_form.ubicacion.data,
        "cv" : biografia_form.cv.data,
        "github" : biografia_form.github.data,
        "twitter" : biografia_form.twitter.data
        }
      result = fb.updateDocument('biografia','DieLgrgLjpktYnx852OA',dataBio)
      flash("Datos Actualizados")

    context = {
     'biografia_form': biografia_form
    }
   
    return render_template('admin/biografia.html',**context)
  else:
    return redirect(url_for('admin.login'))


@admin.route('/proyectos',methods=["GET","POST"])
def proyectos():
  if ('token' in session):
    dataProy = fb.getCollection('proyectos')

    proyecto_form = ProyectosForm()

    if proyecto_form.validate_on_submit():
      dataProy ={
        "codigo": proyecto_form.codigo.data,
        "nombre": proyecto_form.nombre.data,
        "descripcion": proyecto_form.descripcion.data,
        "url": proyecto_form.url.data,
        "imagen": proyecto_form.imagen.data
      }
      nuevo = fb.insertDocument('proyectos',dataProy)
      flash("Proyecto registrado")
      return redirect(url_for('admin.proyectos'))

    context = {
      'proyectos': dataProy,
      'proyecto_form': proyecto_form
    }
    return render_template('admin/proyectos.html',**context)

  else:
    return redirect(url_for('admin.login'))

@admin.route('/proyectoEdit/<id>',methods=["GET","POST"])
def proyectoEdit(id=''):
  if ('token' in session):
    proyectoActualizar = fb.getDocument('proyectos',id)  
    dataProy = fb.getCollection('proyectos')
    proyecto_form = ProyectosForm(data=proyectoActualizar)
    
    if proyecto_form.validate_on_submit():
      dataProy ={
        "codigo": proyecto_form.codigo.data,
        "nombre": proyecto_form.nombre.data,
        "descripcion": proyecto_form.descripcion.data,
        "url": proyecto_form.url.data,
        "imagen": proyecto_form.imagen.data
      }
      nuevo = fb.updateDocument('proyectos',id,dataProy)
      flash("Proyecto actualizado")
      return redirect(url_for('admin.proyectos'))
      
    context = {
      'proyectos': dataProy,
      'proyecto_form': proyecto_form
    }
    return render_template('admin/proyectos.html',**context)

  else:
    return redirect(url_for('admin.login'))

@admin.route('/proyectoDel/<id>',methods=["GET","POST"])
def proyectoDel(id=''):
  if ('token' in session):
    dataProy = fb.getCollection('proyectos')
    proyecto_form = ProyectosForm()

    fb.deleteDocument('proyectos',id)
    flash("Proyecto eliminado")
    context = {
      'proyectos': dataProy,
      'proyecto_form': proyecto_form
    }
    return render_template('admin/proyectos.html',**context)

  else:
    return redirect(url_for('admin.login'))