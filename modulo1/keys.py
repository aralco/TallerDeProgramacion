#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Keys(object):

    def __init__(self):
        self.keys = {}

    def agregarEvento(self, tecla, funcion):
        self.keys[tecla] = funcion

    def removerEvento(self, tecla):
        del self.keys[tecla]


    def keyPressEvent(self, e):
        for tecla in self.keys.keys():
            if e.key() == ord(tecla):
                self.keys[tecla]()
