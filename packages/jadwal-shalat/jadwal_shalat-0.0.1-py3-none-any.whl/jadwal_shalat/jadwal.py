#! /usr/bin/python

import requests as req
from .config import source
from datetime import datetime
from os import path

class shalat():

    def __init__(self):
        self.url = "https://api.myquran.com/v1/sholat"
        self.date = datetime.now()
        self.source = source()
    
    def cek(self):
            try:
                checkUrl = req.get(self.url)
                checkUrl.raise_for_status()
            except req.exceptions.RequestException as er:
                print(er)
                exit()
            except req.exceptions.ConnectionError as er:
                print(er)
                exit()
            except req.exceptions.Timeout as er:
                print(er)
                exit()
    
    def lokasi(self):
        lokasi = self.source.config()
        if lokasi[0] == "" and lokasi[1] == "":
            self.cek()
            kota = input("Masukan Nama Kota/Kabupaten : ")
            cariLokasi = req.get(f"{self.url}/kota/cari/{kota}")
            listLokasi = cariLokasi.json()
            listLokasi = listLokasi["data"]
            idLokasi = {}
            for lokasi in listLokasi:
                idLokasi[lokasi["lokasi"]] = lokasi["id"]
            if len(idLokasi) == 1:
                listIdLokasi = list(idLokasi.values())
                namaLokasi = list(idLokasi.keys())
                idLokasi = listIdLokasi[0]
                namaLokasi = namaLokasi[0]
            else:
                print(f"Ditemukan beberapa lokasi dengan nama '{kota}' silahkan pilih salah satu : ")
                for i, key in enumerate(list(idLokasi.keys())):
                    if (i + 1) % 2:
                        print("[", i, "]", "{:20}".format(key), end="\t")
                    else:
                        print("[", i, "]", key, end="\n")
                listLokasi = list(idLokasi.keys())
                pilihLokasi = int(input(f"Pilih Lokasi 0 - {len(listLokasi) - 1} : "))
                idLokasi = idLokasi[listLokasi[pilihLokasi]]
                namaLokasi = listLokasi[pilihLokasi]
            self.source.setConfig(idLokasi, namaLokasi)
            lokasi = self.source.config()
            return lokasi
        else:
            return lokasi

    def getJadwal(self):
        lokasi = self.lokasi()
        idLokasi = lokasi[0]
        namaLokasi = lokasi[1]
        self.source.tahun(namaLokasi, self.date.strftime("%Y"))
        bulan = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        for b in bulan:
            if not path.isfile(self.source.bulan(namaLokasi, self.date.strftime("%Y"), b)):
                print(f"Sedang mengunduh jadwal shalat {namaLokasi} bulan {b}")
                getJadwal = req.get(f"{self.url}/jadwal/{idLokasi}/{self.date.strftime('%Y')}/{b}")
                listJadwal = getJadwal.json()
                listJadwal = listJadwal["data"]["jadwal"]
                with open(self.source.bulan(namaLokasi, self.date.strftime("%Y"), b), "w") as jadwalPerbulan:
                    jadwalPerbulan.write(str(listJadwal))
        return namaLokasi

    def jadwal(self):
        lokasi = self.getJadwal()
        with open(self.source.bulan(lokasi, self.date.strftime("%Y"), self.date.strftime("%m")),"r") as jadwalShalat:
            jadwal = jadwalShalat.read()
        rpl = ["[{", "}",]
        for r in rpl:
            jadwal = jadwal.replace(r, "")
        jadwal = jadwal.split(", {")
        waktuShalat = filter(lambda tgl:self.date.strftime('%Y-%m-%d') in tgl, jadwal)
        waktuShalat = list(waktuShalat)
        waktuShalat = str(waktuShalat)
        rmt = ["'imsak':", "'subuh':", "'terbit':", "'dhuha':", "'dzuhur':", "'ashar':", "'maghrib':", "'isya':", '["', '"]', "'", "tanggal: ", " "]
        for r in rmt:
            waktuShalat = waktuShalat.replace(r, "")
        waktuShalat = waktuShalat.split(",")
        del waktuShalat[10]
        waktuShalat.append(lokasi)
        return waktuShalat

def display():
    Shalat = shalat()
    jadwalShalat = Shalat.jadwal()
    display = f"""\033[92m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣧⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⠀⠀⠀⠀⠀⠀⡌⠀⡆⠙⣆⠀
⠀⠀⠀⠀⠀⠀⣰⡻⡁⠀⠀⠀⠀⠀⠀⠸⣴⠒⢻⣳⠞⠀
⠀⠀⠀⠀⠀⠰⡡⠥⡷⠀⠀⠀⠀⠀⠀⠀⡆⣧⢸⢹⠆⠀
⠀⠀⢀⣤⠶⠛⠛⠛⠛⡲⢤⡀⠀⠀⠀⡤⣓⣻⣾⣾⣤⡀
⠀⣰⠟⠀⠀⠀⠀⠀⠀⠠⣷⣝⢆⠀⠀⢻⣗⡯⠯⣯⡽⠇
⢀⣿⣠⣤⡶⠶⢶⣯⣽⣿⡟⢿⣏⡆⠀⠀⢅⡠⡟⣿⡇⠀
⠀⢙⣉⣤⠭⠭⠽⣿⣿⣿⣿⣿⣾⠁⠀⠀⠀⣽⠁⡏⡇⠀
⠀⢰⠐⡆⢺⠀⠈⢱⠉⢸⡏⡟⢿⠀⠀⠀⡄⣩⠀⡗⡇⠀
⢀⡼⠖⣓⣉⣉⣩⣭⣭⣥⣤⣁⣉⡄⠀⠀⡇⣫⠀⡷⡇⠀
⢀⡉⠁⠀⠀⠀⢀⣼⠿⢿⣿⣿⣷⡆⠀⠀⡇⠛⠀⡧⡇⠀
⠀⠙⢿⣿⣿⣷⣿⣶⣶⣦⣽⣿⣿⣿⣦⣀⣧⣿⡀⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠃\033[0m
\033[1mJadwal Shalat {jadwalShalat[10]} 
Hari\t: {jadwalShalat[0]}, {jadwalShalat[1]}
Imsak\t: {jadwalShalat[2]}\t Subuh\t: {jadwalShalat[3]}
Terbit\t: {jadwalShalat[4]}\t Dhuha\t: {jadwalShalat[5]}
Dzuhur\t: {jadwalShalat[6]}\t Ashar\t: {jadwalShalat[7]}
Maghrib\t: {jadwalShalat[8]}\t Isya\t: {jadwalShalat[9]}
"""
    print(display)
