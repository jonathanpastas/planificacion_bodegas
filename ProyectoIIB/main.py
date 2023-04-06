from flask import Flask, render_template, request, session, redirect, url_for,flash
from bdd import queryDatos,menuopciones,perfiluser,ciuser,nombreuser,ingresopedidosnuevos,pedidosrealizados,catalago,detalleproducto,pedidoscatalogo,mostrarpedidoscatalago,aceptarpedidoct
from bdd import detallepednu,detallepedct,opmostrarpedidosnuevos,opmostrarpedidosct,detallepct,detallepn,nombreusuario,aceptarpedido,ingresopednue,rechazarpedido,cambiaprecio,ingresopednuect
from bdd import bdpedidon,bdinfo,insertarbdnue,eliminapla,verbodega,insertarbdct,bdpedidoct,verbodegact,bdinfoct,eliminaplact,mcx
import time
import numpy as np
from sklearn import datasets, linear_model
import statsmodels.api as sm  ## Este proporciona funciones para la estimación de muchos modelos estadísticos
import statsmodels.formula.api as smf
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


app = Flask(__name__)
app.secret_key='jsp1234'

@app.route('/')
def index() -> 'html':
    return render_template('inicial.html', titulo='Sistema de Planificación de Pedidos')

@app.route('/info')
def info() -> 'html':
    return render_template('infopro.html', titulo='Sistema de Planificación de Pedidos')

@app.route('/login')
def login()-> 'html':
    return render_template('login.html')


@app.route('/ingresar' ,methods=['POST'])
def ingreso() -> 'html':
  user=request.form['correo']
  clave = request.form['clave']
  validar=queryDatos(user,clave)
)

  if validar == True:
      perfilu = perfiluser(user)
      nombre = nombreuser(user)
      cedula = ciuser(user)
      session['username']=user
      session['pass']=clave
      session['perfiluser']=perfilu
      session['nombre']=nombre
      session['ci']=cedula
      return redirect(url_for('paginicio'))
  else :
       flash("Error al Inciar Sesion. Por Favor Verifique sus Credenciales de Acceso")
       return  redirect(url_for('login'))


@app.route('/inicio')
def paginicio() -> 'html':

    if 'username' in session :
        print("true")
        menu=menuopciones(str(session['perfiluser']))
        usuario=session['username']
        nom = str(session['nombre'])
        return render_template('index.html', menu=menu,user=usuario,nombreusuario=nom)


    else :
        return redirect(url_for('index'))

################################# Metodo para cerrar la Sesion #######################################################
@app.route('/logout')
def salir() ->'html':
    session.clear()
    return redirect(url_for('index'))
#######################################################################################################################
@app.route('/registropedido',methods=['GET'])
def registropedido()-> 'html':
    if 'username' in session:
        valor = request.args.get('id')
        fecha=str(time.strftime("%d/%m/%y"))
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom=str(session['nombre'])
        ci=str(session['ci'])
        print(nom)
        ced=session['ci']
        l,a,al,co,ma,pre,no=detalleproducto(valor)
        return render_template('registropedidos.html', menu=menu,user=usuario,nombreusuario=nom,codigousuario=ci,fechap=fecha,
                               largo=l,ancho=a,alto=al,color=co,precio=pre,nombre=no,material=ma,id=valor)

    else:
        return redirect(url_for('index'))


@app.route('/pedidoscliente')
def verpedidosclie()-> 'html':

    if 'username' in session:

        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])

        ced = session['ci']
        ped=pedidosrealizados(ced)
        pedc=mostrarpedidoscatalago(ced)
        return render_template('pedidoscliente.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,tbpedidos=ped,tbpedidosc=pedc)
    else:
        return redirect(url_for('index'))


@app.route('/menupedidos')
def menupedidos()->'html':
    if 'username' in session:

        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        print(nom)
        ced = session['ci']
        return render_template('mnpedidos.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci)
    else:
        return redirect(url_for('index'))

@app.route('/pedidonuevo')
def nuevopedido()->'html':
    if 'username' in session:

        menu = menuopciones(str(session['perfiluser']))
        fecha = str(time.strftime("%d/%m/%y"))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])

        ced = session['ci']
        return render_template('productonuevo.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,fechap=fecha)
    else:
        return redirect(url_for('index'))


@app.route('/ordenproduccion')
def orden_producccion()->'html':
    if 'username' in session:

        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        tbpr=opmostrarpedidosnuevos()
        tbprc=opmostrarpedidosct()
        return render_template('ordenproduccion.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,tbpdn=tbpr,tbpdct=tbprc)
    else:
        return redirect(url_for('index'))

@app.route('/planificar', methods=['GET'])
def planificacion()->'html':
    if 'username' in session:
        menu = menuopciones(str(session['perfiluser']))
        valor = request.args.get('id')
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']

        return render_template('planificacion.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci)
    else:
        return redirect(url_for('index'))


@app.route('/planificarct',methods=['GET'])
def planificacionct()->'html':
    if 'username' in session:
        valor = request.args.get('id')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        nombre,cantidad,largo,ancho,alto,color,material,precio,preciofinal=detallepct(valor)
        return render_template('planificacionct.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,
                               n=nombre,c=cantidad,l=largo,a=ancho,al=alto,cl=color,mt=material,pr=precio,pf=preciofinal)
    else:
        return redirect(url_for('index'))

@app.route('/reportes')
def reportes() -> 'html':
    import pandas as pd
    if 'username' in session:
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        mat,maty=mcx()
        a=np.array(pd.DataFrame(mat))
        b=np.array(maty)
        X_train, X_test, y_train, y_test = train_test_split(a,b,test_size=0.3, random_state=40)
        lr = linear_model.LinearRegression()
        lr.fit(X_train, y_train)
        lr.coef_
        lr.intercept_
        Y_pred = lr.predict(X_test)
        print(Y_pred)
        precision=lr.score(X_train, y_train)
        algo="ALGORITMO DE REGRESION LINEAL MULTIPLE"

        def media(valores):
            return sum(valores) / len(valores)

        def evaluacion_rendimiento(yt, ypre):
            error = yt - ypre
            print(error)
            MAE = sum(abs(error)) / len(error)
            MSE = sum(pow(error, 2)) / len(error)
            RMSE = math.sqrt(MSE)
            SCE = sum(pow(error, 2))
            median = float(media(yt))
            STC = sum(pow(yt - median, 2))
            SCR = STC - SCE
            c = str(lr.coef_)
            coef = c.split()
            r2 = SCR / STC
            r2_adj = 1 - (1 - r2) * ((len(y_test) - 1) / (len(yt) - (len(coef) - 1) - 1))

            return MAE, MSE, RMSE, r2, r2_adj

        MAE1, MSE1, RMSE1, r21, r2_adj1 = evaluacion_rendimiento(y_test, Y_pred)
        ma=round(float(MAE1),2)
        mse=round(float(MSE1),2)
        rm=round(float(RMSE1),2)
        rs=round(float(r21),2)
        r2a=round(float(r2_adj1),2)



        return render_template('reportes.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,pre=precision,al=algo,
                               mae=ma,msee=mse,rmse=rm,r2=rs,r2aa=r2a)
    else:
        return redirect(url_for('index'))

@app.route('/bodega')
def bodega() -> 'html':
    if 'username' in session:
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        return render_template('reportes.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci)
    else:
        return redirect(url_for('index'))


@app.route('/ingresobodega')
def ingreso_bodega()->'html':
    if 'username' in session:
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        tb=bdpedidon()
        tbn=bdpedidoct()
        return render_template('bdpedidos.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,tbpednv=tb,tbpedct=tbn)
    else:
        return redirect(url_for('index'))


@app.route('/ingresopn', methods=['POST'])
def bdingresopn()->'html':
    if 'username' in session:
        codigo=str(request.form['codigoclie'])
        fechap=str(request.form['fecha'])
        descripcion=str(request.form['detalle'])
        cant=int(request.form['cantidad'])
        dimlargo=float(request.form['largo'])
        dimancho=float(request.form['ancho'])
        dimalto=float(request.form['alto'])
        color=str(request.form['color'])
        tmaterial=str(request.form['material'])
       
        estado="0"

       
        ingresar=ingresopedidosnuevos(codigo,descripcion,cant,dimlargo,dimancho,dimalto,color,tmaterial,fechap,0,str(estado))
        print(ingresar)
        

        if ingresar == True:
             flash("PEDIDO INGRESADO CORRECTAMENTE")
             return redirect(url_for('menupedidos'))
        else:
            flash("NO SE PUDO INGRESAR SU PEDIDO POR FAVOR VERIFIQUE QUE LOS CAMPOS ESTEN CORRECTOS")
            return redirect(url_for('nuevopedido'))
    else:
        return redirect(url_for('index'))


@app.route('/pedidodetalles',methods=['GET'])
def detallepedido()->'html':
    if 'username' in session:
        valor = request.args.get('id')
        print(valor)
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        detalle, cantidad, largo, ancho, alto, color, material, fechap, precio, estado=detallepednu(valor,ci)
        #print(estado)
        return render_template('detallepedido.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,numpedido=valor,
                               det=detalle,cant=cantidad,lar=largo,anc=ancho,alt=alto,col=color,mat=material,fp=fechap,pre=precio,est=estado)
    else:
        return redirect(url_for('index'))

@app.route('/pedidodetallesct',methods=['GET'])
def detallepedidoct()->'html':
    if 'username' in session:
        valor = request.args.get('idc')
        print(valor)
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        nombre, cantidad, fecha_pedido, fechae, estadoc, preciof=detallepedct(valor,ci)
       
        return render_template('detallepedidoct.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,numpedido=valor,
                               nom=nombre,cant=cantidad,fp=fecha_pedido,fe=fechae,est=estadoc,prf=preciof)
    else:
        return redirect(url_for('index'))


@app.route('/catalago')
def catalagoprod()->'html':
    if 'username' in session:

        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        dat=catalago()
        return render_template('catalago.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,tbcatalogo=dat)
    else:
        return redirect(url_for('index'))

@app.route('/ingresapedidocatalogo', methods=['POST'])
def ingresopedidocatalogo()->'html':
    if 'username' in session:
        codigo=str(request.form['codcliente'])
        cant = int(request.form['cantidad'])
        fechap=str(request.form['fechap'])
        fechae='12/12/2020'
        idproducto=str(request.form['idpro'])
        preciou=float(request.form['valor'])
        preciof=preciou*cant
        estado="0"

        ingresar=pedidoscatalogo(codigo,cant,fechap,fechae,estado,idproducto,preciof)
        print(ingresar)


        if ingresar == True:
             flash("PEDIDO INGRESADO CORRECTAMENTE")
             return redirect(url_for('menupedidos'))
        else:
            flash("NO SE PUDO INGRESAR SU PEDIDO POR FAVOR VERIFIQUE QUE LOS CAMPOS ESTEN CORRECTOS")
            return redirect(url_for('nuevopedido'))
    else:
        return redirect(url_for('index'))





@app.route('/planificardet',methods=['GET'])
def planificardet()->'html':
    if 'username' in session:
        valor = request.args.get('id')
        cod = request.args.get('cod')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        clie = nombreusuario(cod)
        nombre,cantidad,largo,ancho,alto,color,material,precio,preciofinal=detallepct(valor)
        return render_template('planificacionct.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,
                               n=nombre,c=cantidad,l=largo,a=ancho,al=alto,cl=color,mt=material,pr=precio,pf=preciofinal,codclient=cod,nomclie=clie,ped=valor)
    else:
        return redirect(url_for('index'))


@app.route('/planificardetnu',methods=['GET'])
def planificardetnu()->'html':
    if 'username' in session:
        valor = request.args.get('id')
        cod=request.args.get('cod')
        codc=request.args.get('cod')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        
        name, c, lr, an, at, cl, mt, fp,e=detallepn(valor)
        clie=nombreusuario(codc)

        return render_template('planificaciondet.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,
                               n=name,c=c,l=lr,a=an,al=at,cl=cl,mt=mt,fe=fp,est=e,nomclie=clie,ped=valor,codclient=cod)
    else:
        return redirect(url_for('index'))

@app.route('/aceptarpedidos',methods=['GET'])
def aceptacionpedidos()->'html':
    if 'username' in session:
        valor = request.args.get('id')
        cod=request.args.get('cod')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        acep=aceptarpedido(valor)
        clien = nombreusuario(cod)
       
        return render_template('planificacionnu.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,ped=valor,clie=clien,cod=cod)
    else:
        return redirect(url_for('index'))

@app.route('/rechazarpedido',methods=['GET'])
def rechazarped()->'html':
    if 'username' in session:
        valor = request.args.get('id')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        acep = rechazarpedido(valor)
        
        if acep == True:
            flash("PEDIDO RECHAZADO CORRECTAMENTE, EL CLIENTE PODRA VER EL ESTADO DEL PEDIDO COMO RECHAZADO")
            return redirect(url_for('orden_producccion'))
        else:
            flash("SE PRODUJO UN ERROR EN LA SOLICITUD")
            return redirect(url_for('orden_producccion'))

    else:
        return redirect(url_for('index'))

@app.route('/igprodnu',methods=['POST'])
def producnueva()->'html':
    if 'username' in session:
        ryobi = str(request.form['ryobi'])
        sourz = str(request.form['sorz'])
        uv = str(request.form['Uv'])
        troq = str(request.form['troqueladora'])
        manu = str(request.form['manuales'])
        peg = str(request.form['peg'])
        fech = str(time.strftime("%d/%m/%y"))
        id_p=str(request.form['ped'])
        precio=str(request.form['precio'])
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        cam=cambiaprecio(precio,id_p)
        ingre=ingresopednue(ryobi,sourz,uv,troq,manu,peg,fech,id_p)
        print(ingre)
        if ingre == True:
            flash("PRODUCCION INGRESADA CORRECTAMENTE")
            return redirect(url_for('orden_producccion'))
        else:
            flash("ERROR AL INGRESAR LA PRODUCCION")
            
            return redirect(url_for('aceptacionpedidos'))
    else:
        return redirect(url_for('index'))


@app.route('/ingresoctpro',methods=['POST'])
def igplanct()->'html':
    if 'username' in session:
        ryobi = str(request.form['ryobi'])
        sourz = str(request.form['sorz'])
        uv = str(request.form['Uv'])
        troq = str(request.form['troqueladora'])
        manu = str(request.form['manuales'])
        peg = str(request.form['peg'])
        fech = str(time.strftime("%d/%m/%y"))
        id_p=str(request.form['ped'])
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        cam=aceptarpedidoct(id_p)
        print(ryobi,sourz,uv,troq,manu,peg,fech,id_p)
        ingre=ingresopednuect(ryobi,sourz,uv,troq,manu,peg,fech,id_p)
        print(ingre)
        if ingre == True:
            flash("PRODUCCION INGRESADA CORRECTAMENTE")
            return redirect(url_for('orden_producccion'))
        else:
            flash("ERROR AL INGRESAR LA PRODUCCION")
            
            return redirect(url_for('aceptacionpedidos'))
    else:
        return redirect(url_for('index'))


@app.route('/bodeganu',methods=['GET'])
def ingresarbodnue()->'html':
    if 'username' in session:
        valor = request.args.get('pro')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        detalle, cantidad, largo, ancho, alto, precio, color, material=bdinfo(valor)
        ingr=insertarbdnue( detalle, cantidad, largo, ancho, alto, precio, color, material,valor)

        if ingr == True:
            eliminapla(valor)
            flash("INGRESO A BODEGA CORRECTAMENTE")
            return redirect(url_for('bodega_m'))
        else :
            flash("FALLO EL INGRESO A BODEGA CORRECTAMENTE")
            return redirect(url_for('ingreso_bodega'))

    else:
        return redirect(url_for('index'))

@app.route('/bodegadatos')
def bodega_m()->'html':
    if 'username' in session:
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        bo=verbodega()
        boct=verbodegact()
        return render_template('bodegadatos.html', menu=menu, user=usuario, nombreusuario=nom, codigousuario=ci,tbodega=bo,tbodegact=boct)
    else:
        return redirect(url_for('index'))


@app.route('/bodegact',methods=['GET'])
def bodegactn()->'html':
    if 'username' in session:
        valor = request.args.get('pro')
        menu = menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ci = str(session['ci'])
        ced = session['ci']
        detalles,cantidad,largo,ancho,alto,precio,color,material=bdinfoct(valor)
        ingr = insertarbdct(detalles, cantidad, largo, ancho, alto, precio, color, material, valor)

        if ingr == True:
            eliminaplact(valor)
            flash("INGRESO A BODEGA CORRECTAMENTE")
            return redirect(url_for('bodega_m'))
        else:
            flash("FALLO EL INGRESO A BODEGA CORRECTAMENTE")
            return redirect(url_for('ingreso_bodega'))

    else:
        return redirect(url_for('index'))



#######################################################################################################################
app.run(debug=True)

