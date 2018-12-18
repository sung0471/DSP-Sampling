import numpy as np
from sampling_FIR import input_signal, sampling, firFiltering, recovering, printSamplingFig, printFIRFig

if __name__ == '__main__':
    index = int(input("How many signals ? "))

    carrier_frequency = [0.] * index
    amplitude = [0.] * index
    phase = [0.] * index
    isCos = [0] * index

    # input sampling rate
    sampling_rate = float(input("sampling rate : "))  # Hz
    for i in range(index):
        # input analog signal
        while(1):
            checkCos=input(str(i+1)+". Cosine or sin (Cos : 0, Sin : 1) : ")
            if(checkCos=="0" or checkCos=="1"):
                break
            else:
                print("error: MUST INPUT 0 or 1")
        isCos[i]=checkCos
        carrier_frequency[i] = float(input(str(i + 1) + ". analog signal frequency (Hz) : "))
        amplitude[i] = float(input(str(i + 1) + ". analog signal amplitude : "))
        phase[i] = float(input(str(i + 1) + ". analog signal phase (degree) : "))
        phase[i] = phase[i] * np.pi / 180

    # sampling process
    input_signal(index, sampling_rate, isCos, carrier_frequency, amplitude, phase)
    sampling()
    check=1
    if check==0:
        recovering(check)
        printSamplingFig()
    else:
        firFiltering()
        recovering(check)
        printFIRFig()