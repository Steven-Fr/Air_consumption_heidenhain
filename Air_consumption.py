#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
This module imports and starts all python masks.
The masks runs in the background.

The visibility of each mask is controlled in the mask file.
Example:
  Open the sub folder "masks" and the file "Mask_Example".
  Look at: embeddedWindow(plcSymbol = 'MG_PYM_Mask_Example')

Some masks can be imported in accordance with a PLC symbol.
Example:
  if jh.Get(GLOBAL_SYMBOL + PLC_OEMMACHINE_WINDOW_ACTIVE) is not None:
      import masks.oemMachine
The token "GLOBAL_SYMBOL" and "PLC_OEMMACHINE_WINDOW_ACTIVE" are defined in the file "common/plcSymbolDefinitions"

HOW TO CREATE A NEW MASK FILE?
 - Create a new file with the extension .py in the sub folder masks.
 - Import the new file name like:  import masks.example (without extension ).
 - Define all pygtk or plcgtk widgets in the new file.
 - For more details look into masks/example.py.

Author: JH PLC-Service / MCE / +49 (8669) 31-3102 / service.plc@heidenhain.de
Version: 2.3
"""

# IMPORT MODULS
#-----------------------------------------------------------
import os, sys

sys.path.append('../../')
from masks import * #import all standard libraries

import os.path
import pickle        # function to store and restore setups
import gobject       # gobject for global events
import os            # operating system functions
import pygtk
pygtk.require('2.0')
import gtk           # pygtk functions
import gtk.glade     # Glade XML description file functions
import pyjh          # JH interface, version
pyjh.require('3.4')
import jh            # Data-Access interface and Main-function
import jh.gtk        # jh.gtk class incl. window-registration
import jh.softkey    # jh softkey functions
import jh.gtk.glade  # jh.gtk Glade XML description file functions
import jh.note       # to show a note in the headline
import jh.event


import time
import datetime

import jh.spawn

#gtk.rc_parse( '../layout/oemGtkStyle%s.rc' %(jh.Get(GLOBAL_SYMBOL + PLC_RESOLUTION).values()[0]) )


gtk.rc_parse( '../../layout/OemGtkStyle_stv.rc')
# GTK_RC_PARSE_LAYOUT = '../layout/oemGtkStyle.rc'
#gtk.rc_parse(GTK_RC_PARSE_LAYOUT)  # define the window style


# CREATE THE WINDOW WITH ALL WIDGETS
#-----------------------------------------------------------
# create Window
myWindow = embeddedWindow(usage='PLCmedium', title = txt('Diagnosis air consumption'), focus = True, plcSymbol = "MG_SK_air_consumption")


notebook = gtk.Notebook()

myTableDiag0 = table()
myTableDiag0.set_border_width(5)
myTableDiag01 = table()
myTableDiag01.set_border_width(5)
myTableDiag1 = table()
myTableDiag1.set_border_width(5)
#2#myTableDiag2 = table()
#2#myTableDiag2.set_border_width(5)

################################################
date_actual =  time.localtime(time.time())                 #data completa di oggi

hours_act   = date_actual.tm_hour
days_act    = date_actual.tm_mday
months_act  = date_actual.tm_mon


today = datetime.date.today()                              #data completa di oggi
yesterday = today - datetime.timedelta(days=1)             #giorno prima
#hoursago = today - datetime.timedelta(hours=1)             #ora prima
testo2 = int(today.month)                                  #mese di oggi

count2 = 0
Zero01 = 0
Zero1 = 0
Zero2 = 0

########################-- Valiore istantaneo    --############################################
myTableDiag0.attachToCell(plcLevelBar(plcSymbol = "WG_machine_air_consumption", maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_LEFT_TO_RIGHT, width=400, height=30, barColors={400:'red',500:'yellow',700:'green'}, preText='',postText=''), col=2, row=3)






########################--Istogramma 0, 24 ore--############################################


#Leggo fino il numero della riga dell'ultimo valore salvato
LineN01 =jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\0\\LastLine" )
LineN01i = (LineN01['LastLine'])
LineN01i = int(LineN01i)
Start01 = LineN01i


#----------------------------------

textn01 = 25
Zero01 = int(0)    #valore 0 se la macchina era spenta
wline01 = 0        #contatore quante righe ho scritto
bar01 = 23         #contatore indice della barra che scrivo  0 a 23 (24 valori/colonne)

now = datetime.datetime.now().hour    #ora attuale
now = now - 1

while wline01 < 24:      #finche non ho scritto 24 colonne cicla
    if now < 0:
        now = 23
    if Start01 > 0:
        Datatime01 =jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\%i\\DataTime"%Start01)   #leggo la data da tabella ultima riga scritta
        Datatimes01 = (Datatime01['DataTime'])
        secondi = int(Datatimes01)                                                                           #trasformo in dato intero per leggerlo

        datapartenza01 = datetime.datetime(1970, 1, 1,0,0,0)                 #data di partenza del timer usato dal plc
        datapartenza01 = datapartenza01 + datetime.timedelta(hours=2)        #sembra che il plc abbia perso 2 ore dal 1970 contanto in secondi???
        datatabella01 = datapartenza01 + datetime.timedelta(seconds=secondi) #calcolo la data che segna in tabella in secondi
        datatabella01 = datatabella01.hour                                   #dalla data estraggo l'ora

#---    -------------------------------
        if datatabella01 == now:                                                                                  #l'ora presunta coincide con l'ora della tabella scrivi normalmente
            Value_air01 = jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\%i\\air_hour"%Start01 )   #leggi il valore in tabella
            Value_air_int01 = (Value_air01['air_hour'])
            Value_air_int01 = int(Value_air_int01)
            jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count01[%s]' %bar01: Value_air_int01})           #aseegna il valore in tabella alla barra
            Start01 = Start01 -1                                                                                  #passa al valore sucessivo
            bar01 = bar01 -1                                                                                      #passa alla barra sucessiva
            wline01 = wline01 +1                                                                                  #incremento il numero di colonne scritte per arrivare a 24
            #disegno la barra
            myTableDiag01.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count01[%s]" %(bar01+1), maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=(bar01+1), row=2)
            #scrivo l'ora sotto la barra
            myTableDiag01.attachToCell(gtk.Label((txt(now))),col=(bar01+1),row=3, xpadding=5)
            now = now - 1                                                                                         #decremento l'ora da controllare

        elif datatabella01 < now:                                                                 #se l'ora della riga è minore di quella aspettata la macchina è stata spenta per piu di un ora e
            jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count01[%s]' %bar01: Zero01})    #non ha scritto in tabella quel'ora quindi creo una barra con valore 0 e passo alla barra sucessiva
            bar01 = bar01 -1                                                                      #ricontrollando la stessa riga della tabella (non decremento start01)
            wline01 = wline01 +1
            myTableDiag01.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count01[%s]" %(bar01+1), maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=(bar01+1), row=2)
            myTableDiag01.attachToCell(gtk.Label(txt((now))),       col=(bar01+1),row=3, xpadding=5)
            now = now - 1
        elif datatabella01 > now:            #se maggiore c'è un anomalia nella tabella ignora il valore perchè è stata manomessa manualmente e passo alla riga sucessiva
            Start01 = Start01 -1
    else:
        jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count01[%s]' %bar01: Zero01})
        bar01 = bar01 -1
        wline01 = wline01 +1
        myTableDiag01.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count01[%s]" %(bar01+1), maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=(bar01+1), row=2)
        myTableDiag01.attachToCell(gtk.Label(txt((now))),       col=(bar01+1),row=3, xpadding=5)
        now = now - 1
########################################################################################################################################################








########################--Istogramma 1, 31 giorni--############################################

#Leggo fino il numero della riga dell'ultimo valore salvato
LineN1 =jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\0\\LastLine" )
LineN1i = (LineN1['LastLine'])
LineN1i = int(LineN1i)

Start1 = LineN1i

#----------------------------------

textn1 = 32
Zero1 = int(0)    #valore 0 se la macchina era spenta
wline1 = 0        #contatore quante righe ho scritto
bar1 = 30        #contatore indice della barra che scrivo  0 a 30 (31 valori/colonne)
Value_air_som1 = int(0)
count_som1 = 0
while wline1 < 31:      #finche non ho scritto 31 colonne cicla

    if Start1 > 0:
        Datatime =jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\%i\\DataTime"%Start1)   #leggo la data da tabella ultima riga scritta
        Datatimes = (Datatime['DataTime'])
        Datatimes = Datatimes/86400                                                                     #sec* min * hour = calcolo giorni
        giornitab = int(Datatimes)                                                                      #trasformo in dato intero per leggerlo
        datapartenza = datetime.date(1970, 1, 1)                                                        #data di partenza del timer usato dal plc
        datatabella = datapartenza + datetime.timedelta(days=giornitab)                                 #calcolo il giorno in cui è stato scritto il valore in tabella


#----------------------------------

        if datatabella == today:               #salto le ore precedenti e passo alla riga sucessiva fino al giorno prima
            print "datatabella"
            print "oggi"
            Start1 = Start1 -1

        elif datatabella == yesterday:
            print "ieri uguale"                                                                   #se la data presunta coincide con la data della tabella scrivi normalmente
            Value_air1 = jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\%i\\air_hour"%Start1 )   #leggi il valore in tabella
            Value_air_int1 = (Value_air1['air_hour'])
            Value_air_int1 = int(Value_air_int1)
            Value_air_som1 =  Value_air_int1  ###
            print Value_air_som1
            jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count1[%s]' %bar1: Value_air_som1})           #aseegna il valore in tabella alla barra
            count_som1 = 1
            Start1 = Start1 -1                                                                                 #passa al valore sucessivo
            bar1 = bar1 -1                                                                                     #bassa alla barra sucessiva
            wline1 = wline1 +1                                                                                 #incremento il numero di colonne scritte per arrivare a 31
            yesterday = yesterday - datetime.timedelta(days=1)
                                                             #decremento il giorno da controllare
            #disegno la barra
            myTableDiag1.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count1[%s]" %(bar1+1), maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=(bar1+1), row=4)
            #scrivo la data sotto la barra
            testo1 = (str(datatabella.day)+"/"+str(datatabella.month))
            myTableDiag1.attachToCell(gtk.Label(txt((testo1))),       col=(bar1+1),row=5, xpadding=5)


        elif datatabella < yesterday:     #se la data della riga è minore di quella aspettata la macchina è stata spenta per piu di un giorno e
            print "minore tab salta"              #non ha scritto in tabella quel giorno quindi credo una barra con valore 0 e passo alla barra sucessiva
                                          #ricontrollando la stessa riga della tabella
            jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count1[%s]' %bar1: Zero1})
            bar1 = bar1 -1
            wline1 = wline1 +1

            myTableDiag1.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count1[%s]" %(bar1+1), maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=(bar1+1), row=4)

            testo1 = (str(yesterday.day)+"/"+str(yesterday.month))
            myTableDiag1.attachToCell(gtk.Label(txt((testo1))),       col=(bar1+1),row=5, xpadding=5)

            yesterday = yesterday - datetime.timedelta(days=1)
        elif datatabella > yesterday:            #se maggiore devo sommare il valore

            print "maggiore tab somma"
            Value_air1 = jh.Get( "\\TABLE\\'PLC:\\TABLE\\hour_air_consumption.tab'\\NR\\%i\\air_hour"%Start1 )   #leggi il valore in tabella
            Value_air_int1 = (Value_air1['air_hour'])
            Value_air_int1 = int(Value_air_int1)
            print "faiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii"
            Value_air_som1 =  Value_air_som1 + Value_air_int1
            count_som1 = count_som1 +1
            jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count1[%s]' %(bar1+1): (Value_air_som1/count_som1)})
            Start1 = Start1 -1

    else:
        jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count1[%s]' %bar1: Zero1})
        bar1 = bar1 -1
        wline1 = wline1 +1

        myTableDiag1.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count1[%s]" %(bar1+1), maxValue= 1600,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=(bar1+1), row=4)

        testo1 = (str(yesterday.day)+"/"+str(yesterday.month))
        yesterday = yesterday - datetime.timedelta(days=1)
        myTableDiag1.attachToCell(gtk.Label(txt((testo1))),       col=(bar1+1),row=5, xpadding=5)

################################################################################################

### Istogramma 2, 12 mesi ###############################################################

#2#column = 0
#2#
#2#LineN2 =jh.Get( "\\TABLE\\'PLC:\\TABLE\\mounth_air_consumption.tab'\\NR\\0\\LastLine" )
#2#LineN2i = (LineN2['LastLine'])
#2#LineN2i = int(LineN2i)
#2#if LineN2i >= 12:
#2#    Start2 = LineN2i - 11
#2#
#2#else:
#2#    Start2 = 12
#2#
#2#
#2#for i in range(Start2,LineN2i+1):
#2#
#2#    count2 = count2
#2#    column = i+1
#2#    LineN2i = i+1
#2#
#2#    hours_act = hours_act + 1
#2#    if months_act > 12:
#2#       months_act = 1
#2#
#2#
#2#
#2#    Value_air2 =jh.Get( "\\TABLE\\'PLC:\\TABLE\\mounth_air_consumption.tab'\\NR\\%i\\air_moth"%i )
#2#    Value_air_int2 = (Value_air2['air_moth'])
#2#    Value_air_int2 = int(Value_air_int2)
#2#    jh.Put({'\\PLC\\program\\symbol\\global\\DG_levelbar_count2[%s]' %count2: Value_air_int2})
#2#
#2#
#2#    myTableDiag2.attachToCell(plcLevelBar(plcSymbol = "DG_levelbar_count2[%s]" %count2, maxValue= 700,   plcFactor=1,    orientation=gtk.PROGRESS_BOTTOM_TO_TOP, width=45, height=180, barColors={400:'red',500:'yellow',700:'green'},showText = True, preText='',postText=''), col=column, row=6)
#2#
#2#    testomesi = ""
#2#    if testo2 == 1:
#2#        testomesi = "Gen"
#2#    elif testo2 == 2:
#2#        testomesi = "Feb"
#2#    elif testo2 == 3:
#2#        testomesi = "Mar"
#2#    elif testo2 == 4:
#2#        testomesi = "Apr"
#2#    elif testo2 == 5:
#2#        testomesi = "Mag"
#2#    elif testo2 == 6:
#2#        testomesi = "Giu"
#2#    elif testo2 == 7:
#2#        testomesi = "Lug"
#2#    elif testo2 == 8:
#2#        testomesi = "Ago"
#2#    elif testo2 == 9:
#2#        testomesi = "Set"
#2#    elif testo2 == 10:
#2#        testomesi = "Ott"
#2#    elif testo2 == 11:
#2#        testomesi = "Nov"
#2#    elif testo2 == 12:
#2#        testomesi = "Dic"
#2#
#2#
#2#    myTableDiag2.attachToCell(gtk.Label(txt(testomesi)),       col=column,row=7, xpadding=5)
#2#    if testo2 >= 12:
#2#        testo2 = 0
#2#    testo2 = testo2 + 1
#2#    count2 = count2 + 1

############

vBoxMachine = gtk.VBox()
###############
frameStatus0 =  gtk.Frame(label=txt('Valore istantaneo'))
frameStatus0.add(myTableDiag0)

frameStatus01 =  gtk.Frame(label=txt('Media flusso orario (24h)'))
frameStatus01.add(myTableDiag01)

frameStatus1 =  gtk.Frame(label=txt('Media flusso orario per giorno (31gg)'))
frameStatus1.add(myTableDiag1)

#2#frameStatus2 =  gtk.Frame(label=txt('Media flusso orario per mese (12 mesi)'))
#2#frameStatus2.add(myTableDiag2)


###############

vBoxMachine.pack_start(frameStatus0, expand=True, fill=True, padding=5)
vBoxMachine.pack_start(frameStatus01, expand=True, fill=True, padding=5)
vBoxMachine.pack_start(frameStatus1, expand=True, fill=True, padding=5)
#2#vBoxMachine.pack_start(frameStatus2, expand=True, fill=True, padding=5)




labelAdd = gtk.Label(txt('Rilevazione dati portata aria macchina'))
notebook.append_page(vBoxMachine, labelAdd)


myWindow.pack_start(notebook, expand=True, fill=True)


jh.Main()