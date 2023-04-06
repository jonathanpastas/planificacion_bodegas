import psycopg2

db = psycopg2.connect(host="[host]", database="[bdname]", user="[userbd]", password="[passbd]")
#cur = db.cursor()

def queryDatos(user,contra):
    sql = "SELECT * FROM usuarios WHERE correo='"+str(user)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:

        email=row[2]
        contrasenia=row[3]

        #print(email)
        #print(contrasenia)
        if email == user and contrasenia == contra:
            return True
        else:
            return False

def perfiluser(user):

    dato=0
    sql = "SELECT * FROM usuarios WHERE correo='"+str(user)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        dato = row[4]
    return dato


def nombreuser(user):
    sql = "SELECT * FROM usuarios WHERE correo='" + str(user) + "'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        nombre = row[1]
    return nombre

def ciuser(user):
    sql = "SELECT * FROM usuarios WHERE correo='" + str(user) + "'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        ci = row[0]
    return ci

def menuopciones(perfils):
    sql="select descripcion,url from perfilxpagina,pagina where perfilxpagina.id_pagina=pagina.id_pagina and id_perfil = "+str(perfils)
    #print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    return data


def ingresopedidosnuevos(codcliente,detalle,cantidad,largo,ancho,alto,color,material,fecha_pedido,precio_nuevo,estado):
    try:
        sql ="INSERT INTO pedidosnuevos (cod_cliente,detalle,cantidad,largo,ancho,alto,color,material,fecha_pedido,preio_nuevo,estado) VALUES ("+"'"+str(codcliente)+"','"+str(detalle)+"','"+str(cantidad)+"','"+str(largo)+"','"+str(ancho)+"','"+str(alto)+"','"+str(color)+"','"+str(material)+"','"+str(fecha_pedido)+"','"+str(precio_nuevo)+"','"+str(estado)+"');"
      
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False



def pedidosrealizados(user):
    sql="SELECT ID_PEDIDO_NUEVO,DETALLE,CANTIDAD,FECHA_PEDIDO FROM PEDIDOSNUEVOS WHERE COD_CLIENTE="+"'"+user+"'"
  
    cursor = db.cursor()
    cursor.execute(sql)
    pedidos = cursor.fetchall()

    return pedidos

def detallepedidosid(id):
    sql = "SELECT ID_PEDIDO_NUEVO,DETALLE,CANTIDAD,FECHA_PEDIDO FROM PEDIDOSNUEVOS WHERE COD_CLIENTE=" + "'" + id+ "'"

    cursor = db.cursor()
    cursor.execute(sql)
    pedidos = cursor.fetchall()

    return pedidos

def catalago():
    sql = "SELECT * FROM PRODUCTO"
    
    cursor = db.cursor()
    cursor.execute(sql)
    ctlog = cursor.fetchall()

    return ctlog

def detalleproducto(id):
    sql = "SELECT * FROM PRODUCTO WHERE ID_PRODUCTO='"+id+"'"
  
    cursor = db.cursor()
    cursor.execute(sql)
    ctlog = cursor.fetchall()

    for row in ctlog:
        nombre=row[1]
        largo = row[3]
        ancho = row[4]
        alto = row[5]
        color = row[6]
        material=row[7]
        precio=row[8]

    return largo,ancho,alto,color,material,precio,nombre

def pedidoscatalogo(codigo,cantidad,fechapedido,fechaentrega,estado,idproducto,valorfinal):
    try:
        sql = "insert into pedidos (cod_cliente,cantidad,fecha_pedido,fecha_entrega,estado,id_producto,preciofinal) " \
              "values ('"+str(codigo)+"','"+str(cantidad)+"','"+str(fechapedido)+"','"+str(fechaentrega)+"','"+str(estado)+"','"+str(idproducto)+"','"+str(valorfinal)+"');"
       
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False


def mostrarpedidoscatalago(cod):
    
    sql="SELECT PEDIDOS.ID_PEDIDO,PEDIDOS.CANTIDAD,PEDIDOS.FECHA_PEDIDO,PEDIDOS.ESTADO,PRODUCTO.NOMBRE,PEDIDOS.PRECIOFINAL " \
        "FROM PEDIDOS,PRODUCTO WHERE PEDIDOS.ID_PRODUCTO=PRODUCTO.ID_PRODUCTO AND PEDIDOS.COD_CLIENTE='"+str(cod)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedidos = cursor.fetchall()
    return pedidos

def detallepednu(id,cod):

    
    sql = "SELECT DETALLE,CANTIDAD,LARGO,ANCHO,ALTO,COLOR,MATERIAL,FECHA_PEDIDO,PREIO_NUEVO,ESTADO FROM PEDIDOSNUEVOS" \
          " WHERE COD_CLIENTE='"+str(cod)+"' AND ID_PEDIDO_NUEVO='"+str(id)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedidos = cursor.fetchall()
    for row in pedidos:
        detalle = row[0]
        cantidad = row[1]
        largo = row[2]
        ancho = row[3]
        alto = row[4]
        color = row[5]
        material = row[6]
        fechap=row[7]
        precio=row[8]
        estado=row[9]

    if str(estado)=='0':
        et="PENDIENTE"
    if str(estado)=='1':
        et="EN PROCESO"
    if str(estado)=='2':
        et="FINALIZADO"
    if str(estado)=='3':
        et = "RECHAZADO"

    return detalle,cantidad,largo,ancho,alto,color,material,fechap,precio,et


def detallepedct(id,cod):
    
    sql = "SELECT PRODUCTO.NOMBRE,PEDIDOS.CANTIDAD,PEDIDOS.FECHA_PEDIDO,PEDIDOS.FECHA_ENTREGA,PEDIDOS.ESTADO,PEDIDOS.PRECIOFINAL " \
          "FROM PRODUCTO,PEDIDOS WHERE PEDIDOS.COD_CLIENTE='"+str(cod)+"' AND PEDIDOS.ID_PEDIDO='"+str(id)+"' AND PEDIDOS.ID_PRODUCTO=PRODUCTO.ID_PRODUCTO"
    cursor = db.cursor()
    cursor.execute(sql)
    pedidos = cursor.fetchall()
    for row in pedidos:
        nombre=row[0]
        cantidad=row[1]
        fecha_pedido=row[2]
        fechae=row[3]
        estadoc=row[4]
        preciof=row[5]

    if str(estadoc) == '0':
        et = "PENDIENTE"
    if str(estadoc) == '1':
        et = "EN PROCESO"
    if str(estadoc) == '2':
        et = "FINALIZADO"

    return nombre, cantidad, fecha_pedido, fechae, et, preciof

########################################################################OPERARIO#########################################################



def opmostrarpedidosnuevos():
    sql = "SELECT PEDIDOSNUEVOS.ID_PEDIDO_NUEVO,PEDIDOSNUEVOS.COD_CLIENTE,USUARIOS.NOMBRECLIENTE,PEDIDOSNUEVOS.DETALLE,PEDIDOSNUEVOS.FECHA_PEDIDO FROM PEDIDOSNUEVOS,USUARIOS WHERE PEDIDOSNUEVOS.COD_CLIENTE=USUARIOS.COD_CLIENTE AND PEDIDOSNUEVOS.ESTADO='0'"
    cursor = db.cursor()
    cursor.execute(sql)
    pednuevos = cursor.fetchall()
    return pednuevos

def opmostrarpedidosct():

   

    sql = "SELECT PEDIDOS.ID_PEDIDO,PEDIDOS.COD_CLIENTE,USUARIOS.NOMBRECLIENTE,PRODUCTO.NOMBRE,PEDIDOS.FECHA_PEDIDO FROM PEDIDOS,USUARIOS,PRODUCTO " \
          "WHERE PEDIDOS.COD_CLIENTE = USUARIOS.COD_CLIENTE AND PEDIDOS.ID_PRODUCTO = PRODUCTO.ID_PRODUCTO AND ESTADO='0'"
    cursor = db.cursor()
    cursor.execute(sql)
    pednuevosct = cursor.fetchall()
    return pednuevosct

def detallepct(idp):
    
    sql = "SELECT PRODUCTO.NOMBRE,PEDIDOS.CANTIDAD,PRODUCTO.LARGO,PRODUCTO.ANCHO,PRODUCTO.ALTO,PRODUCTO.COLOR,PRODUCTO.MATERIAL,PRODUCTO.PRECIO,PEDIDOS.PRECIOFINAL " \
          "FROM PRODUCTO,PEDIDOS WHERE PEDIDOS.ID_PEDIDO='"+str(idp)+"' AND PEDIDOS.ID_PRODUCTO = PRODUCTO.ID_PRODUCTO"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    for row in pedct:
        nombre=row[0]
        cantidad=row[1]
        largo=row[2]
        ancho=row[3]
        alto=row[4]
        color=row[5]
        material=row[6]
        precio=row[7]
        preciofinal=row[8]

    return nombre,cantidad,largo,ancho,alto,color,material,precio,preciofinal


def detallepn(id):
    
    sql = "SELECT PEDIDOSNUEVOS.DETALLE,PEDIDOSNUEVOS.CANTIDAD,PEDIDOSNUEVOS.LARGO,PEDIDOSNUEVOS.ANCHO,PEDIDOSNUEVOS.ALTO,PEDIDOSNUEVOS.COLOR,PEDIDOSNUEVOS.MATERIAL,PEDIDOSNUEVOS.FECHA_PEDIDO,PEDIDOSNUEVOS.ESTADO FROM PEDIDOSNUEVOS WHERE ID_PEDIDO_NUEVO='"+str(id)+"'"
    
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    for row in pedct:
        name = row[0]
        c = row[1]
        lr = row[2]
        an = row[3]
        at = row[4]
        cl = row[5]
        mt = row[6]
        fp = row[7]
        estado = row[8]

    if str(estado)=='0':
        et="PENDIETE"
    if str(estado)=='1':
        et="EN PROCESO"
    if str(estado)=='2':
        et="ENTREGADO"

    return name, c, lr, an, at, cl, mt, fp,et

def nombreusuario(id):
    sql="SELECT * FROM USUARIOS WHERE COD_CLIENTE='"+str(id)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    for row in pedct:
        name = row[1]
    return name

def aceptarpedido(id):
    try:
        sql ="UPDATE PEDIDOSNUEVOS SET ESTADO='1' WHERE ID_PEDIDO_NUEVO='"+str(id)+"'"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False



def ingresopednue(ryobi,sourz,uv,troqueladora,manuales,pegadora,fecha_produccion,id_pedido_nuevo):
    try:
        sql = "INSERT INTO PRODUCCIONNUEVA(ryobi,sourz,uv,troqueladora,manuales,pegadora,fecha_produccion,id_pedido_nuevo)VALUES(" \
              "'"+str(ryobi)+"','"+str(sourz)+"','"+str(uv)+"','"+str(troqueladora)+"','"+str(manuales)+"','"+str(pegadora)+"','"+str(fecha_produccion)+"','"+str(id_pedido_nuevo)+"',ESTADO='0')"
       
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False


def rechazarpedido(id):
    try:
        sql ="UPDATE PEDIDOSNUEVOS SET ESTADO='3' WHERE ID_PEDIDO_NUEVO='"+str(id)+"'"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

def cambiaprecio(pre,id):
    try:
        sql = "UPDATE PEDIDOSNUEVOS SET PREIO_NUEVO='"+str(pre)+"' WHERE ID_PEDIDO_NUEVO='" + str(id) + "'"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False


def ingresopednuect(ryobi,sourz,uv,troqueladora,manuales,pegadora,fecha_produccion,id_pedido):
    try:
        sql = "INSERT INTO PRODUCCION(ryobi,sourz,uv,troqueladora,manuales,pegadora,fecha_produccion,id_pedido)VALUES(" \
              "'"+str(ryobi)+"','"+str(sourz)+"','"+str(uv)+"','"+str(troqueladora)+"','"+str(manuales)+"','"+str(pegadora)+"','"+str(fecha_produccion)+"','"+str(id_pedido)+"');"
     
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

def aceptarpedidoct(id):
    try:
        sql ="UPDATE PEDIDOS SET ESTADO='1' WHERE ID_PEDIDO='"+str(id)+"'"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

#######################################################################################################################

def bdpedidon():

   
    sql = "SELECT PRODUCCIONNUEVA.ID_PRODUCCION_NUEVA,PRODUCCIONNUEVA.FECHA_PRODUCCION,PEDIDOSNUEVOS.DETALLE FROM PRODUCCIONNUEVA,PEDIDOSNUEVOS WHERE PRODUCCIONNUEVA.ID_PEDIDO_NUEVO=PEDIDOSNUEVOS.ID_PEDIDO_NUEVO AND PRODUCCIONNUEVA.ESTADO='0'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    return pedct

def bdinfo(pro):
    
    sql = "SELECT PED.DETALLE,PED.CANTIDAD,PED.LARGO,PED.ANCHO,PED.ALTO,PED.PREIO_NUEVO,PED.COLOR,PED.MATERIAL FROM PRODUCCIONNUEVA AS PN,PEDIDOSNUEVOS AS PED WHERE PN.ID_PEDIDO_NUEVO=PED.ID_PEDIDO_NUEVO AND PN.ID_PRODUCCION_NUEVA='"+str(pro)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()

    for row in pedct:
        detalles = row[0]
        cantidad = row[1]
        largo = row[2]
        ancho = row[3]
        alto = row[4]
        precio = row[5]
        color = row[6]
        material = row[7]

    return detalles,cantidad,largo,ancho,alto,precio,color,material

def bdinfoct(pro):
    
    sql = "SELECT PR.NOMBRE,PED.CANTIDAD,PR.LARGO,PR.ANCHO,PR.ALTO,PED.PRECIOFINAL,PR.COLOR,PR.MATERIAL FROM PRODUCCION AS PN,PEDIDOS AS PED ," \
          "PRODUCTO AS PR WHERE PN.ID_PEDIDO=PED.ID_PEDIDO AND PR.ID_PRODUCTO=PED.ID_PRODUCTO AND PN.ID_PRODUCCION='"+str(pro)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()

    for row in pedct:
        detalles = row[0]
        cantidad = row[1]
        largo = row[2]
        ancho = row[3]
        alto = row[4]
        precio = row[5]
        color = row[6]
        material = row[7]

    return detalles,cantidad,largo,ancho,alto,precio,color,material

def insertarbdnue(detalle,cantidad,largo,ancho,alto,precio,color,material,id_pro):
    try:
        sql = "INSERT INTO BODEGANUEVA (DESCRIPCION,CANTIDAD,LARGO,ANCHO,ALTO,PRECIO,COLOR,MATERIAL,ID_PRODUCCION_NUEVa) " \
              "VALUES ('"+str(detalle)+"','"+str(cantidad)+"','"+str(largo)+"','"+str(ancho)+"','"+str(alto)+"','"+str(precio)+"','"+str(color)+"','"+str(material)+"','"+str(id_pro)+"');"

        print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

def eliminapla(id):
    sql = "UPDATE PRODUCCIONNUEVA SET ESTADO='1' WHERE ID_PRODUCCION_NUEVA='"+id+"'"
    cursor = db.cursor()
    cursor.execute(sql)

def eliminaplact(id):
    sql = "UPDATE PRODUCCION SET ESTADO='1' WHERE ID_PRODUCCION='"+id+"'"
    cursor = db.cursor()
    cursor.execute(sql)


def verbodega():
    
    sql = "SELECT ID_BODEGA,DESCRIPCION,CANTIDAD,LARGO,ANCHO,ALTO,PRECIO,COLOR,MATERIAL FROM BODEGANUEVA"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    return pedct

def verbodegact():
  
    sql = "SELECT ID_BODEGA,DESCRIPCION,CANTIDAD,LARGO,ANCHO,ALTO,PRECIO,COLOR,MATERIAL FROM BODEGA"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    return pedct

def insertarbdct(detalle,cantidad,largo,ancho,alto,precio,color,material,id_pro):
    try:
        sql = "INSERT INTO BODEGA (DESCRIPCION,CANTIDAD,LARGO,ANCHO,ALTO,PRECIO,COLOR,MATERIAL,ID_PRODUCCION) " \
              "VALUES ('"+str(detalle)+"','"+str(cantidad)+"','"+str(largo)+"','"+str(ancho)+"','"+str(alto)+"','"+str(precio)+"','"+str(color)+"','"+str(material)+"','"+str(id_pro)+"');"

        print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False

def bdpedidoct():

    
    sql = "SELECT PRODUCCION.ID_PRODUCCION,PRODUCCION.FECHA_PRODUCCION,PRODUCTO.NOMBRE FROM PRODUCCION,PEDIDOS,PRODUCTO WHERE PRODUCCION.ID_PEDIDO=PEDIDOS.ID_PEDIDO AND PEDIDOS.ID_PRODUCTO=PRODUCTO.ID_PRODUCTO AND PRODUCCION.ESTADO='0'"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    return pedct




#########################################################################################################################
import numpy as np
def mcx():
    sql = "SELECT CANTIDAD,LARGO,ANCHO,ALTO,ESTADO,PRECIO FROM MC"
    cursor = db.cursor()
    cursor.execute(sql)
    pedct = cursor.fetchall()
    x=[]
    y=[]
    mat=[]
    maty=[]
    for row in pedct:
        mat= [row[0],row[1],row[2],row[3],row[4]]
        maty=[row[5]]
        y.append((maty))
        x.append(mat)
    return x,y

