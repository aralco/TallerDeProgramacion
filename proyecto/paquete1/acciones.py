#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import pygame
from lxml import etree
from .robot import Robot

def guardarXML(serializacion, ruta):
    archivo = open(ruta,"w")
    archivo.write(serializacion.decode("utf-8"))
    archivo.close()

# Evento
def grabarMovimiento(clase):
    pygame.init()
    robot = Robot.getInstance(clase)
    robot.ultimoMv = clase.obtenerKeyEvent(robot.mvDetenerse)
    robot.ultimoPz = clase.obtenerKeyEvent(robot.cerrarPz)

    reloj = pygame.time.Clock()
    ultimoMV = "inicio"
    raiz = etree.Element("auto")

    movimiento = etree.Element("datos")
    movimiento.set('posX', str(robot.posX))
    movimiento.set('posY', str(robot.posY))
    movimiento.set('m', str(robot.m))
    movimiento.set('b', str(robot.b))
    movimiento.set('orientacion', str(robot.orientacion))
    movimiento.set('angulo', str(robot.angulo))
    movimiento.set('ultimoPz', str(robot.ultimoPz))
    movimiento.set('ultimoMv', str(robot.ultimoMv))
    movimiento.set('rotation', str(robot.rotation))

    raiz.append(movimiento)

    while clase.grabando:
        if ultimoMV == 'inicio':
            reloj.tick()
            ultimoMV = robot.ultimoMv
            ultimoPz = robot.ultimoPz
        else:
            if robot.ultimoMv != ultimoMV or robot.ultimoPz != ultimoPz:
                reloj.tick()
                tiempo = reloj.get_time()
                movimiento = etree.Element("movimiento")
                movimiento.set('tiempo', str(tiempo))
                movimiento.set('movimiento', ultimoMV)
                movimiento.set('pinza', ultimoPz)
                raiz.append(movimiento)
                print("se gravo  movimiento : {}, pinzas : {},  con tiempo  {}".format(ultimoMV, ultimoPz, tiempo))
                ultimoMV, ultimoPz = robot.ultimoMv, robot.ultimoPz
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
    guardarXML(serializacion,"archivosXML/datos.xml")

    print("se termino de grabar")
    pygame.quit()

def reproducirMovimiento(clase):
    pygame.init()
    robot = Robot.getInstance(clase)
    raiz = etree.parse("archivosXML/datos.xml").getroot()
    datos = raiz[0]

    robot.posX = float(datos.get('posX'))
    robot.posY = float(datos.get('posY'))
    robot.m = float(datos.get('m'))
    robot.b = float(datos.get('b'))
    robot.orientacion = datos.get('orientacion')
    robot.angulo = float(datos.get('angulo'))
    robot.ultimoMv = datos.get('ultimoMv')
    robot.ultimoPz = datos.get('ultimoPz')
    robot.rotation = float(datos.get('rotation'))
    robot.move(robot.posX, robot.posY)

    for auto in raiz[1:]:
        tiempoActual = pygame.time.get_ticks()
        fin = tiempoActual+int(auto.get('tiempo'))
        clase.keys[auto.get('movimiento')]()
        clase.keys[auto.get('pinza')]()
        while True:
            if pygame.time.get_ticks() >=fin:
                break
    print("esto es todo")
    pygame.quit()

def grabarMov(clase):
    hiloMv = threading.Thread(target=grabarMovimiento, args=(clase,))
    hiloMv.setDaemon(True)
    hiloMv.start()

# evento
def reproMov(clase):
    hiloRm = threading.Thread(target=reproducirMovimiento, args=(clase,))
    hiloRm.setDaemon(True)
    hiloRm.start()
