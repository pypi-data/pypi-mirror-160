#! /usr/bin/python

from os import path, mkdir
from appdirs import user_config_dir, user_data_dir
from configparser import ConfigParser as conf

class source():

    def __init__(self):
        self.dirData = user_data_dir("jadwal-shalat")
        if not path.isdir(self.dirData):
            mkdir(self.dirData)
        self.confDir = user_config_dir()
        self.cfg = conf()
    
    def config(self):
        if not path.isfile(f"{self.confDir}/jadwal-shalat.ini"):
            self.cfg.add_section("Lokasi")
            self.cfg.set("Lokasi", "id lokasi", "")
            self.cfg.set("Lokasi", "lokasi", "")
            with open(f"{self.confDir}/jadwal-shalat.ini", "w") as configFile:
                self.cfg.write(configFile)
        else:
            self.cfg.read(f"{self.confDir}/jadwal-shalat.ini")

        idLokasi = self.cfg["Lokasi"]["id lokasi"]
        lokasi = self.cfg["Lokasi"]["lokasi"]
        return idLokasi, lokasi

    def setConfig(self, idLokasi, lokasi):
        self.cfg.set("Lokasi", "id lokasi", idLokasi)
        self.cfg.set("Lokasi", "lokasi", lokasi)
        with open(f"{self.confDir}/jadwal-shalat.ini", "w") as configFile:
            self.cfg.write(configFile)

    def tahun(self, kota, tahun):
        if not path.isdir(f"{self.dirData}/{kota}/{tahun}"):
            mkdir(f"{self.dirData}/{kota}")
            mkdir(f"{self.dirData}/{kota}/{tahun}")
    
    def bulan(self, kota, tahun, bulan):
        bulan = f"{self.dirData}/{kota}/{tahun}/{bulan}"
        return bulan
