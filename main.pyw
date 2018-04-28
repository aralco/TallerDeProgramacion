#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from paquete1.ventana import Ventana
import sys


if __name__ == "__main__":

    app = QApplication(sys.argv)
    rutaImagenes = "imagenes/"
    ventana = Ventana( rutaImagenes)

    ventana.agregarEvento('O', ventana.label.mvAdelante)
    ventana.agregarEvento('S', ventana.label.mvAtras)
    ventana.agregarEvento('D', ventana.label.rtPos)
    ventana.agregarEvento('A', ventana.label.rtNeg)
    ventana.agregarEvento('X', ventana.label.mvDetenerse)
    #ventana.agregarEvento('Q', ventana.label.circulo)
    ventana.agregarEvento('R', ventana.label.abrirPz)
    ventana.agregarEvento('T', ventana.label.cerrarPz)

    ventana.agregarClickEvent(ventana.grabar,ventana.veriGrabar)
    ventana.agregarClickEvent(ventana.reproducir,ventana.reproducirMovimiento)


    ventana.show()
    app.exec_()