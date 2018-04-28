#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import pygame
from lxml import etree
from .robot import Robot
class Acciones():
    def __init__(self,clase):
        self.robot = Robot.getInstance(clase)
        self.clase = clase
        pygame.init()

    def guardarXML(self,serializacion, ruta):
        archivo = open(ruta,"w")
        archivo.write(serializacion.decode("utf-8"))
        archivo.close()

    # Evento
    def grabarMovimiento(self):
        self.robot.ultimoMv = self.clase.obtenerKeyEvent(self.robot.mvDetenerse)
        self.robot.ultimoPz = self.clase.obtenerKeyEvent(self.robot.cerrarPz)
        reloj = pygame.time.Clock()
        ultimoMV = "inicio"
        raiz = etree.Element("auto")

        movimiento = etree.Element("datos")
        movimiento.set('posX', str(self.robot.posX))
        movimiento.set('posY', str(self.robot.posY))
        movimiento.set('m', str(self.robot.m))
        movimiento.set('b', str(self.robot.b))
        movimiento.set('orientacion', str(self.robot.orientacion))
        movimiento.set('angulo', str(self.robot.angulo))
        movimiento.set('ultimoPz', str(self.robot.ultimoPz))
        movimiento.set('ultimoMv', str(self.robot.ultimoMv))
        movimiento.set('rotation', str(self.robot.rotation))

        raiz.append(movimiento)

        while self.clase.grabando:
            if ultimoMV == 'inicio':
                reloj.tick()
                ultimoMV = self.robot.ultimoMv
                ultimoPz = self.robot.ultimoPz
            else:
                if self.robot.ultimoMv != ultimoMV or self.robot.ultimoPz != ultimoPz:
                    reloj.tick()
                    tiempo = reloj.get_time()
                    movimiento = etree.Element("movimiento")
                    movimiento.set('tiempo', str(tiempo))
                    movimiento.set('movimiento', ultimoMV)
                    movimiento.set('pinza', ultimoPz)
                    raiz.append(movimiento)
                    print("se gravo  movimiento : {}, pinzas : {},  con tiempo  {}".format(ultimoMV, ultimoPz, tiempo))
                    ultimoMV, ultimoPz = self.robot.ultimoMv, self.robot.ultimoPz
        else:
            reloj.tick()
            tiempo = reloj.get_time()
            movimiento = etree.Element("movimiento")
            movimiento.set('tiempo', str(tiempo))
            movimiento.set('movimiento', ultimoMV)
            movimiento.set('pinza', ultimoPz)
            raiz.append(movimiento)
            print("se gravo  movimiento : {}, pinzas : {},  con tiempo  {}".format(ultimoMV,ultimoPz, tiempo))

        doc = etree.ElementTree(raiz)
        serializacion = etree.tostring( doc ,pretty_print=True, xml_declaration=True, encoding="utf-8")
        self.guardarXML(serializacion,"archivosXML/datos.xml")

        """
        archivo = open("archivosXML/datos.xml","w")
        archivo.write(serializacion.decode("utf-8"))
        archivo.close()
        """
        print("se termino de grabar")

    # evento
    def reproducirMovimiento(self):
        raiz = etree.parse("archivosXML/datos.xml").getroot()
        datos = raiz[0]

        self.robot.posX = float(datos.get('posX'))
        self.robot.posY = float(datos.get('posY'))
        self.robot.m = float(datos.get('m'))
        self.robot.b = float(datos.get('b'))
        self.robot.orientacion = datos.get('orientacion')
        self.robot.angulo = float(datos.get('angulo'))
        self.robot.ultimoMv = datos.get('ultimoMv')
        self.robot.ultimoPz = datos.get('ultimoPz')
        self.robot.rotation = float(datos.get('rotation'))
        self.robot.move(self.robot.posX, self.robot.posY)

        for auto in raiz[1:]:
            tiempoActual = pygame.time.get_ticks()
            fin = tiempoActual+int(auto.get('tiempo'))
            self.clase.keys[auto.get('movimiento')]()
            self.clase.keys[auto.get('pinza')]()
            while True:
                if pygame.time.get_ticks() >=fin:
                    break

        print("esto es todo")

    # evento
    def grabarMov(self):
        hiloMv = threading.Thread(target=self.grabarMovimiento)
        hiloMv.setDaemon(True)
        hiloMv.start()

    # evento
    def reproMov(self):
        hiloRm = threading.Thread(target=self.reproducirMovimiento)
        hiloRm.setDaemon(True)
        hiloRm.start()