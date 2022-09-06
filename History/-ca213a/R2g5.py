# -*- coding: utf-8 -*-

# import pyqtgraph
# Copyright (c) 2012  University of North Carolina at Chapel Hill
# Luke Campagnola    ('luke.campagnola@%s.com' % 'gmail')

# Form implementation generated from reading ui file 'FRF_Analyzer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import os
from socket import if_indextoname
import sys
import warnings
from math import sqrt

import numpy as np
import pandas as pd
import scipy.linalg as la
from matplotlib.pyplot import (
    figure,
    grid,
    plot,
    savefig,
    show,
    subplot,
    xlabel,
    xlim,
    ylabel,
    ylim,
)
from pyqtgraph import LinearRegionItem, PlotWidget  # , mkPen
from PyQt5 import QtCore, QtWidgets
from scipy import interpolate  # QV
from scipy.signal import find_peaks, peak_widths

warnings.filterwarnings("ignore")

# path2local = 'C:/Users/qxo1686/python/__raw__/'
class Ui_FRF_Analyzer(object):
    prominences = {}
    widths = {}
    distances = {}
    x_peaks={}
    y_peaks={}
    l_base={}
    r_base={}
    trai_peaks = {}
    def __init__(self, df):
        """
        f: Der Zeilenvektor von Frequenz
        TF: Der Zeilenvektor von komplexen FRF
        abs_TF: Der Zeilenvektor von FRF-Amplitude
        phase: Der Spaltenvecktor von FRF-Phase
        coh: Der Zeilenvektor von Kohärenz
        f_column: Der Spaltenvektor von Frequenz
        TF_column: Der Spaltenvektor von komplexen FRF
        Nur Spaltenvektor kann in Funktion >sdof_cf< eingegeben werden
        """
        self.df=df
        self.trai = df.index
        self.features = list(df.columns)
        #find peaks
        for ft in self.features:
            prominence=0.5
            width=0
            distance=1
            self.find_feature_peaks(ft,prominence,width,distance)
            # self.prominences[ft] = 0.5
            # self.widths[ft]=0
            # self.distances[ft] = 1 
            # self.x_peaks[ft],self.l_base[ft],self.r_base[ft] = self.get_peaks(df[ft],self.prominences[ft],self.widths[ft],self.distances[ft])
            # self.y_peaks[ft]=df[ft].take(self.x_peaks[ft])
            # self.trai_peaks[ft] = self.trai.take(self.x_peaks[ft])

    def find_feature_peaks(self,ft,prominence,width,distance):
        self.prominences[ft] = prominence
        self.widths[ft]=width
        self.distances[ft] = distance
        self.x_peaks[ft],self.l_base[ft],self.r_base[ft] = self.get_peaks(self.df[ft],self.prominences[ft],self.widths[ft],self.distances[ft])
        if not isinstance(self.x_peaks[ft],list):
            self.x_peaks[ft]=self.x_peaks[ft].tolist()
        self.y_peaks[ft]=self.df[ft].take(self.x_peaks[ft])
        if not isinstance(self.y_peaks[ft],list):
            self.y_peaks[ft]=self.y_peaks[ft].tolist()
        self.trai_peaks[ft] = self.trai.take(self.x_peaks[ft])
        if not isinstance(self.trai_peaks[ft],list):
            self.trai_peaks[ft]=self.trai_peaks[ft].tolist()


    def get_peaks(self,signal,prominence=0.5,width=0,distance=1):
        # find peaks
        x_peak,_ =find_peaks(signal, prominence, width, distance)
        # get left and right bases
        # get l_base and r_base with peak_widths function
        _, _, l_base, r_base = peak_widths(signal, x_peak)
        l_base = (l_base // 1).astype(int)
        l_base = l_base.tolist()  # np.array to list
        r_base = (r_base // 1 + 1).astype(int)
        r_base = r_base.tolist()
        return x_peak,l_base,r_base

    # def sdof_fit(self):
    #     self.x_peak=self.x_peak.tolist()#np.array to list

    #     self.amp_peak = self.abs_TF[self.x_peak]
    #     self.amp_peak = self.amp_peak.tolist()

    #     self.coh_peak = self.coh[self.x_peak]
    #     self.coh_peak= self.coh_peak.tolist()
    #     self.dampings,self.eigenfrequenz, self.residuum = zip(*[self.sdof_cf(self.f_column,
    #                                         self.TF_column, self.l_base[i], self.r_base[i])
    #                     for i in range(len(self.l_base))])

    #     self.dampings=list(self.dampings)#tupel to list
    #     self.eigenfrequenz = np.array(self.eigenfrequenz).astype(int).tolist()

    #     self.residuum=np.sqrt(self.residuum)
    #     self.max_residuum = max(self.residuum)
    #     self.residuum=self.residuum/self.max_residuum
    #     self.residuum=self.residuum.tolist()

    def switch_feature(self):
        self.ft=self.cbo_features.currentText()
        self.main_view_plot()
        self.peak_view_plot()
        self.add_list_items()
        self.set_find_peaks_parameter()
        # fenster in mainview
        self.lr = LinearRegionItem()
        self.main_view.addItem(self.lr)
        # fenster in peakview
        self.lr2 = LinearRegionItem()
        self.peak_view.addItem(self.lr2)
        self.lr.sigRegionChangeFinished.connect(self.MainRegionUpdated)
        self.lr2.sigRegionChangeFinished.connect(self.PeakRegionUpdated)
        self.item_change()

    def main_view_plot(self):
        self.main_view.clear()
        self.main_view.plot(self.trai,df[self.ft].array)
        self.main_mark=self.main_view.plot(self.trai_peaks[self.ft], self.y_peaks[self.ft], pen = None, symbol='x',symbolPen = ('r'))

    def peak_view_plot(self):
        self.peak_view.clear()
        self.peak_view.plot(self.trai,df[self.ft].array)
        self.peak_view.plot(pen = ('y'))
        self.peak_view.plot(pen = None, symbol='x',symbolPen = ('r'))

    def add_list_items(self):
        """
        Alle Eigenfrequenzen als String in Liste >items< speichen
        Nur String kann in QListWidget >list_peaks< hinzugefügt werden
        """
        items = [f"trai {self.trai[i]}" for i in self.x_peaks[self.ft]]
        self.list_peaks.clear()
        self.list_peaks.addItems(items)
        self.list_peaks.setCurrentRow(0)
        
    def set_find_peaks_parameter(self):
        str_prominences=str(self.prominences[self.ft])
        str_width=str(self.widths[self.ft])
        str_distances=str(self.distances[self.ft])
        self.txt_prominence.setText(str_prominences)
        self.txt_width.setText(str_width)
        self.txt_distance.setText(str_distances)

    def item_change(self):
        """
        rownum: Nummer der ausgewählten Zeile der Spitze
        Fenster wird zur ausgewählten Spitze verschoben
        """
        rownum = self.list_peaks.currentRow()
        self.lr.setRegion([self.trai[self.l_base[self.ft][rownum]], self.trai[self.r_base[self.ft][rownum]]])
        self.MainRegionUpdated()

    def get_single_peak(self,signal_slice):
        trai=signal_slice.idxmax()
        x_peak= self.trai.get_loc(trai)
        y_peak=signal_slice.max()
        return trai,x_peak,y_peak


    def MainRegionUpdated(self):
        """
        Fenster in Peak View bewegt sich gleichzeitig
        """
        self.lr2.setRegion(self.lr.getRegion())
        #self.PeakRegionUpdated()

        # self.unter_index = min(range(len(self.trai)), key=lambda i: abs(self.trai[i] - self.lr2.getRegion()[0]))
        # self.ober_index = min(range(len(self.trai)), key=lambda i: abs(self.trai[i] - self.lr2.getRegion()[1]))
        # #zur Optimierung
        # xu = np.min(self.df[self.ft][self.unter_index:self.ober_index])
        # xo = np.max(self.df[self.ft][self.unter_index:self.ober_index])
        # self.peak_view.setYRange(xu,xo,padding=0.2)
        # self.peak_view.setXRange(self.lr.getRegion()[0], self.lr.getRegion()[1])



    def PeakRegionUpdated(self):
        self.lr.setRegion(self.lr2.getRegion())
        self.unter_index = min(range(len(self.trai)), key=lambda i: abs(self.trai[i] - self.lr2.getRegion()[0]))
        self.ober_index = min(range(len(self.trai)), key=lambda i: abs(self.trai[i] - self.lr2.getRegion()[1]))

        #zur Optimierung
        xu = np.min(self.df[self.ft][self.unter_index:self.ober_index])
        xo = np.max(self.df[self.ft][self.unter_index:self.ober_index])
        self.peak_view.setYRange(xu,xo,padding=0.2)
        self.peak_view.setXRange(self.lr.getRegion()[0], self.lr.getRegion()[1])
        #self.peak_view.setXRange(self.f[unter_index], self.f[ober_index], padding=0.2)

        rownum = self.list_peaks.currentRow()
        self.l_base[self.ft][rownum] = self.unter_index
        self.r_base[self.ft][rownum] = self.ober_index
        self.trai_peaks[self.ft][rownum],self.x_peaks[self.ft][rownum],self.y_peaks[self.ft][rownum]=self.get_single_peak(self.df[self.ft][self.unter_index:self.ober_index])

        actual_x_peak = self.x_peaks[self.ft][rownum]
        self.x_peaks[self.ft].sort()
        position = self.x_peaks[self.ft].index(actual_x_peak)

        # prüfen, ob die Position geändert
        if rownum != position:


            self.l_base[self.ft].insert(position, self.l_base[self.ft].pop(rownum))
            self.r_base[self.ft].insert(position, self.r_base[self.ft].pop(rownum))
            self.trai_peaks[self.ft].insert(position, self.trai_peaks[self.ft].pop(rownum))
            self.x_peaks[self.ft].insert(position, self.x_peaks[self.ft].pop(rownum))
            self.y_peaks[self.ft].insert(position, self.y_peaks[self.ft].pop(rownum))

            self.list_peaks.insertItem(position, self.list_peaks.takeItem(rownum))
            self.list_peaks.setCurrentRow(position)

        self.main_mark.setData(self.trai_peaks[self.ft], self.y_peaks[self.ft])
        try:
            self.list_peaks.item(rownum).setText(f"trai {self.trai_peaks[self.ft][rownum]}" )
        except:
            pass


    def find_peaks_click(self):
        prominence=float(self.txt_prominence.text())
        width=float(self.txt_width.text())
        distance=float(self.txt_distance.text())
        self.find_feature_peaks(self.ft,prominence,width,distance)
        self.switch_feature()

    def add_new(self):
        newrow = self.list_peaks.count()

        self.list_peaks.insertItem(newrow, "Neue...")

        self.x_peaks[self.ft].insert(newrow, 0)
        self.y_peaks[self.ft].insert(newrow, 0)
        self.trai_peaks[self.ft].insert(newrow, 0)
        self.l_base[self.ft].insert(newrow, 0)
        self.r_base[self.ft].insert(newrow, 100)
        self.list_peaks.setCurrentRow(newrow)


    def peak_entfernen(self):
        rownum = self.list_peaks.currentRow()
        self.list_peaks.takeItem(rownum)
        self.x_peaks[self.ft].pop(rownum)
        self.y_peaks[self.ft].pop(rownum)
        self.trai_peaks[self.ft].pop(rownum)
        self.l_base[self.ft].pop(rownum)
        self.r_base[self.ft].pop(rownum)
        self.main_mark.setData(self.trai_peaks[self.ft], self.y_peaks[self.ft])


    def speichern(self):
        pass

    def setupUi(self, FRF_Analyzer):
        FRF_Analyzer.setObjectName("FRF_Analyzer")
        FRF_Analyzer.resize(1074, 680)
        FRF_Analyzer.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(FRF_Analyzer)
        self.centralwidget.setObjectName("centralwidget")
        self.list_peaks = QtWidgets.QListWidget(self.centralwidget)
        self.list_peaks.setGeometry(QtCore.QRect(20, 40, 141, 561))
        self.list_peaks.setObjectName("list_peaks")
        self.main_view = PlotWidget(self.centralwidget)  # QtWidgets.QWidget(self.centralwidget)
        self.main_view.setGeometry(QtCore.QRect(170, 80, 871, 241))
        self.main_view.setObjectName("main_view")
        self.peak_view = PlotWidget(self.centralwidget)
        self.peak_view.setGeometry(QtCore.QRect(170, 360, 400, 241))
        self.peak_view.setObjectName("peak_view")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 60, 111, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 340, 111, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 111, 19))
        self.label_3.setObjectName("label_3")
        self.lbl_features = QtWidgets.QLabel(self.centralwidget)
        self.lbl_features.setGeometry(QtCore.QRect(170, 20, 111, 19))
        self.lbl_features.setObjectName("lbl_features")
        self.lbl_prominence = QtWidgets.QLabel(self.centralwidget)
        self.lbl_prominence.setGeometry(QtCore.QRect(400, 20, 111, 19))
        self.lbl_prominence.setObjectName("lbl_prominence")
        self.txt_prominence = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_prominence.setGeometry(QtCore.QRect(480, 20, 30, 19))
        self.txt_prominence.setObjectName("txt_prominence")
        self.lbl_width = QtWidgets.QLabel(self.centralwidget)
        self.lbl_width.setGeometry(QtCore.QRect(520, 20, 111, 19))
        self.lbl_width.setObjectName("lbl_width")
        self.txt_width = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_width.setGeometry(QtCore.QRect(560, 20, 30, 19))
        self.txt_width.setObjectName("txt_width")
        self.lbl_distance = QtWidgets.QLabel(self.centralwidget)
        self.lbl_distance.setGeometry(QtCore.QRect(600, 20, 111, 19))
        self.lbl_distance.setObjectName("lbl_distance")
        self.txt_distance = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_distance.setGeometry(QtCore.QRect(655, 20, 30, 19))
        self.txt_distance.setObjectName("txt_distance")
        self.btnSave = QtWidgets.QPushButton(self.centralwidget)
        self.btnSave.setGeometry(QtCore.QRect(950, 570, 88, 27))
        self.btnSave.setObjectName("btnSave")
        self.btnloeschen = QtWidgets.QPushButton(self.centralwidget)
        self.btnloeschen.setGeometry(QtCore.QRect(850, 570, 88, 27))
        self.btnloeschen.setObjectName("btnloeschen")
        self.btnnew = QtWidgets.QPushButton(self.centralwidget)
        self.btnnew.setGeometry(QtCore.QRect(750, 570, 88, 27))
        self.btnnew.setObjectName("btnnew")
        self.btnfindpeaks = QtWidgets.QPushButton(self.centralwidget)
        self.btnfindpeaks.setGeometry(QtCore.QRect(650, 570, 88, 27))
        self.btnfindpeaks.setObjectName("btnfindpeaks")
        FRF_Analyzer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FRF_Analyzer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1074, 21))
        self.menubar.setObjectName("menubar")
        FRF_Analyzer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FRF_Analyzer)
        self.statusbar.setObjectName("statusbar")
        FRF_Analyzer.setStatusBar(self.statusbar)
        self.cbo_features = QtWidgets.QComboBox(self.centralwidget)
        self.cbo_features.setGeometry(QtCore.QRect(230, 20, 160, 19))
        self.cbo_features.setObjectName("cbo_features")

        #add features combobox items 
        self.cbo_features.addItems(self.features)

        # add list items
        # self.add_list_items()

        self.switch_feature()



        # fenster verschieben
        self.lr.sigRegionChangeFinished.connect(self.MainRegionUpdated)
        self.lr2.sigRegionChangeFinished.connect(self.PeakRegionUpdated)

        # switch feature 
        self.cbo_features.activated.connect(self.switch_feature)

        # refind peaks
        self.btnfindpeaks.clicked.connect(self.find_peaks_click)

        # peak wählen
        self.list_peaks.currentItemChanged.connect(self.item_change)

        # peak löschen
        self.btnloeschen.clicked.connect(self.peak_entfernen)

        # peak aktualisieren
        self.btnnew.clicked.connect(self.add_new)

        # speichern
        self.btnSave.clicked.connect(self.speichern)

        self.retranslateUi(FRF_Analyzer)
        QtCore.QMetaObject.connectSlotsByName(FRF_Analyzer)

    def retranslateUi(self, FRF_Analyzer):
        _translate = QtCore.QCoreApplication.translate
        FRF_Analyzer.setWindowTitle(_translate("FRF_Analyzer", "FRF Analyzer"))
        self.label.setText(_translate("FRF_Analyzer", "FRF-Übersicht"))
        self.label_2.setText(_translate("FRF_Analyzer", "Peak View"))
        self.label_3.setText(_translate("FRF_Analyzer", "Bänder"))
        self.lbl_features.setText(_translate("FRF_Analyzer", "Features:"))
        self.lbl_prominence.setText(_translate("FRF_Analyzer", "Prominence:"))
        self.lbl_width.setText(_translate("FRF_Analyzer", "Width:"))
        self.lbl_distance.setText(_translate("FRF_Analyzer", "Distance:"))
        self.btnSave.setText(_translate("FRF_Analyzer", "Speichern"))
        self.btnloeschen.setText(_translate("FRF_Analyzer", "Löschen"))
        self.btnnew.setText(_translate("FRF_Analyzer", "Neue Spitze"))
        self.btnfindpeaks.setText(_translate("FRF_Analyzer", "Find Peaks"))
        #self.expand.setText(_translate("FRF_Analyzer", "Bänder vergrößern"))


if __name__ == "__main__":
    # print('Start Application\n')
    from vallendb import FileHandler

    # f = FileHandler("feature_data.pkl", subdir=["data"])
    # df = pd.DataFrame(f.read())

    f = FileHandler("02_Ruhemessung_pp.trfdb", wkd = r"C:\Users\ahofer\Desktop\INTEUM\00_Messungen_03_05_2022\00_Pos1_VS150M")
    with f.current_file() as trfdb:
        df = trfdb.read()

    # remove constants
    # df = df.loc[:, (df != df.iloc[0]).any()]

    # Reset index
    if df.index.name != "trai":
        df.set_index("trai", inplace=True)

    # remove enumerations
    # df2 = df.diff().round(3).iloc[1:-1]
    # df = df.loc[:, (df2 != df2.iloc[1]).any()]

    # min max scale
    #df = (df - df.min()) / (df.max() - df.min())

    app = QtWidgets.QApplication(["test"])
    FRF_Analyzer = QtWidgets.QMainWindow()
    # print('Run GUI\n')
    ui = Ui_FRF_Analyzer(df)
    ui.setupUi(FRF_Analyzer)
    FRF_Analyzer.show()
    sys.exit(app.exec_())
