import numpy as np
import matplotlib.pyplot as plt

# analog signal x axis
time_of_view        = 1.    # s.
analog_time         = np.linspace (0, time_of_view, 10e5)   # s.


def get_signal(frequency, time_point):
    return amplitude * np.cos(2 * np.pi * frequency * time_point + phase)

def check_aliasing(frequency, sampling_rate):
    global isAliasing
    if 2 * np.pi * frequency / sampling_rate <= np.pi:
        return frequency
    else:
        isAliasing = 1;
        frequency = np.absolute(frequency - sampling_rate)
        return check_aliasing(frequency, sampling_rate)

# iterate as much as input value
while(1):
    try:
        index=int(input("How many signals ? "))
        sampling_rate = float(input("sampling rate : "))  # Hz
        for i in range(index):
            # global variable
            isAliasing          = 0
            recovered_frequency = 0

            # analog signal
            carrier_frequency   = float(input("analog signal frequency : "))
            amplitude           = float(input("analog signal amplitude : "))
            phase               = float(input("analog signal phase\n"
                                        "ex) input : 3 → output : 3pi\n : "))
            phase               = np.pi*phase

            # sampling parameter
            sampling_period     = 1. / (sampling_rate+1) # s
            sample_number       = time_of_view / sampling_period
            sampling_time       = np.linspace (0, time_of_view, sample_number)

            analog_signal       = get_signal (carrier_frequency, analog_time)
            sampling_signal     = get_signal (carrier_frequency, sampling_time)
            # quantizing_signal   = np.round (sampling_signal / quantizing_step) * quantizing_step
            recovered_frequency = check_aliasing(carrier_frequency,sampling_rate)
            recovered_signal    = get_signal (recovered_frequency, analog_time)

            fig = plt.figure ()
            fig1=fig.add_subplot(3,2,1)
            fig1.plot (analog_time, analog_signal)
            fig1.stem (sampling_time, sampling_signal, linefmt='r-', markerfmt='rs', basefmt='r-')
            fig1.set_title("Analog to digital signal Sampling")
            fig1.set_xlim(0,sampling_period*5)
            fig1.set_xlabel("Time")
            fig1.set_ylabel("Amplitude")

            fig2=fig.add_subplot(3,2,2)
            fig2.plot (analog_time, recovered_signal)
            fig2.stem (sampling_time, sampling_signal, linefmt='r-', markerfmt='rs', basefmt='r-')
            fig2.set_title("digital to Analog Sampled Signal")
            fig2.set_xlim(0,sampling_period*5)
            fig2.set_xlabel("Time")
            fig2.set_ylabel("Amplitude")

            fig1=fig.add_subplot(3,2,5)
            phasor=np.real(amplitude*np.exp(complex(0,phase))/2)
            set_x=np.linspace(-carrier_frequency, carrier_frequency, 2)
            set_y=np.array([phasor,phasor])
            fig1.bar(set_x,set_y,width=1)
            fig1.set_title("Analog Signal Frequency Domain")
            get_xlim=fig1.get_xlim()
            fig1.set_xlabel("Frequency")
            fig1.set_ylabel("Phasor")


            fig2=fig.add_subplot(3,2,6)
            if recovered_frequency==0:
                set_x=recovered_frequency
                set_y=phasor;
            else:
                set_x=np.linspace(-recovered_frequency, recovered_frequency, 2)
                set_y=np.array([phasor,phasor])
            fig2.bar(set_x,set_y,width=1)
            if isAliasing:
                fig2.set_title("Aliasing occurred!")
            else:
                fig2.set_title("No Aliasing")
            fig2.set_xlim(get_xlim)
            fig2.set_xlabel("Frequency")
            fig2.set_ylabel("Phasor")


            fig.show()
            fig.clear()
        break
    except ValueError as e:
        print("Value error : ",e)