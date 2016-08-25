import random
import time
import copy
import sqlite3
import time
import platform # for Check what OS you running on
import os # for clearing screan

bu_gun_tarih  = time.strftime("%d.%m.%Y", time.localtime())
vt = sqlite3.connect('database.sqlite')
db = vt.cursor()

db.execute("CREATE TABLE IF NOT EXISTS yerler (yer, puan, tarih)")

tam_liste = []
tmp_liste = []

def yedi_gun_sayac(veri_tarihi, bu_gun_tarih):
    if veri_tarihi[2] != bu_gun_tarih[2]:
        return True
    elif veri_tarihi[1] != bu_gun_tarih[1]:
        return True
    elif int(bu_gun_tarih[0]) - int(veri_tarihi[0]) >= 7:
        return True
    else:
        return False

tmp_tarih = ""
bu_gun_tarih_list = []
for i in bu_gun_tarih:
    if i == ".":
        bu_gun_tarih_list.append(tmp_tarih)
        tmp_tarih = ""
    else:
        tmp_tarih += i
bu_gun_tarih_list.append(tmp_tarih)

def tam_liste_ayarla():
    db.execute("SELECT * FROM yerler")

    veriler = db.fetchall()

    for veri in veriler:
        tmp_tarih = ""
        veri_tarihi_list = []
        for i in veri[2]:
            if i == ".":
                veri_tarihi_list.append(tmp_tarih)
                tmp_tarih = ""
            else:
                tmp_tarih += i
        veri_tarihi_list.append(tmp_tarih)
        if yedi_gun_sayac(veri_tarihi_list, bu_gun_tarih_list):
            db.execute("UPDATE yerler SET tarih = '{0}' WHERE yer = '{1}'".format(bu_gun_tarih, veri[0]))
            db.execute("UPDATE yerler SET puan = 5 WHERE yer = '{0}'".format(veri[0]))
            vt.commit()
        if int(veri[1]) > 1:
            tam_liste.append(veri[0])

tam_liste_ayarla()
tmp_liste = copy.deepcopy(tam_liste)

def clear_screan():
    if platform.system() == "Windows":
        os.system('cls')  # on windows
    else:
        os.system('clear') # on linux / os x

def yer_ekle():
    print("Çıkış: Boş Enter")
    while True:
        yemek_yeri = input("Yemek Yeri: ")
        if yemek_yeri in tam_liste:
            print("Bu seçenek zaten ekli !\n")
        elif yemek_yeri == "":
            return
        else:
            db.execute("INSERT INTO yerler VALUES ('{0}', 5, '{1}')".format(yemek_yeri, bu_gun_tarih))
            tmp_liste.append(yemek_yeri)
            vt.commit()
        tam_liste_ayarla()

while True:

    clear_screan()

    while len(tmp_liste) < 2:
        print("Database Boş Lütfen Birşeyler Ekleyiniz !")
        yer_ekle()

    giris = input("Yeni Birşey Eklemek İster Misiniz (Evet: 1): ")
    if giris == "1":
        yer_ekle()

    tam_liste_ayarla()
    db = vt.cursor()

    clear_screan()

    inpt = input("Çevir: \n")

    del_liste = copy.deepcopy(tmp_liste)

    liste = []
    secilen = ""

    while del_liste != []:
        secilen = random.choice(del_liste)
        liste.append(secilen)
        del_liste.remove(secilen)

    for i in liste:
        print(i)
        time.sleep(0.3)

    print("\nSeçilen: " + liste[-1])
    inpt = input("Güzel Mi ? (Hayır: 0)")

    db.execute("SELECT puan FROM yerler WHERE yer = '{0}'".format(liste[-1]))
    puan = db.fetchall()[0][0]
    db.execute("SELECT * FROM yerler")
    if inpt == "0":
        db.execute("UPDATE yerler SET puan = {0} WHERE yer = '{1}'".format(int(puan)-1, liste[-1]))
        tmp_liste.remove(liste[-1])
        vt.commit()
        if tmp_liste == []:
            tam_liste_ayarla()
    else:
        if int(puan) < 10:
            db.execute("UPDATE yerler SET puan = {0} WHERE yer = '{1}'".format(int(puan)+1, liste[-1]))
            vt.commit()
        break
if vt:
    vt.commit()
    vt.close()
