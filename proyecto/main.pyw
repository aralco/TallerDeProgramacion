#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from paquete1.ventana import Ventana
import sys
from paquete1.robot import Robot

if __name__ == "__main__":

    app = QApplication(sys.argv)
    rutaImagenes = "imagenes/"
    ventana = Ventana( rutaImagenes)

    ventana.agregarEvento('W', Robot.getInstance(Ventana).mvAdelante)
    ventana.agregarEvento('S', Robot.getInstance(ventana).mvAtras)
    ventana.agregarEvento('D', Robot.getInstance(ventana).rtPos)
    ventana.agregarEvento('A', Robot.getInstance(ventana).rtNeg)
    ventana.agregarEvento('X', Robot.getInstance(ventana).mvDetenerse)
    ventana.agregarEvento('R', Robot.getInstance(ventana).abrirPz)
    ventana.agregarEvento('T', Robot.getInstance(ventana).cerrarPz)

    ventana.agregarClickEvent(ventana.grabar,ventana.veriGrabar)
    ventana.agregarClickEvent(ventana.reproducir,ventana.reproducirMovimiento)
    ventana.show()
    app.exec_()