#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, threading, time
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QComboBox, QPushButton,QGraphicsView
from PyQt5 import uic
from .robot import Robot
from .eventos import Eventos
from .acciones import grabarMov,reproMov

class Ventana(QMainWindow,Eventos):

    def __init__(self,rutaImg):
        pygame.init()
        super(QMainWindow,self).__init__()
        self.setWindowTitle("Robot")
        widthP = pygame.display.Info().current_w
        heightP = pygame.display.Info().current_h
        uic.loadUi("archivosUi/proyecto.ui",self)
        self.setGeometry(0, 0, widthP, heightP)
        self.grafico.setGeometry(100,100,widthP-200,heightP-200)
        robot =  Robot.getInstance(self)
        robot.cargarImg(rutaImg, 'auto1')
        robot.show()
        self.imprimir = threading.Thread(target=self.informacion, args=(robot,))
        self.imprimir.setDaemon(True)
        #self.imprimir.start()
        self.grabando = False


    def informacion(self, robot):
        while True:
            time.sleep(.10)
            robot.informacion()

    def veriGrabar(self):
        self.grabando = False if self.grabando else True
        if self.grabando:
            grabarMov(self)

    def reproducirMovimiento(self):
        reproMov(self)

    def closeEvent(self,event):
        resultado = QMessageBox.question(self,"salir...","seguro que quieres salir ?", QMessageBox.Yes | QMessageBox.No )
        if resultado == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()