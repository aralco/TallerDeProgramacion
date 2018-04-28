#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pygame
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform, QImage
import math, time, threading
from lxml import etree
from PyQt5 import QtCore

class Robot(QLabel):

    """
    clase Singleton que vamos a reutilizar en varias modulos del paquete2
    """

    robot = None
    def __init__(self, clase):
        # QLabel recibe como parametro la clase que lo invoca, para en en esta lo escriba
        pygame.init()
        super(QLabel,self).__init__(clase)
        self.clase = clase
        self.posX = self.clase.grafico.x() + (self.clase.grafico.width() // 2)
        self.posY = self.clase.grafico.y() + (self.clase.grafico.height() // 2)
        self.angulo = 0
        self.m = 0
        self.b = self.posY
        self.orientacion = 'o'
        self.rotation = 0
        #self.cir()
        self.estados = {'adelante':[False,self.moverAdelante],
                        'atras':[False,self.moverAtras],
                        'rotarPos':[False,self.rotatePos],
                        'rotarNeg':[False, self.rotateNeg],
                        'detenido':[True, self.detenerse]}
        self.estadosPinzas = {'abierta':[False,self.abrirPinzas],
                              'cerrada':[True,self.cerrarPinzas]}

        self.hilo = threading.Thread(target=self.moverse)
        self.hilo.setDaemon(True)
        self.hilo.start()

        self.ultimoMv = None
        self.ultimoPz = None

    # clase
    def cargarImg(self,rutaImg,auto):
        self.img = QImage()
        self.rutaImg = rutaImg+auto
        self.img.load(self.rutaImg+"/cerrar.png")
        pixmap = QPixmap(self.img)
        self.centerX = pixmap.rect().center().x()
        self.centerY = pixmap.rect().center().y()
        diag = (pixmap.width() ** 2 + pixmap.height() ** 2) ** 0.5
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setPixmap(pixmap)
        self.setGeometry(self.posX, self.posY, diag, diag)

    # clase
    def modificar(self):
        angR = self.angulo*(math.pi/180)
        self.m = math.tan(angR)
        self.b = self.posY-(self.m*self.posX)
        self.definirOrientacion()

    # clase
    def nuevoY(self):
        self.posY = self.posX*self.m+self.b

    # clase
    def nuevoX(self):
        self.posX = (self.posY-self.b)/self.m

    # clase
    def avanzarXPos(self):
        self.posX += 5
        self.nuevoY()
        self.move(self.posX, self.posY)

    # clase
    def avanzarXNeg(self):
        self.posX -= 5
        self.nuevoY()
        self.move(self.posX, self.posY)

    # clase
    def avanzarYPos(self):
        self.posY += 5
        self.nuevoX()
        self.move(self.posX, self.posY)

    # clase
    def avanzarYNeg(self):
        self.posY -= 5
        self.nuevoX()
        self.move(self.posX, self.posY)

    # clase
    def limites(self):
        centerX = self.posX + self.centerX
        centerY = self.posY + self.centerY
        return (centerX > self.clase.grafico.x()+70 and centerY>self.clase.grafico.y()+50 and centerX<self.clase.grafico.x()+self.clase.grafico.width()-100 and centerY < self.clase.grafico.y()+self.clase.grafico.height()-120)


    # clase
    def moverAdelante(self):
        if (self.angulo >= 0 and self.angulo <= 45) or (self.angulo >= 316 and self.angulo <= 360):
            self.avanzarXPos()
            if not self.limites():
                self.avanzarXNeg()
        elif (self.angulo >= 46 and self.angulo <= 135):
            self.avanzarYPos()
            if not self.limites():
                self.avanzarYNeg()
        elif (self.angulo >= 136 and self.angulo <= 225):
            self.avanzarXNeg()
            if not self.limites():
                self.avanzarXPos()
        elif (self.angulo >= 226 and self.angulo <= 315):
            self.avanzarYNeg()
            if not self.limites():
                self.avanzarYPos()

    # clase
    def moverAtras(self):
        if (self.angulo >= 0 and self.angulo <= 45) or (self.angulo >= 316 and self.angulo <= 360):
            self.avanzarXNeg()
            if not self.limites():
                self.avanzarXPos()
        elif (self.angulo >= 46 and self.angulo <= 135):
            self.avanzarYNeg()
            if not self.limites():
                self.avanzarYPos()
        elif (self.angulo >= 136 and self.angulo <= 225):
            self.avanzarXPos()
            if not self.limites():
                self.avanzarXNeg()
        elif (self.angulo >= 226 and self.angulo <= 315):
            self.avanzarYPos()
            if not self.limites():
                self.avanzarYNeg()

    # clase
    def rotatePos(self):

        pixmap = QPixmap(self.img)
        self.rotation += 5
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.angulo = math.fabs(self.rotation % 360)
        self.modificar()

    # clase
    def rotateNeg(self):
        pixmap = QPixmap(self.img)
        self.rotation -= 5
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.angulo = math.fabs(self.rotation % 360)
        self.modificar()

    # facade
    def mvAdelante(self):
        for clave in self.estados.keys():
            if clave == 'adelante':
                self.estados[clave][0] = True
            else:
                self.estados[clave][0] = False

        self.ultimoMv = self.clase.obtenerKeyEvent(self.mvAdelante)

    # facade
    def mvAtras(self):
        for clave in self.estados.keys():
            if clave == 'atras':
                self.estados[clave][0] = True
            else:
                self.estados[clave][0] = False

        self.ultimoMv = self.clase.obtenerKeyEvent(self.mvAtras)

    # facade
    def rtPos(self):
        for clave in self.estados.keys():
            if clave == 'rotarPos':
                self.estados[clave][0] = True
            else:
                self.estados[clave][0] = False

        self.ultimoMv = self.clase.obtenerKeyEvent(self.rtPos)

    # facade
    def rtNeg(self):
        for clave in self.estados.keys():
            if clave == 'rotarNeg':
                self.estados[clave][0] = True
            else:
                self.estados[clave][0] = False

        self.ultimoMv = self.clase.obtenerKeyEvent(self.rtNeg)

    # facade
    def mvDetenerse(self):
        for clave in self.estados.keys():
            if clave == 'detenido':
                self.estados[clave][0] = True
            else:
                self.estados[clave][0] = False
        self.ultimoMv = self.clase.obtenerKeyEvent(self.mvDetenerse)

    # clase
    def detenerse(self):
        pass

    # facade
    def abrirPz(self):
        for clave in self.estadosPinzas.keys():
            if clave == 'abierta':
                self.estadosPinzas[clave][0] = True
            else:
                self.estadosPinzas[clave][0] = False
        self.ultimoPz = self.clase.obtenerKeyEvent(self.abrirPz)

    # facade
    def cerrarPz(self):
        for clave in self.estadosPinzas.keys():
            if clave == 'cerrada':
                self.estadosPinzas[clave][0] = True
            else:
                self.estadosPinzas[clave][0] = False
        self.ultimoPz = self.clase.obtenerKeyEvent(self.cerrarPz)

    # clase
    def moverse(self):
        while True:
            time.sleep(.05)
            for value in self.estados.values():
                if value[0]:
                    value[1]()

            for value in self.estadosPinzas.values():
                if value[0]:
                    value[1]()

    # clase
    def definirOrientacion(self):
        if self.angulo == 0:
            self.orientacion = 'o'
        elif self.angulo == 90:
            self.orientacion = 's'
        elif self.angulo == 180:
            self.orientacion = 'e'
        elif self.angulo == 270:
            self.orientacion = 'n'
        elif self.angulo >0 and self.angulo<90:
            self.orientacion = 'so'
        elif self.angulo >90 and self.angulo<180:
            self.orientacion = 'se'
        elif self.angulo >180 and self.angulo<270:
            self.orientacion = 'ne'
        elif self.angulo >180 and self.angulo<360:
            self.orientacion = 'no'

    # clase
    def abrirPinzas(self):
        self.img = QImage()
        self.img.load(self.rutaImg+"/abrir.png")
        pixmap = QPixmap(self.img)
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    # clase
    def cerrarPinzas(self):
        self.img = QImage()
        self.img.load(self.rutaImg+"/cerrar.png")
        pixmap = QPixmap(self.img)
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    # falta definir a donde va por el momento va ir en la clase
    """
    def cir(self):
        raiz = etree.Element("auto")
        for i in range(72):

            movimiento = etree.Element("movimiento")
            movimiento.set('tiempo', str(100))
            movimiento.set('movimiento', 'W')
            movimiento.set('pinza', 'T')
            raiz.append(movimiento)

            m3 = etree.Element("movimiento")
            m3.set('tiempo', str(50))
            m3.set('movimiento', 'A')
            m3.set('pinza', 'T')
            raiz.append(m3)

        doc = etree.ElementTree(raiz)
        serializacion = etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="utf-8")
        archivo = open("circulo.xml", "w")
        archivo.write(serializacion.decode("utf-8"))
        archivo.close()
    """


     # clase
    def informacion(self):
        print("posX = {}, posY = {}, m = {}, b = {}, angulo = {}, orientacio = {}, ultimoMV = {}, ultimoPz = {}".format(self.posX,self.posY,self.m,self.b,self.angulo, self.orientacion,self.ultimoMv ,self.ultimoPz))

    # clase
    def getInstance(clase):
        if Robot.robot == None:
            Robot.robot = Robot(clase)
        return Robot.robot
