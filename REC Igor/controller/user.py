from flask import Flask, Blueprint, request,render_template,session,flash,redirect,url_for,make_response,abort
from model.viagens import Viagem,lista_viagem
from json import *

userController= Blueprint('user',__name__)



@userController.route('/', methods= ["GET","POST"])
def add():
    if request.method == "POST":
        destino = request.form.get("destino")
        data = request.form.get("data")
        desc = request.form.get("desc")
        avaliacao = request.form.get("av")
        if destino and data and desc and avaliacao:
            viagem=Viagem(destino,data, desc, avaliacao)
            lista_viagem.append(viagem.__dict__)
            session['viagem']= lista_viagem
            flash('Viagem adicionada com sucesso','success')
            return redirect(url_for("user.set_cookie"))

        else:
            flash('preencha todos os campos para adicionar a viagem', 'error')

    return render_template('add.html')

@userController.route('/lista')
def lista():
    nViagens= request.cookies.get('viagens')
    return render_template('lista.html', viagens= session.get('viagem'), nViagens=nViagens)

@userController.route("/excluir-lista")
def excluir():
    session.pop('viagem', None)
    return redirect(url_for("user.delete_cookie"))

@userController.route("/set_cookie")
def set_cookie():
    resp =make_response("cookie criado!")
    num=str(len(session.get('viagem', [])))
    resp.set_cookie('viagens',num, max_age=60*60*24*7)
    return resp

@userController.route("/get_cookie")
def get_cookie():
    nViagens= request.cookies.get('viagens')
    if nViagens:
        return f'numero de viagens cadastradas: {nViagens}'
    else:
        'nenhuma viagem encontrada'


@userController.route("/delete_cookie")
def delete_cookie():
    resp =make_response("cookie deletado!")
    resp.set_cookie('viagens', '', expires=0)
    return resp

rotaPriv=['user.lista']
all_rotas=['user.lista', 'user.add', 'user.delete_cookie','user.get_cookie','user.set_cookie','user.excluir']


@userController.before_request
def autenticar_rotas():
    viagens=session.get('viagem')
    if not viagens and request.endpoint in rotaPriv:
        return redirect(url_for('user.add'))
    if request.endpoint not in all_rotas:
        abort(404)
    
    
@userController.errorhandler(404)
def pageNotFound(e):
    return render_template("404.html"), 404

@userController.errorhandler(500)
def ErroInterno(e):
    return render_template("500.html"), 500
