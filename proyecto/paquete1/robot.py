#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform, QImage
import math, time, threading
from PyQt5 import QtCore

class Robot(QLabel):

    robot = None
    def __init__(self, clase):
        super(QLabel,self).__init__(clase)
        self.clase = clase
        self.posX = self.clase.grafico.x() + (self.clase.grafico.width() // 2)
        self.posY = self.clase.grafico.y() + (self.clase.grafico.height() // 2)
        self.angulo = 0
        self.m = 0
        self.b = self.posY
        self.orientacion = 'o'
        self.rotation = 0
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

    def modificarEcuacion(self):
        angR = self.angulo*(math.pi/180)
        self.m = math.tan(angR)
        self.b = self.posY-(self.m*self.posX)
        self.definirOrientacion()

    def moveImgXPositivo(self):
        self.posX += 5
        self.posY = self.posX * self.m + self.b
        self.move(self.posX, self.posY)

    def moveImgXNegativo(self):
        self.posX -= 5
        self.posY = self.posX * self.m + self.b
        self.move(self.posX, self.posY)

    def moveImgYPositivo(self):
        self.posY += 5
        self.posX = (self.posY - self.b) / self.m
        self.move(self.posX, self.posY)

    def moveImgYNegativo(self):
        self.posY -= 5
        self.posX = (self.posY - self.b) / self.m
        self.move(self.posX, self.posY)

    def isLimit(self):
        centerX = self.posX + self.centerX
        centerY = self.posY + self.centerY
        return (centerX > self.clase.grafico.x()+70 and centerY>self.clase.grafico.y()+50 and centerX<self.clase.grafico.x()+self.clase.grafico.width()-100 and centerY < self.clase.grafico.y()+self.clase.grafico.height()-120)

    def moverAdelante(self):
        if (self.angulo >= 0 and self.angulo <= 45) or (self.angulo >= 316 and self.angulo <= 360):
            self.moveImgXPositivo()
            if not self.isLimit():
                self.moveImgXNegativo()
        elif (self.angulo >= 46 and self.angulo <= 135):
            self.moveImgYPositivo()
            if not self.isLimit():
                self.moveImgYNegativo()
        elif (self.angulo >= 136 and self.angulo <= 225):
            self.moveImgXNegativo()
            if not self.isLimit():
                self.moveImgXPositivo()
        elif (self.angulo >= 226 and self.angulo <= 315):
            self.moveImgYNegativo()
            if not self.isLimit():
                self.moveImgYPositivo()

    def moverAtras(self):
        if (self.angulo >= 0 and self.angulo <= 45) or (self.angulo >= 316 and self.angulo <= 360):
            self.moveImgXNegativo()
            if not self.isLimit():
                self.moveImgXPositivo()
        elif (self.angulo >= 46 and self.angulo <= 135):
            self.moveImgYNegativo()
            if not self.isLimit():
                self.moveImgYPositivo()
        elif (self.angulo >= 136 and self.angulo <= 225):
            self.moveImgXPositivo()
            if not self.isLimit():
                self.moveImgXNegativo()
        elif (self.angulo >= 226 and self.angulo <= 315):
            self.moveImgYPositivo()
            if not self.isLimit():
                self.moveImgYNegativo()

    def rotatePos(self):

        pixmap = QPixmap(self.img)
        self.rotation += 3
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.angulo = math.fabs(self.rotation % 360)
        self.modificarEcuacion()

    def rotateNeg(self):
        pixmap = QPixmap(self.img)
        self.rotation -= 3
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.angulo = math.fabs(self.rotation % 360)
        self.modificarEcuacion()

    def abrirPinzas(self):
        self.img = QImage()
        self.img.load(self.rutaImg+"/abrir.png")
        pixmap = QPixmap(self.img)
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

    def cerrarPinzas(self):
        self.img = QImage()
        self.img.load(self.rutaImg+"/cerrar.png")
        pixmap = QPixmap(self.img)
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

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

    # facade
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


    def moverse(self):
        while True:
            time.sleep(.05)
            for value in self.estados.values():
                if value[0]:
                    value[1]()

            for value in self.estadosPinzas.values():
                if value[0]:
                    value[1]()

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

    def informacion(self):
        print("posX = {}, posY = {}, m = {}, b = {}, angulo = {}, orientacio = {}, ultimoMV = {}, ultimoPz = {}".format(self.posX,self.posY,self.m,self.b,self.angulo, self.orientacion,self.ultimoMv ,self.ultimoPz))

    def getInstance(clase):
        if Robot.robot == None:
            Robot.robot = Robot(clase)
        return Robot.robot
