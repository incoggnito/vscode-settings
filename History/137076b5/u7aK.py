# -*- coding: utf-8 -*-

# import pyqtgraph
# Copyright (c) 2012  University of North Carolina at Chapel Hill 
# Luke Campagnola    ('luke.campagnola@%s.com' % 'gmail') 

# Form implementation generated from reading ui file 'FRF_Analyzer.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from scipy import interpolate #QV
from PySide2 import QtCore, QtWidgets
from pyqtgraph import PlotWidget, LinearRegionItem#, mkPen
import numpy as np
from scipy.signal import find_peaks, peak_widths
import scipy.linalg as la
import pandas as pd
from math import sqrt
import os
from matplotlib.pyplot import savefig, xlabel, ylabel, subplot, grid, plot, ylim, xlim, figure
import sys
import warnings
warnings.filterwarnings("ignore")

#path2local = 'C:/Users/qxo1686/python/__raw__/'
class Ui_FRF_Analyzer(object):

    def __init__(self, df):
        '''
        f: Der Zeilenvektor von Frequenz
        TF: Der Zeilenvektor von komplexen FRF
        abs_TF: Der Zeilenvektor von FRF-Amplitude
        phase: Der Spaltenvecktor von FRF-Phase
        coh: Der Zeilenvektor von Kohärenz
        f_column: Der Spaltenvektor von Frequenz
        TF_column: Der Spaltenvektor von komplexen FRF
        Nur Spaltenvektor kann in Funktion >sdof_cf< eingegeben werden
        '''
        self.feature = df.iloc[:,2]
        self.peaks, properties = find_peaks(self.feature, prominence=1, width=20)

    def get_all_peaks(self):
        '''
        x_peak: Die Liste der Indexe aller Spitzen
        l_base: Die Liste der linken Indexe aller Spitzen, floor
        r_base: Die Liste der rechten Indexe aller Spitzen, ceil

        eigenfrequenz: Die Liste der aufgerundeten Eigenfrequenzen
        amp_peak: Die Liste der Amplituden aller Spitzen
        coh_peak: Die Liste der Kohärenz aller Spitzen
        dampings: Die Liste der Dämpfungen aller Spitzen
        '''

        #find peaks
        self.x_peak, _ = find_peaks(self.abs_TF[self.xu:self.xo_peak], distance=10,
                        height=self.border,prominence=[0.01*np.max(self.abs_TF[self.xu:self.xo_peak]),np.max(self.abs_TF[self.xu:self.xo_peak])] )
        if len(self.x_peak) ==0:
            self.x_peak, _ = find_peaks(self.abs_TF[self.xu:self.xo], distance =10, prominence=[0.005*np.max(self.abs_TF[self.xu:self.xo_peak]),np.max(self.abs_TF[self.xu:self.xo_peak])])
        self.x_peak = self.x_peak +self.xu
        #get left and right bases
        #get l_base and r_base with peak_widths function
        _, _, l_base, r_base = peak_widths(self.abs_TF, self.x_peak)
        self.l_base = (l_base // 1).astype(int)
        self.l_base=self.l_base.tolist() #np.array to list
        self.r_base = (r_base // 1 + 1).astype(int)
        self.r_base = self.r_base.tolist()

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

    def add_list_items(self):
        '''
        Alle Eigenfrequenzen als String in Liste >items< speichen
        Nur String kann in QListWidget >list_peaks< hinzugefügt werden
        '''
        items = [f'{self.eigenfrequenz[i]}Hz-err:{round(self.residuum[i],3)}'
                    for i in range(len(self.eigenfrequenz))]
        self.list_peaks.addItems(items)

    def item_change(self, item):
        '''
        rownum: Nummer der ausgewählten Zeile der Spitze
        Fenster wird zur ausgewählten Spitze verschoben
        '''
        rownum=self.list_peaks.currentRow()
        self.lr.setRegion([self.f[self.l_base[rownum]], self.f[self.r_base[rownum]]])
        self.phase_view.setXRange(self.f[self.l_base[rownum]],self.f[self.r_base[rownum]])
        self.label_8.setText('%.4f' % self.coh_peak[rownum])


    def MainRegionUpdated(self):
        '''
        Fenster in Peak View bewegt sich gleichzeitig
        '''
        self.lr2.setRegion(self.lr.getRegion())
        self.peak_view.setXRange(self.lr.getRegion()[0],self.lr.getRegion()[1])
        self.phase_view.setXRange(self.lr.getRegion()[0],self.lr.getRegion()[1])

        unter_index=min(range(len(self.f)), key=lambda i: abs(self.f[i]-self.lr2.getRegion()[0]))
        ober_index=min(range(len(self.f)), key=lambda i: abs(self.f[i]-self.lr2.getRegion()[1]))

        #zur Optimierung
        xu = np.min(20*np.log10(self.abs_TF[unter_index:ober_index]))
        xo = np.max(20*np.log10(self.abs_TF[unter_index:ober_index]))
        self.peak_view.setYRange(xu,xo,padding=0.2)
        self.peak_view.setXRange(self.f[unter_index], self.f[ober_index], padding=0.2)



    def PeakRegionUpdated(self):
        '''
        Fenster in Main View bewegt sich gleichzeitig

        unter_index: Der Index der linken Frequenz des Fensters
        ober_index: Der Index der rechten Frequenz des Fensters
        z: Die neu berechnete Dämpfung der ausgewählten Spitzen

        Neue unter_index, ober_index und damping werden in den Listen self.r_base/l_base/dampings aktualisiert
        '''
        self.lr3.setRegion(self.lr2.getRegion())


        self.unter_index=min(range(len(self.f)), key=lambda i: abs(self.f[i]-self.lr2.getRegion()[0]))
        self.ober_index=min(range(len(self.f)), key=lambda i: abs(self.f[i]-self.lr2.getRegion()[1]))
        self.z, self.nf, self.err = self.sdof_cf(self.f_column, self.TF_column, self.unter_index, self.ober_index, plot_it=True)
        damping = 100*self.z
        fehler = sqrt(self.err)/self.max_residuum
        self.label_5.setText('%.2f' % damping + '%')
        self.label_10.setText('%.3f' % fehler)

        rownum=self.list_peaks.currentRow()
        self.l_base[rownum] = self.unter_index
        self.r_base[rownum] = self.ober_index
        self.dampings[rownum] = self.z


    def PeakRegionUpdatedFinished(self):
        self.lr.setRegion(self.lr2.getRegion())

        rownum=self.list_peaks.currentRow()
        self.x_peak[rownum] = min(range(len(self.f)), key=lambda i: abs(self.f[i]-self.nf))
        actual_x_peak =  self.x_peak[rownum]
        self.x_peak.sort()
        position = self.x_peak.index(actual_x_peak)

        #prüfen, ob die Position geändert
        if rownum != position:
            self.eigenfrequenz[rownum] = int(self.nf)
            self.eigenfrequenz.insert(position,self.eigenfrequenz.pop(rownum))

            self.amp_peak[rownum]=self.abs_TF[actual_x_peak]
            self.amp_peak.insert(position,self.amp_peak.pop(rownum))

            self.l_base.insert(position,self.l_base.pop(rownum))
            self.r_base.insert(position,self.r_base.pop(rownum))
            self.residuum.insert(position, self.residuum.pop(rownum))

            self.coh_peak[rownum] = self.coh[actual_x_peak]
            self.coh_peak.insert(position, self.coh_peak.pop(rownum))

            self.dampings.insert(position,self.dampings.pop(rownum))

            self.list_peaks.insertItem(position, self.list_peaks.takeItem(rownum))
            self.list_peaks.setCurrentRow(position)
        #Korrigieren, nur wenn der Unterschied zwischen beiden Algorithmus zu groß ist
        else:
        #elif abs(self.eigenfrequenz[rownum] - int(self.nf))>1:
            self.eigenfrequenz[rownum] = int(self.nf)
            self.amp_peak[rownum]=self.abs_TF[actual_x_peak]
            self.coh_peak[rownum] = self.coh[actual_x_peak]

        self.peak_mark.setData(self.eigenfrequenz, 20*np.log10(self.amp_peak))
        self.list_peaks.item(rownum).setText(str(self.eigenfrequenz[rownum])+'Hz-err:'+str(round(sqrt(self.err)/self.max_residuum,3)))


    def peak_search(self):
        newrow = self.list_peaks.count()

        self.list_peaks.insertItem(newrow, 'Neue...')

        self.x_peak.insert(newrow,0)
        self.eigenfrequenz.insert(newrow, 0)
        self.amp_peak.insert(newrow,100)
        self.l_base.insert(newrow,100)
        self.r_base.insert(newrow,500)
        self.coh_peak.insert(newrow,0)
        self.dampings.insert(newrow,0)
        self.residuum.insert(newrow,0)
        self.list_peaks.setCurrentRow(newrow)


    def PhaseRegionUpdated(self):
        self.lr2.setRegion(self.lr3.getRegion())


    def peak_entfernen(self):
        rownum=self.list_peaks.currentRow()
        self.list_peaks.takeItem(rownum)
        self.x_peak.pop(rownum)
        self.eigenfrequenz.pop(rownum)
        self.amp_peak.pop(rownum)
        self.l_base.pop(rownum)
        self.r_base.pop(rownum)
        self.coh_peak.pop(rownum)
        self.dampings.pop(rownum)
        self.peak_mark.setData(self.eigenfrequenz, 20*np.log10(self.amp_peak))


    # def create_txt(self):
    #     txtfile=os.path.join(path2txt, self.ID + ".txt")
    #     x = self.f
    #     y = 20*np.log10(self.abs_TF)
    #     frf= np.hstack([x[:,None], y[:,None]])
    #     df = pd.DataFrame(frf,columns=['Frequenz',self.ID])
    #     df.to_csv(txtfile, index=False, sep='\t', decimal=',',float_format='%.3f')


    def speichern(self):
        try:
            figure(figsize=(6,4))
            subplot(211)
            plot(self.f, self.abs_TF, '-')
            plot(self.eigenfrequenz, self.amp_peak,'x',markersize=7, color='C3')
            xlabel('Frequenz [Hz]')
            ylabel('Amplitude [lin]')
            xlim([0,16000])
            ylim([0,np.max(self.amp_peak)*1.1])
            grid(True)

            subplot(212)
            plot(self.f, 20*np.log10(self.abs_TF), '-')
            plot(self.eigenfrequenz, 20*np.log10(self.amp_peak),'x',markersize=7, color='C3')
            xlabel('Frequenz [Hz]')
            ylabel('Amplitude [dB] (Ref:1/kg)')
            xlim([0,16000])
            grid(True)

            #create txt
            self.create_txt()

            #build figure loseless and vector

            if self.INP == "Wahr":
                self.ID = self.ID + "_INP"

            fig2=path2messdaten+ self.ID + ".png"
            xlsfile=path2dämpfung + self.ID + '.xlsx'
            savefig(fig2)


            self.dampings = [d*100 for d in self.dampings]
            test= np.column_stack((self.eigenfrequenz, self.dampings))
            df = pd.DataFrame(test, columns=['Eigenfrequenz [Hz]','Dämpfung [%]'])
            df.index += 1
            df.to_excel(xlsfile, sheet_name='Tabelle1', index=True, float_format='%.2f')
            
            # if os.path.isfile(os.path.join(path2local, 'FRF.hdf5')):
            #     with h5py.File(os.path.join(path2local, 'FRF.hdf5'), 'a') as f:
    
            #         if 'components' in f:
            #             g = f['components']
            #         else:
            #             g = f.create_group('components')
    
            #         #overwrite
            #         if self.ID in g:
            #             del g[self.ID]
    
            #         h = g.create_group(self.ID)
            #         if type(self.TF[0])==np.float64:
            #             #QV
            #             h.create_dataset('TF', data=self.TF, dtype='float')
            #         else:
            #             h.create_dataset('TF', data=self.TF, dtype='complex')
            #         h.create_dataset('coh', data=self.coh, dtype='float')
            #         h.create_dataset('peaks', data=self.x_peak)
            #         h.create_dataset('ef', data=self.eigenfrequenz)
            #         h.create_dataset('D', data=self.dampings)
            #         h.create_dataset('l_bases', data = self.l_base)
            #         h.create_dataset('r_bases', data = self.r_base)

            # with h5py.File(os.path.join(path2frf, 'FRF.hdf5'), 'a') as f:

            #     if 'components' in f:
            #         g = f['components']
            #     else:
            #         g = f.create_group('components')

            #     #overwrite
            #     if self.ID in g:
            #         del g[self.ID]

            #     h = g.create_group(self.ID)
            #     if type(self.TF[0])==np.float64:
            #         h.create_dataset('TF', data=self.TF, dtype='float')
            #     else:
            #         h.create_dataset('TF', data=self.TF, dtype='complex')
            #     h.create_dataset('coh', data=self.coh, dtype='float')
            #     h.create_dataset('peaks', data=self.x_peak)
            #     h.create_dataset('ef', data=self.eigenfrequenz)
            #     h.create_dataset('D', data=self.dampings)
            #     h.create_dataset('l_bases', data = self.l_base)
            #     h.create_dataset('r_bases', data = self.r_base)

            #remove file from folder if exists
            if hasattr(self, 'file'):
                os.remove(self.file)
                print('File was saved successfully.')
            sys.exit()

        except Exception as e:
            print('File could not be saved! \n', e)
            sys.exit()

    def expand_bands(self):
        self.l_base=(np.array(self.l_base)*0.99).astype(int)
        self.r_base=(np.array(self.r_base)*1.01).astype(int)

        self.l_base=self.l_base.tolist()
        self.r_base=self.r_base.tolist()

        rownum=self.list_peaks.currentRow()
        self.lr.setRegion([self.f[self.l_base[rownum]],self.f[self.r_base[rownum]]])


    # def sdof_cf(self, f, TF, Fmin=None, Fmax=None, plot_it = False):
    #     if type(self.TF[0])!=np.complex128:
    #         #QV
    #         _,_, nf, z = _fit_gaussian.calc_peak(f[:,0],TF[:,0],[Fmin,Fmax]) 
    #         #z = 0 if np.isnan(z) else z
    #         return z, nf, 1
    #     else:
    #         # check fmin fmax existance
    #         if Fmin is None:
    #             inlow = 0
    #         else:
    #             inlow = Fmin
    
    #         if Fmax is None:
    #             inhigh = np.size(f)
    #         else:
    #             inhigh = Fmax
    
    #         if f[inlow] == 0:
    #             inlow = 1
    
    #         f = f[inlow:(inhigh+1), :]
    #         TF = TF[inlow:(inhigh+1), :]
    
    #         R = TF
    #         y = np.amax(np.abs(TF))
    #         cin = np.argmax(np.abs(TF))
    
    #         ll = np.size(f)
    
    #         w = f * 2 * np.pi * 1j
    
    #         w2 = w * 0
    #         R3 = R * 0
    
    #         for i in range(1, ll + 1):
    #             R3[i - 1] = np.conj(R[ll - i])
    #             w2[i - 1] = np.conj(w[ll - i])
    
    #         w = np.vstack((w2, w))
    #         R = np.vstack((R3, R))
    
    #         N = 2
    #         x, y = np.meshgrid(np.arange(0, N + 1), R)
    #         x, w2d = np.meshgrid(np.arange(0, N + 1), w)
    #         c = -1 * w**N * R
    
    #         aa1 = w2d[:, np.arange(0, N)] \
    #             ** x[:, np.arange(0, N)] \
    #             * y[:, np.arange(0, N)]
    #         aa2 = -w2d[:, np.arange(0, N + 1)] \
    #             ** x[:, np.arange(0, N + 1)]
    #         aa = np.hstack((aa1, aa2))
    
    #         aa = np.reshape(aa, [-1, 5])
    
    #         b, residuum, _, _ = la.lstsq(aa, c)
    #         b = b.reshape(-1)
    #         rs = np.roots(np.array([1,b[1],b[0]]))
    #         omega = np.abs(rs[1])
    #         z = -1 * np.real(rs[1]) / np.abs(rs[1])
    #         nf = omega / 2 / np.pi
    
    
    #         XoF1 = np.hstack(([1 / (w - rs[0]), 1 / (w - rs[1])]))
    #         XoF2 = 1 / (w**0)
    #         XoF3 = 1 / w**2
    #         XoF = np.hstack((XoF1, XoF2, XoF3))
    
    #         # check if extra _ needed
    
    #         a, _, _, _ = la.lstsq(XoF, R)
    #         XoF = XoF[np.arange(ll, 2 * ll), :].dot(a)
    
    #         a = np.sqrt(-2 * np.imag(a[0]) * np.imag(rs[0]) -
    #                     2 * np.real(a[0]) * np.real(rs[0]))
    #         Fmin = np.min(f)
    #         Fmax = np.max(f)
    
    #         phase = np.unwrap(np.angle(TF), np.pi, 0) * 180 / np.pi
    #         phase2 = np.unwrap(np.angle(XoF), np.pi, 0) * 180 / np.pi
    #         while phase2[cin] > 50:
    #             phase2 = phase2 - 360
    #         phased = phase2[cin] - phase[cin]
    #         phase = phase + np.round(phased / 360) * 360
    
    
    #         if plot_it == True:
    #             self.peak_XoF.setData(f[:,0], 20 * np.log10(np.abs(XoF[:,0])))
    #             ##print(20 * np.log10(self.abs_TF[min(range(len(self.f)), key=lambda i: abs(self.f[i]-nf))]))
    #             #self.peak_XoF_mark.setData(np.array([nf]), np.array([20 * np.log10(self.abs_TF[min(range(len(self.f)), key=lambda i: abs(self.f[i]-nf))])]))
    
    #         #Weiß nicht warum residuum leeres array sein kann.Aber wenn leer,
    #         #muss ein 0 element manuel zuzufügen, um fehler zu vermeiden
    #         if len(residuum)==0:
    #             residuum = np.array([0])
    #         #
    #         return z, nf, residuum[0]

    def setupUi(self, FRF_Analyzer):
        FRF_Analyzer.setObjectName("FRF_Analyzer")
        FRF_Analyzer.resize(1074, 637)
        FRF_Analyzer.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(FRF_Analyzer)
        self.centralwidget.setObjectName("centralwidget")
        self.list_peaks = QtWidgets.QListWidget(self.centralwidget)
        self.list_peaks.setGeometry(QtCore.QRect(20, 40, 141, 521))
        self.list_peaks.setObjectName("list_peaks")
        self.main_view = PlotWidget(self.centralwidget)#QtWidgets.QWidget(self.centralwidget)
        self.main_view.setGeometry(QtCore.QRect(170, 40, 871, 241))
        self.main_view.setObjectName("main_view")
        self.peak_view = PlotWidget(self.centralwidget)
        self.peak_view.setGeometry(QtCore.QRect(170, 320, 430, 241))
        self.peak_view.setObjectName("peak_view")
        self.phase_view = PlotWidget(self.centralwidget)
        self.phase_view.setGeometry(QtCore.QRect(611, 320, 430, 241))
        self.phase_view.setObjectName("phase_view")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 20, 111, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 290, 111, 19))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 111, 19))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 570, 111, 19))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(100, 570, 111, 19))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(611, 290, 111, 19))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 585, 111, 19))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(100, 585, 111, 19))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 600, 111, 19))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(100, 600, 111, 19))
        self.label_10.setObjectName("label_10")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(950, 570, 88, 27))
        self.pushButton.setObjectName("pushButton")
        self.expand = QtWidgets.QPushButton(self.centralwidget)
        self.expand.setGeometry(QtCore.QRect(635, 570, 105, 27))
        self.expand.setObjectName("expand")
        self.btnloeschen = QtWidgets.QPushButton(self.centralwidget)
        self.btnloeschen.setGeometry(QtCore.QRect(850, 570, 88, 27))
        self.btnloeschen.setObjectName("btnloeschen")
        self.btnnew = QtWidgets.QPushButton(self.centralwidget)
        self.btnnew.setGeometry(QtCore.QRect(750, 570, 88, 27))
        self.btnnew.setObjectName("btnnew")
        FRF_Analyzer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(FRF_Analyzer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1074, 21))
        self.menubar.setObjectName("menubar")
        FRF_Analyzer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(FRF_Analyzer)
        self.statusbar.setObjectName("statusbar")
        FRF_Analyzer.setStatusBar(self.statusbar)

        #add list items
        self.add_list_items()

        #fenster in meinview
        self.lr = LinearRegionItem()
        self.main_view.addItem(self.lr)
        #fenster in peakview
        self.lr2 = LinearRegionItem()
        self.peak_view.addItem(self.lr2)
        #fenster in phaseview
        self.lr3 = LinearRegionItem()
        self.phase_view.addItem(self.lr3)

        #add initial plots
        
        self.main_view.plot(self.f[self.xu:self.xo], 20*np.log10(self.abs_TF[self.xu:self.xo]))
        #peaks mit roten Kreuzungen markiert
        self.peak_mark=self.main_view.plot(self.eigenfrequenz, 20*np.log10(self.amp_peak), pen = None, symbol='x',symbolPen = ('r'))

        self.c2=self.peak_view.plot(self.f[self.xu:self.xo], 20 * np.log10(self.abs_TF[self.xu:self.xo]))
        self.peak_XoF = self.peak_view.plot(pen = ('y'))
        self.peak_XoF_mark = self.peak_view.plot(pen = None, symbol='x',symbolPen = ('r'))
        self.c3 = self.phase_view.plot(self.f, self.phase)
        #self.c4 = self.phase_view.plot(self.f, self.abs_TF)
        self.phase_view.setYRange(-180,180)

        #self.phase_view.plot(self.f,[-90 for i in range(len(self.phase))], pen=mkPen(color = (105,105,105)))


        #fenster verschieben
        self.lr.sigRegionChangeFinished.connect(self.MainRegionUpdated)
        self.lr2.sigRegionChanged.connect(self.PeakRegionUpdated)
        self.lr2.sigRegionChangeFinished.connect(self.PeakRegionUpdatedFinished)
        self.lr3.sigRegionChangeFinished.connect(self.PhaseRegionUpdated)

        #expand peak band
        self.expand.clicked.connect(self.expand_bands)

        #peak wählen
        self.list_peaks.currentItemChanged.connect(self.item_change)

        #peak löschen
        self.btnloeschen.clicked.connect(self.peak_entfernen)

        #peak aktualisieren
        self.btnnew.clicked.connect(self.peak_search)

        #speichern
        self.pushButton.clicked.connect(self.speichern)

        self.retranslateUi(FRF_Analyzer)
        QtCore.QMetaObject.connectSlotsByName(FRF_Analyzer)


    def retranslateUi(self, FRF_Analyzer):
        _translate = QtCore.QCoreApplication.translate
        FRF_Analyzer.setWindowTitle(_translate("FRF_Analyzer", "FRF Analyzer"))
        self.label.setText(_translate("FRF_Analyzer", "FRF-Übersicht"))
        self.label_2.setText(_translate("FRF_Analyzer", "Peak View"))
        self.label_3.setText(_translate("FRF_Analyzer", "Bänder"))
        self.label_4.setText(_translate("FRF_Analyzer", "Dämpfung:"))
        self.label_5.setText(_translate("FRF_Analyzer", "x"))
        self.label_6.setText(_translate("FRF_Analyzer", "Phase View"))
        self.label_7.setText(_translate("FRF_Analyzer", "Kohärenz:"))
        self.label_8.setText(_translate("FRF_Analyzer", "x"))
        self.label_9.setText(_translate("FRF_Analyzer", "Fehler:"))
        self.label_10.setText(_translate("FRF_Analyzer", "x"))
        self.pushButton.setText(_translate("FRF_Analyzer", "Speichern"))
        self.btnloeschen.setText(_translate("FRF_Analyzer", "Löschen"))
        self.btnnew.setText(_translate("FRF_Analyzer", "Neue Spitze"))
        self.expand.setText(_translate("FRF_Analyzer", "Bänder vergrößern"))

if __name__ == '__main__':
    #print('Start Application\n')
    from atoolbox import FileHandler
    f = FileHandler("feature_data.pkl", subdir=["data"])
    df = pd.DataFrame(f.read())

    # remove constants
    df = df.loc[:, (df != df.iloc[0]).any()]

    # logarithmic
    df.set_index("trai",inplace=True) 
    df = np.log10(df)

    # min max scale
    df = (df-df.min())/(df.max()-df.min())

    app = QtWidgets.QApplication()
    FRF_Analyzer = QtWidgets.QMainWindow()
    #print('Run GUI\n')
    ui = Ui_FRF_Analyzer(df)
    ui.setupUi(FRF_Analyzer)
    FRF_Analyzer.show()
    sys.exit(app.exec_())
