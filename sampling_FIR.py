import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 8})

# analog signal x axis
time_of_view = 1.  # s.
analog_time = np.linspace(0, time_of_view, 10e5)  # s.
analog_min_freq = 10e10
sample_number_per_period = 0.
zero_xlim = 0

# sampling paramete
sampling_rate = 0
sampling_period = 0.  # s
sample_number = 0

# time domain & version variable
analog_to_sampling_time = []
sampling_time = []
recovered_to_sampling_time = []
version=0

# signal Class object variables
analog_signal = []
sum_analog_signal = 0
sampling_signal = []
sum_sampling_signal = 0

a2s_signal = []
sum_a2s_signal = 0

recovered_signal = []
sum_recovered_signal = 0
recovered_sampled_signal = []
sum_recovered_sampled_signal = 0

isAliasing = []
recovered_frequency = []

# filtering parameter
filter={}
filter["Magnitude"]=[]
filter["Phase"]=0.

# fir signal
fir_Signal = []
sum_fir_Signal=0
fir_sampling_Signal = []
sum_fir_sampling_Signal=0

# graph x, y axis values
set_x_nonAliasing, set_y_nonAliasing = [], []
set_x_Aliasing, set_y_Aliasing = {}, {}

def get_signal(signal):
    if signal.isCos=="0":
        return signal.amplitude * np.cos(2 * np.pi * signal.frequency * signal.time_point + signal.phase)
    else:
        return signal.amplitude * np.sin(2 * np.pi * signal.frequency * signal.time_point + signal.phase)

def shift_frequency(frequency, sampling_rate, isAliasing):
    if 2 * np.pi * frequency <= np.pi:
        return frequency, isAliasing
    else:
        isAliasing = 1;
        frequency = frequency - 1
        return shift_frequency(frequency, sampling_rate, isAliasing)

class signal:
    def __init__(self, signal, isCos=None, frequency=None, amplitude=None, phase=None, time_point=None):
        if signal == None:
            self.isCos=isCos
            self.frequency = frequency
            self.amplitude = amplitude
            self.phase = phase
            self.time_point = time_point
        else:
            self.isCos=signal.isCos
            self.frequency = signal.frequency
            self.amplitude = signal.amplitude
            self.phase = signal.phase
            self.time_point = signal.time_point
        self.sinusoid_signal = get_signal(self)

    def set_sinusoid(self):
        self.sinusoid_signal = get_signal(self)

    def __str__(self):
        sinusoid_type="";
        if self.isCos=="0":
            sinusoid_type="Cos"
        else:
            sinusoid_type="Sin"
        return (
                "Sinusoid type : " + str(sinusoid_type) + "\n" +
                "Frequency : " + str(self.frequency) + "Hz\n" +
                "Amplitude : " + str(self.amplitude) + "\n" +
                "Phase : " + str(self.phase) + "radian\n" +
                "time point : " + str(self.time_point))

def set_parameter(index,get_sampling_rate):
    # global
    global analog_signal, sum_analog_signal, sampling_signal, sum_sampling_signal, a2s_signal, sum_a2s_signal, \
        fir_Signal, sum_fir_Signal,fir_sampling_Signal, sum_fir_sampling_Signal,\
        recovered_signal, sum_recovered_signal, recovered_sampled_signal, sum_recovered_sampled_signal, \
        isAliasing, recovered_frequency

    # all parameter initiation
    analog_signal = [signal] * index
    sum_analog_signal = 0
    sampling_signal = [signal] * index
    sum_sampling_signal = 0

    a2s_signal = [signal] * index
    sum_a2s_signal = 0

    recovered_signal = [signal] * index
    sum_recovered_signal = 0
    recovered_sampled_signal = [signal] * index
    sum_recovered_sampled_signal = 0

    isAliasing = [0] * index
    recovered_frequency = [0] * index

    fir_Signal = [signal]*index
    sum_fir_Signal=0
    fir_sampling_Signal = [signal]*index
    sum_fir_sampling_Signal=0

    global sampling_rate, sampling_period, sample_number, analog_to_sampling_time, sampling_time, recovered_to_sampling_time

    # sampling parameter
    sampling_rate=get_sampling_rate
    sampling_period = 1. / (sampling_rate)  # s
    sample_number = time_of_view / sampling_period
    analog_to_sampling_time = np.linspace(0, sample_number, 10e5)
    sampling_time = np.linspace(0, sample_number, sample_number + 1)
    recovered_to_sampling_time = np.linspace(0, time_of_view, sample_number + 1)

def input_signal(index, sampling_rate, isCos, carrier_frequency, amplitude, phase):
    set_parameter(index,sampling_rate)

    global analog_min_freq, sample_number_per_period

    for i in range(index):
        analog_signal[i] = signal(None, isCos[i], carrier_frequency[i], amplitude[i], phase[i], analog_time)
        if analog_min_freq>carrier_frequency[i]:
            analog_min_freq=carrier_frequency[i]
    sample_number_per_period=sampling_rate/analog_min_freq

def set_axes(index, signal, isAliasing, check):
    set_x, set_y = [], []
    phasor = [0.] * index
    for i in range(index):
        if isAliasing[i] == check:
            phasor[i] = np.real(signal[i].amplitude * np.exp(complex(0, signal[i].phase)) / 2)
            if signal[i].frequency == 0:
                set_x.append(signal[i].frequency)
                set_y.append(phasor[i])
            else:
                set_x.extend([-signal[i].frequency, signal[i].frequency])
                set_y.extend([phasor[i], phasor[i]])
    return set_x, set_y

def sampling():
    # global variable
    global analog_signal, sum_analog_signal, sampling_signal, sum_sampling_signal,\
        a2s_signal, sum_a2s_signal, zero_xlim

    index=len(analog_signal)
    for i in range(index):
        sum_analog_signal += analog_signal[i].sinusoid_signal
        zero_xlim = max(zero_xlim, np.absolute(analog_signal[i].frequency))

        # analog_to_sampling_signal (x: time, y: amplitude)
        a2s_signal[i] = signal(analog_signal[i])
        a2s_signal[i].frequency = analog_signal[i].frequency / sampling_rate
        a2s_signal[i].time_point=analog_to_sampling_time
        a2s_signal[i].set_sinusoid()
        sum_a2s_signal += a2s_signal[i].sinusoid_signal

        # sampling_signal (x: sampling number, y: amplitude)
        sampling_signal[i] = signal(a2s_signal[i])
        sampling_signal[i].time_point=sampling_time
        sampling_signal[i].set_sinusoid()
        sum_sampling_signal += sampling_signal[i].sinusoid_signal

    global set_x_Aliasing,set_y_Aliasing,set_x_nonAliasing,set_y_nonAliasing

    set_x_nonAliasing, set_y_nonAliasing = set_axes(index, analog_signal, isAliasing, 0)
    set_x_Aliasing["analog"], set_y_Aliasing["analog"] = set_axes(index, analog_signal, isAliasing, 1)

def getFilterAmplitude(sampling_freq):
    return 1/5*(2*np.cos(2*sampling_freq)+2*np.cos(sampling_freq)+1)

def getFilterPhase(sampling_freq):
    quotient = int(-2*sampling_freq / (2*np.pi))
    phase=-2*sampling_freq-quotient*2*np.pi
    return phase


def firFiltering():
    global fir_Signal, sum_fir_Signal, fir_sampling_Signal, sum_fir_sampling_Signal

    index=len(analog_signal)
    firAmpli=[0.]*index
    firPhase=[0.]*index

    for i in range(index):
        firAmpli[i]=getFilterAmplitude(a2s_signal[i].frequency*2*np.pi)
        firPhase[i]=getFilterPhase(a2s_signal[i].frequency*2*np.pi)

        fir_Signal[i]=signal(a2s_signal[i])
        fir_Signal[i].amplitude*=firAmpli[i]
        fir_Signal[i].phase+=firPhase[i]
        fir_Signal[i].set_sinusoid()
        sum_fir_Signal+=fir_Signal[i].sinusoid_signal

        fir_sampling_Signal[i]=signal(fir_Signal[i])
        fir_sampling_Signal[i].time_point = sampling_time
        fir_sampling_Signal[i].set_sinusoid()
        sum_fir_sampling_Signal+=fir_sampling_Signal[i].sinusoid_signal

def recovering(check):
    global recovered_signal, sum_recovered_signal, recovered_sampled_signal, sum_recovered_sampled_signal, \
    isAliasing, recovered_frequency

    index = len(analog_signal)

    signal_list=[signal]*index
    for i in range(index):
        if check==0:
            signal_list[i]=signal(a2s_signal[i])
        else:
            signal_list[i]=signal(fir_Signal[i])

    for i in range(index):
        recovered_frequency[i], isAliasing[i] = shift_frequency(signal_list[i].frequency,
                                                                sampling_rate, isAliasing[i])
        recovered_signal[i] = signal(signal_list[i])
        recovered_signal[i].frequency = recovered_frequency[i]*sampling_rate
        recovered_signal[i].time_point = analog_time
        recovered_signal[i].set_sinusoid()
        sum_recovered_signal += recovered_signal[i].sinusoid_signal

        recovered_sampled_signal[i] = signal(recovered_signal[i])
        recovered_sampled_signal[i].time_point = recovered_to_sampling_time
        recovered_sampled_signal[i].set_sinusoid()
        sum_recovered_sampled_signal += recovered_sampled_signal[i].sinusoid_signal

    global set_x_Aliasing, set_y_Aliasing

    set_x_Aliasing["recover"], set_y_Aliasing["recover"] = set_axes(index, recovered_signal, isAliasing, 1)

def printSamplingFig():
    # zero_x, y setting
    zero_x, zero_y = [], []
    zero_x = np.linspace(-zero_xlim * 3 / 2, zero_xlim * 3 / 2, 10e5)
    for x in zero_x:
        zero_y.append(0)

    fig = plt.figure()

    fig1 = fig.add_subplot(3, 3, 1)
    fig1.plot(analog_time, sum_analog_signal)
    fig1.plot(zero_x, zero_y, 'k-')
    fig1.set_title("Analog Signal")
    fig1.set_xlim(0, 1/analog_min_freq * 3)
    fig1.set_xlabel("Time")
    fig1.set_ylabel("Amplitude")

    fig2 = fig.add_subplot(3, 3, 2)
    fig2.plot(analog_to_sampling_time, sum_a2s_signal)
    fig2.stem(sampling_time, sum_sampling_signal, linefmt='r-', markerfmt='rs', basefmt='k-')
    fig2.set_title("Sampling Signal")
    fig2.set_xlim(0, sample_number_per_period*3)
    fig2.set_xlabel("Number")

    fig3 = fig.add_subplot(3, 3, 3)
    fig3.plot(analog_time, sum_recovered_signal)
    fig3.stem(recovered_to_sampling_time, sum_recovered_sampled_signal, linefmt='r-', markerfmt='rs', basefmt='k-')
    fig3.set_title("Recovered Signal")
    fig3.set_xlim(0, 1/analog_min_freq * 3)
    fig3.set_xlabel("Time")

    fig4 = fig.add_subplot(3, 3, 7)
    fig4.bar(set_x_nonAliasing, set_y_nonAliasing, width=2, color='b')
    fig4.bar(set_x_Aliasing["analog"], set_y_Aliasing["analog"], width=2, color='b')
    fig4.plot(zero_x, zero_y, 'k-')
    fig4.set_title("Analog Signal")
    get_xlim = np.array(fig4.get_xlim())
    fig4.set_xlabel("Cyclic Frequency")
    fig4.set_ylabel("Phasor")

    set_x_nonAliasing_s = []
    for i in range(len(set_x_nonAliasing)):
        set_x_nonAliasing_s.append(set_x_nonAliasing[i] * 2 * np.pi / sampling_rate)
    set_x_Aliasing_analog2s = []
    set_x_Aliasing_recover2s = []
    for i in range(len(set_x_Aliasing["analog"])):
        set_x_Aliasing_analog2s.append(set_x_Aliasing["analog"][i] * 2 * np.pi / sampling_rate)
        set_x_Aliasing_recover2s.append(set_x_Aliasing["recover"][i] * 2 * np.pi / sampling_rate)

    fig5 = fig.add_subplot(3, 3, 8)
    fig5.bar(set_x_nonAliasing_s, set_y_nonAliasing, width=0.5, color='b')
    fig5.bar(set_x_Aliasing_analog2s, set_y_Aliasing["analog"], width=0.5, color='b', alpha=0.4)
    fig5.bar(set_x_Aliasing_recover2s, set_y_Aliasing["recover"], width=0.5, color='r', alpha=0.4)
    fig5.plot(zero_x, zero_y, 'k-')
    fig5.set_title("Check Aliasing")
    fig5.set_xlim(get_xlim * 2 * np.pi / sampling_rate)
    fig5.set_xticks([-2 * np.pi, -np.pi, 0, np.pi, 2 * np.pi])
    fig5.set_xticklabels(['-2π', '-π', '0', 'π', '2π'])
    fig5.set_xlabel("Normalized Radian Frequency")

    fig6 = fig.add_subplot(3, 3, 9)
    fig6.bar(set_x_nonAliasing, set_y_nonAliasing, width=2, color='b')
    fig6.bar(set_x_Aliasing["recover"], set_y_Aliasing["recover"], width=2, color='r')
    fig6.plot(zero_x, zero_y, color='k')
    if len(set_x_Aliasing["analog"]) > 0:
        fig6.set_title("Aliasing occurred!")
    else:
        fig6.set_title("No Aliasing")
    fig6.set_xlim(get_xlim)
    fig6.set_xlabel("Cyclic Frequency")

    fig.show()

    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(basedir+'/templates/figures/result'+str(version)+'.svg')

def printFIRFig():
    # zero_x, y setting
    zero_x, zero_y = [], []
    zero_x = np.linspace(-zero_xlim * 3 / 2, zero_xlim * 3 / 2, 10e5)
    for x in zero_x:
        zero_y.append(0)

    fig = plt.figure()


    fig1 = fig.add_subplot(2, 3, 1)
    fig1.plot(analog_to_sampling_time, sum_a2s_signal)
    fig1.stem(sampling_time, sum_sampling_signal, linefmt='r-', markerfmt='rs', basefmt='k-')
    fig1.set_title("Input Signal")
    fig1.set_xlim(0, sample_number_per_period*3)
    fig1.set_xlabel("Number")

    fig3 = fig.add_subplot(2, 3, 3)
    fig3.plot(analog_time, sum_recovered_signal)
    fig3.stem(recovered_to_sampling_time, sum_recovered_sampled_signal, linefmt='r-', markerfmt='rs', basefmt='k-')
    fig3.set_title("Recovered Signal")
    fig3.set_xlim(0, 1 / analog_min_freq * 3)
    fig3.set_xlabel("Time")

    set_x_magnitude = np.linspace(-6,6,10e5)
    set_y_magnitude = np.absolute(getFilterAmplitude(set_x_magnitude))
    set_x_phase = np.linspace(-6,6,10e5)
    set_y_phase=[]
    for x in set_x_phase:
        set_y_phase.append(getFilterPhase(x))

    fig2 = fig.add_subplot(2, 3, 2)
    fig2.plot(set_x_magnitude,set_y_magnitude)
    fig2.set_title("Magnitude of the Filter")

    fig6 = fig.add_subplot(2, 3, 5)
    fig6.plot(set_x_phase,set_y_phase)
    fig6.set_title("Phase of the Filter")
    fig6.set_xlabel("Sampling frequency")

    fig.show()

    import os
    basedir = os.path.abspath(os.path.dirname(__file__))
    fig.savefig(basedir+'/templates/figures/result'+str(version)+'.svg')

if __name__ == '__main__':
    pass