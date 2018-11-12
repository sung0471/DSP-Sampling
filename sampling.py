import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size':8})

# analog signal x axis
time_of_view        = 1.    # s.
analog_time         = np.linspace (0, time_of_view, 10e5)   # s.
zero_xlim           = 0

def get_signal(signal):
    return amplitude * np.cos(2 * np.pi * signal.frequency * signal.time_point + signal.phase)

def shift_frequency(frequency, sampling_rate,isAliasing):
    if 2 * np.pi * frequency <= np.pi:
        return frequency*sampling_rate,isAliasing
    else:
        isAliasing = 1;
        frequency = frequency - 1
        return shift_frequency(frequency, sampling_rate,isAliasing)

def set_axes(index,signal,phasor,isAliasing,check):
    set_x,set_y=[],[]
    for i in range(index):
        if isAliasing[i]==check:
            phasor[i] = np.real(signal[i].amplitude * np.exp(complex(0, signal[i].phase)) / 2)
            if signal[i].frequency == 0:
                set_x.append(signal[i].frequency)
                set_y.append(phasor[i])
            else:
                set_x.extend([-signal[i].frequency, signal[i].frequency])
                set_y.extend([phasor[i], phasor[i]])
    return set_x,set_y

class signal:
    def __init__(self,signal,frequency=None,amplitude=None,phase=None,time_point=None):
        if signal==None:
            self.frequency=frequency
            self.amplitude=amplitude
            self.phase=phase
            self.time_point=time_point
        else:
            self.frequency = signal.frequency
            self.amplitude = signal.amplitude
            self.phase = signal.phase
            self.time_point = signal.time_point
        self.sinusoid_signal=get_signal(self)

    def set_sinusoid(self):
        self.sinusoid_signal=get_signal(self)

    def __str__(self):
        return("Frequency : "+str(self.frequency)+"Hz\n"+
                "Amplitude : "+str(self.amplitude)+"\n"+
                "Phase : "+str(self.phase)+"radian\n"+
                "time point : "+str(self.time_point))


# iterate as much as input value
while(1):
    # try:
        index=int(input("How many signals ? "))
        sampling_rate = float(input("sampling rate : "))  # Hz

        analog_signal       =[signal]*index
        sum_signal          =0

        sampling_signal     =[signal]*index
        sum_sampling_signal =0

        analog_to_sampling_signal=[signal]*index
        sum_a2s_signal      =0

        recovered_signal            = [signal]*index
        sum_recovered_signal        = 0
        recovered_sampled_signal    = [signal] * index
        sum_recovered_sampled_signal= 0

        isAliasing          =[0]*index
        recovered_frequency =[0]*index
        for i in range(index):
            # global variable

            # analog signal
            carrier_frequency   = float(input(str(i+1)+". analog signal frequency (Hz) : "))
            amplitude           = float(input(str(i+1)+". analog signal amplitude : "))
            phase               = float(input(str(i+1)+". analog signal phase (degree) : "))
            phase               = phase*np.pi/180

            # sampling parameter
            sampling_period     = 1. / (sampling_rate+1) # s
            sample_number       = time_of_view / sampling_period
            analog_to_sampling_time = np.linspace(0,sample_number,10e5)
            sampling_time       = np.linspace (0, sample_number, sample_number+1)
            recovered_to_sampling_time = np.linspace(0,time_of_view,sample_number)

            analog_signal[i]    = signal(None,carrier_frequency,amplitude,phase,analog_time)
            sum_signal+=analog_signal[i].sinusoid_signal
            zero_xlim=max(zero_xlim,np.absolute(analog_signal[i].frequency))

            analog_to_sampling_signal[i]    = signal(None,carrier_frequency/sampling_rate,amplitude,phase,analog_to_sampling_time)
            sum_a2s_signal+=analog_to_sampling_signal[i].sinusoid_signal

            sampling_signal[i]  = signal(None,carrier_frequency/sampling_rate,amplitude,phase,sampling_time)
            sum_sampling_signal+= sampling_signal[i].sinusoid_signal

            recovered_frequency[i],isAliasing[i] = shift_frequency(sampling_signal[i].frequency,sampling_rate,isAliasing[i])
            recovered_signal[i]             = signal(analog_signal[i])
            recovered_signal[i].frequency   = recovered_frequency[i]
            recovered_signal[i].set_sinusoid()
            sum_recovered_signal+=recovered_signal[i].sinusoid_signal

            recovered_sampled_signal[i]             =signal(recovered_signal[i])
            recovered_sampled_signal[i].time_point  =recovered_to_sampling_time
            recovered_sampled_signal[i].set_sinusoid()
            sum_recovered_sampled_signal+=recovered_sampled_signal[i].sinusoid_signal

        zero_y=[]
        zero_x=np.linspace(-zero_xlim*3/2,zero_xlim*3/2,10e5)
        for x in zero_x:
            zero_y.append(0)

        fig = plt.figure ()
        fig1=fig.add_subplot(3,3,1)
        fig1.plot (analog_time, sum_signal)
        fig1.plot (zero_x, zero_y,'k-')
        fig1.set_title("Analog Signal")
        fig1.set_xlim(0,sampling_period*5)
        fig1.set_xlabel("Time")
        fig1.set_ylabel("Amplitude")

        fig2=fig.add_subplot(3,3,2)
        fig2.plot (analog_to_sampling_time, sum_a2s_signal)
        fig2.stem (sampling_time, sum_sampling_signal, linefmt='r-', markerfmt='rs', basefmt='k-')
        fig2.set_title("Sampling Signal")
        fig2.set_xlim(0,5)
        fig2.set_xlabel("Number")

        fig3=fig.add_subplot(3,3,3)
        fig3.plot (analog_time, sum_recovered_signal)
        fig3.stem (recovered_to_sampling_time, sum_recovered_sampled_signal, linefmt='r-', markerfmt='rs', basefmt='k-')
        fig3.set_title("Recovered Signal")
        fig3.set_xlim(0,sampling_period*5)
        fig3.set_xlabel("Time")

        phasor=[0.]*index
        set_x_nonAliasing ,set_y_nonAliasing=[],[]
        set_x_Aliasing, set_y_Aliasing={},{}
        set_x_nonAliasing, set_y_nonAliasing = set_axes(index, analog_signal, phasor, isAliasing,0)
        set_x_Aliasing["analog"], set_y_Aliasing["analog"] = set_axes(index, analog_signal, phasor, isAliasing,1)
        set_x_Aliasing["recover"], set_y_Aliasing["recover"] = set_axes(index, recovered_signal, phasor, isAliasing, 1)

        fig4=fig.add_subplot(3,3,7)
        fig4.bar(set_x_nonAliasing,set_y_nonAliasing,width=2,color='b')
        fig4.bar(set_x_Aliasing["analog"], set_y_Aliasing["analog"], width=2,color='b')
        fig4.plot (zero_x, zero_y,'k-')
        fig4.set_title("Analog Signal")
        get_xlim=np.array(fig4.get_xlim())
        fig4.set_xlabel("Cyclic Frequency")
        fig4.set_ylabel("Phasor")

        set_x_nonAliasing_s = []
        for i in range(len(set_x_nonAliasing)):
            set_x_nonAliasing_s.append(set_x_nonAliasing[i] * 2 * np.pi / sampling_rate)
        set_x_Aliasing_analog2s = []
        set_x_Aliasing_recover2s = []
        for i in range(len(set_x_Aliasing["analog"])):
            set_x_Aliasing_analog2s.append(set_x_Aliasing["analog"][i]*2*np.pi/sampling_rate)
            set_x_Aliasing_recover2s.append(set_x_Aliasing["recover"][i]*2*np.pi/sampling_rate)

        fig5 = fig.add_subplot(3, 3, 8)
        fig5.bar(set_x_nonAliasing_s, set_y_nonAliasing, width=1,color='b')
        fig5.bar(set_x_Aliasing_analog2s,set_y_Aliasing["analog"],width=1,color='b',alpha=0.5)
        fig5.bar(set_x_Aliasing_recover2s,set_y_Aliasing["recover"],width=1,color='r',alpha=0.5)
        fig5.plot(zero_x, zero_y, 'k-')
        fig5.set_title("Check Aliasing")
        fig5.set_xlim(get_xlim*2*np.pi/sampling_rate)
        fig5.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi])
        fig5.set_xticklabels(['-2π','-π','0','π','2π'])
        fig5.set_xlabel("Normalized Radian Frequency")

        fig6=fig.add_subplot(3,3,9)
        fig6.bar(set_x_nonAliasing,set_y_nonAliasing,width=2,color='b')
        fig6.bar(set_x_Aliasing["recover"], set_y_Aliasing["recover"], width=2,color='r')
        fig6.plot(zero_x, zero_y,color='k')
        if len(set_x_Aliasing["analog"])>0:
            fig6.set_title("Aliasing occurred!")
        else:
            fig6.set_title("No Aliasing")
        fig6.set_xlim(get_xlim)
        fig6.set_xlabel("Cyclic Frequency")

        fig.show()
        fig.clear()
        break
    # except ValueError as e:
    #     print("Value error : ",e)