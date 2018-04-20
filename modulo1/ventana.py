#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QComboBox, QPushButton
from PyQt5 import uic
from .robot import Robot
from .keys import Keys
from PyQt5.QtCore import Qt,QEvent

class Ventana(QMainWindow,Keys):

    def __init__(self,rutaImg):
        pygame.init()
        super(QMainWindow,self).__init__()
        self.setWindowTitle("Robot")
        widthP = pygame.display.Info().current_w
        heightP = pygame.display.Info().current_h
        uic.loadUi("proyecto.ui",self)

        self.setGeometry(0, 0, widthP, heightP)
        self.label = Robot.getInstance(self)
        self.label.cargarImg(rutaImg,self.autos.currentText())
        self.grafico.setGeometry(100,100,widthP-200,heightP-200)
        self.label.show()


        # self.label.informacion()

    def closeEvent(self,event):
        resultado = QMessageBox.question(self,"salir...","seguro que quieres salir ?", QMessageBox.Yes | QMessageBox.No )
        if resultado == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()