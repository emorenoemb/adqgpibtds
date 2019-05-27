import visa
from struct import unpack
import pylab
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import time
import os 

os.chdir('\Users\FisicaMedica')
 

rm = visa.ResourceManager()
rm.list_resources()
rm.list_resources()[0]

scope = rm.open_resource(rm.list_resources()[0])

scope.write('DATA:SOU CH1;:DATA:WIDTH 1;:DATA:ENC RPB;:DATA:START 1;:DATA:STOP 1000;:ACQ:STOPA SEQ')

fopen=open("cesio137_xx1.dat","a")
print time.time()
for i in range(100000):
    while '1' in scope.ask("ACQ:STATE?"):
        time.sleep(0.01)
    scope.write('CURVE?')
    data=scope.read_raw()
    hl=2+int(data[1])
    wave=data[hl:-1]
    fopen.write(wave)
    if i%10000==0:
        print i
        ADC_wave = np.array(unpack('%sB' % len(wave),wave))
        plt.plot(ADC_wave)
    scope.write("ACQ:STATE ON")
print time.time()
fopen.close()