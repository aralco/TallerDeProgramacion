#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from paquete1.ventana import Ventana
import sys


if __name__ == "__main__":

    app = QApplication(sys.argv)
    rutaImagenes = "imagenes/"
    ventana = Ventana( rutaImagenes)
    ventana.agregarEvento('W', ventana.label.moverAdelante)
    ventana.agregarEvento('S', ventana.label.moverAtras)
    ventana.agregarEvento('D', ventana.label.rotatePos)
    ventana.agregarEvento('A', ventana.label.rotateNeg)
    ventana.agregarEvento('Q', ventana.label.circulo)
    ventana.agregarEvento('R', ventana.label.abrirPinzas)
    ventana.agregarEvento('T', ventana.label.cerrarPinzas)

    ventana.show()
    app.exec_()