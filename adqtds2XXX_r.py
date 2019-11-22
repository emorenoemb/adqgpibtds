#!/usr/bin/env python
import ROOT
import pyvisa
from struct import unpack
import numpy as np
import scipy
import matplotlib.pyplot as plt
import time
import os
from IPython.display import display, clear_output
os.chdir('/Users/emoreno/workpython/jupyter/cosmic')
#comunicación con el osciloscopio
rm = pyvisa.ResourceManager()
rm.list_resources()
rm.list_resources()[0]
scope = rm.open_resource(rm.list_resources()[0]);
#parametros de adquisicion del osciloscopio
scope.write('DATA:SOU CH1;:DATA:WIDTH 1;:DATA:ENC RPB;:DATA:START 1;:DATA:STOP 500;:ACQ:STOPA SEQ');
#Declaracion de los objetos de root
nt = ROOT.TNtuple("ntuple","data","amplitud:min:charge")
c = ROOT.TCanvas("myCanvasName","The Canvas Title",800,600)
#ciclo de adquisicion
fig,ax = plt.subplots(1,1)
ax = fig.add_subplot(111)
fopen=open("patron.txt","a")
ndatos=1000000
for i in range(ndatos):
    while '1' in scope.ask("ACQ:STATE?"):
        time.sleep(0.001)
    scope.write('CURVE?')
    data=scope.read_raw()
    hl=2+int(data[1])
    wave=data[hl:-1]
    fopen.write(wave)
    adc=np.array(unpack('%sB'%len(wave),wave))
    signal=(sum(adc[:100])/100-adc)*(5.0/256)
    ma=max(signal)
    mi=min(signal)
    qs=np.trapz(adc[150:300])
    nt.Fill(ma,mi,qs)
    if i%int(ndatos*.1)==0:
        if True: 
            plt.clf()
            #print i;
            # adc=np.array(unpack('%sB'%len(wave),wave))
            #plt.plot(adc)
            #signal=(sum(adc[:100])/100-adc)*(5.0/256)
            plt.text(250,0.8,r'signal number: '+str(i), color='red', fontsize=15)
            plt.plot(signal)
            display(fig)
            clear_output(wait=True)
            #fig.canvas.draw()
    scope.write("ACQ:STATE ON")
fopen.close()
#uso de la herramientas de root
nt.Draw("charge>>hq")
c.Draw("charge")
