#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform, QImage
import math, time, threading

from PyQt5 import QtCore

class Robot(QLabel):

    """
    clase Singleton que vamos a reutilizar en varias modulos del paquete2
    """

    robot = None
    def __init__(self, clase):
        # QLabel recibe como parametro la clase que lo invoca, para en en esta lo escriba
        super(QLabel,self).__init__(clase)
        self.clase = clase
        self.posX = self.clase.grafico.x() + (self.clase.grafico.width() // 2)
        self.posY = self.clase.grafico.y() + (self.clase.grafico.height() // 2)
        self.angulo = 0
        self.m = 0
        self.b = self.posY
        self.orientacion = 'o'
        self.rotation = 0

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

    def modificar(self):
        angR = self.angulo*(math.pi/180)
        self.m = math.tan(angR)
        self.b = self.posY-(self.m*self.posX)
        self.definirOrientacion()

    def nuevoY(self):
        self.posY = self.posX*self.m+self.b

    def nuevoX(self):
        self.posX = (self.posY-self.b)/self.m

    def avanzarXPos(self):
        self.posX += 5
        self.nuevoY()
        self.move(self.posX, self.posY)

    def avanzarXNeg(self):
        self.posX -= 5
        self.nuevoY()
        self.move(self.posX, self.posY)

    def avanzarYPos(self):
        self.posY += 5
        self.nuevoX()
        self.move(self.posX, self.posY)

    def avanzarYNeg(self):
        self.posY -= 5
        self.nuevoX()
        self.move(self.posX, self.posY)

    def limites(self):
        centerX = self.posX + self.centerX
        centerY = self.posY + self.centerY
        return (centerX > self.clase.grafico.x()+70 and centerY>self.clase.grafico.y()+50 and centerX<self.clase.grafico.x()+self.clase.grafico.width()-100 and centerY < self.clase.grafico.y()+self.clase.grafico.height()-120)


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

    def rotatePos(self):

        pixmap = QPixmap(self.img)
        self.rotation += 5
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.angulo = math.fabs(self.rotation % 360)
        self.modificar()


    def rotateNeg(self):
        pixmap = QPixmap(self.img)
        self.rotation -= 5
        transform = QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.angulo = math.fabs(self.rotation % 360)
        self.modificar()

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


    def circulo(self):
        hilo = threading.Thread(target=self.cir)
        hilo.setDaemon(True)
        hilo.start()

    def cir(self):
        for i in range(72):
            self.moverAdelante()
            time.sleep(0.01)
            self.moverAdelante()
            time.sleep(0.01)
            self.rotateNeg()
            time.sleep(0.02)

    def informacion(self):
        print("posX = {}, posY = {}, m = {}, b = {}, angulo = {}, orientacio = {}".format(self.posX,self.posY,self.m,self.b,self.angulo, self.orientacion))

    def getInstance(clase):
        if Robot.robot == None:
            Robot.robot = Robot(clase)
        return Robot.robot