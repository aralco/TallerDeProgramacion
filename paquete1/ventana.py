#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, threading, time
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QComboBox, QPushButton,QGraphicsView
from PyQt5.QtCore import Qt
from PyQt5 import uic
from .robot import Robot
from .keys import Keys
from .acciones import Acciones

class Ventana(QMainWindow,Keys):

    def __init__(self,rutaImg):
        pygame.init()
        super(QMainWindow,self).__init__()
        self.setWindowTitle("Robot")
        widthP = pygame.display.Info().current_w
        heightP = pygame.display.Info().current_h

        uic.loadUi("archivosUi/proyecto.ui",self)
        self.setGeometry(0, 0, widthP, heightP)
        self.grafico.setGeometry(100,100,widthP-200,heightP-200)
        self.label = Robot.getInstance(self)
        self.label.cargarImg(rutaImg, 'auto1')
        self.label.show()
        self.imprimir = threading.Thread(target=self.informacion)
        self.imprimir.setDaemon(True)
        #self.imprimir.start()
        self.grabando = False
        self.accionesRobot = Acciones(self)

    def informacion(self):
        while True:
            time.sleep(.10)
            self.label.informacion()

    def veriGrabar(self):
        self.grabando = False if self.grabando else True
        if self.grabando:
            #self.label.grabarMov()
            self.accionesRobot.grabarMov()

    def reproducirMovimiento(self):
        #self.label.reproMov()
        self.accionesRobot.reproMov()

    def closeEvent(self,event):
        resultado = QMessageBox.question(self,"salir...","seguro que quieres salir ?", QMessageBox.Yes | QMessageBox.No )
        if resultado == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()