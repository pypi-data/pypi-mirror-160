# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2021/1/7 15:17
# __fileName__ : GoldenCoordinateV2 Settings.py
# __devIDE__ : PyCharm


from PySide2 import QtCore as qtc


class Settings:


    def __init__(self, configFile):
        _Settings = qtc.QSettings(configFile, qtc.QSettings.IniFormat)
        _Settings.setIniCodec(qtc.QTextCodec.codecForName('utf-8'.encode()))
        _Settings.setAtomicSyncRequired(True)
        self._Settings = _Settings
        self._currentSec = ''

    def keys(self, section=""):
        self._Settings.beginGroup(section)
        keys = self._Settings.childKeys()
        self._Settings.endGroup()
        return keys

    def Sections(self):
        return self._Settings.childGroups()

    def setSection(self, section):
        self._currentSec = section


    def value(self,key, defaultValue=None, type=str):
        self._Settings.beginGroup(self._currentSec)
        value = self._Settings.value(key, defaultValue=defaultValue, type=type)
        self._Settings.endGroup()
        return value

    def setValue(self,key, value):
        self._Settings.beginGroup(self._currentSec)
        self._Settings.setValue(key, value)
        self._Settings.endGroup()

    def items(self, ks=None, section="", hidden=None):
        ks = (ks and set(ks) or set()).intersection(set(self.keys(section=section)))
        if hidden and isinstance(hidden, (list, tuple)):
            ks = set(self.keys(section=section)).difference(ks and set(ks) or set())
        return {
            k: self.value(k)
            for k in ks
        }









