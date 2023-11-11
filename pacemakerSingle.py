import sys
import os
cpu_clk_freq = 1.5e7  # cycles per second
p_wavelength = 110  # 110 msec, atrium sensing duration
pulse_duration = 1   # 1 msec, pacing signal duration
qrs_complex = 100   # 100 msec, ventricle sensing duration
AVI_length = 150   # 150 msec, time for ventricle fill after atrial contraction
PVARP_length = 350  # 350 msec, ignoring false atrium activity
VAI_length = 850  # 850 msec, time between ventricle activity followed by atrial sense
MSI = 500  # 500 msec, time between atrial events to switch mode
LRI = 1000  # 1000 msec, longest interval between two ventricular events
max_cycles = 10000

# SOHAN
current_for_sensing_atrium = 22.3  # 22.3 mA of current is required to sense atrium
current_for_sensing_ventrium = 82.5  # 82.5 mA of current is required to sense ventrium
current_to_pace_atrium = 64.0  # 64.0 mA of current is required to pace atrium
current_to_pace_ventrium = 112.8  # 112.8 mA of current is required to pace ventrium
battery_capacity = int(5.4e16)  # Battery capacity = 1500 mAh = 5.4e+16 charge units
mAh_to_coulomb = 3.6  # 1 mAh = 3.6 coulombs
coulomb_to_charge_units = int(10.0e12)  # 1 Coulomb = 10.0E+12 charge units
mAh_to_charge_units = 3.6 * (10.0e12)  # 1 mAh = 3.6*(10*(10^13)) charge units
present_charge_in_supercapacitor = 0  # Present charge in Supercapacitor in terms of Charge units
max_charge_in_supercapacitor = 500 * (10.0e12) * (1e-6)  # Maximum Charge that Supercapacitor can hold (Assumed Value)
rate_at_which_supercapacitor_is_charged = 500000  # Supercapacitor charging rate (Assumed Value)
# rate_at_which_supercapacitor_is_charged = int(os.environ['ARG_FROM_PARENT'])  # Supercapacitor charging rate (Assumed Value)
pa_by_battery = 0  # Counter to hold the number of times supercapacitor is not available to pace atrium
pv_by_battery = 0  # Counter to hold the number of times supercapacitor is not available to pace ventrium
# SOHAN

fp = open("cardiac_signal_trace.txt", "r")
# multi

# capacitors = [0, 0, 0, 0, 0, 0, 0, 0]

def sense_atrium(fp):
    signal = 0
    global battery_capacity, present_charge_in_supercapacitor
    
    for i in range(int(PVARP_length), int(VAI_length)):

        charge_sc = min(rate_at_which_supercapacitor_is_charged, max_charge_in_supercapacitor - present_charge_in_supercapacitor)
        battery_capacity -= charge_sc
        present_charge_in_supercapacitor += charge_sc  
        battery_capacity -= current_for_sensing_atrium * coulomb_to_charge_units * 1e-6
        c = fp.read(1)
        if c == 'P':
            signal = 1
        elif c == '':
            signal = 2
    return signal

def pace_atrium():
    global present_charge_in_supercapacitor, battery_capacity, pa_by_battery

    if present_charge_in_supercapacitor >= current_to_pace_atrium * pulse_duration * coulomb_to_charge_units * 1e-6:
       present_charge_in_supercapacitor -= current_to_pace_atrium * pulse_duration * coulomb_to_charge_units * 1e-6

    else:
        pa_by_battery += 1
        battery_capacity -= current_to_pace_atrium * pulse_duration * coulomb_to_charge_units * 1e-6

def sense_ventricle(fp):
    signal = 0
    global battery_capacity, present_charge_in_supercapacitor
    for i in range(int(AVI_length)):

        charge_sc = min(rate_at_which_supercapacitor_is_charged, max_charge_in_supercapacitor - present_charge_in_supercapacitor)
        battery_capacity -= charge_sc
        present_charge_in_supercapacitor += charge_sc        
        battery_capacity -= current_for_sensing_ventrium * coulomb_to_charge_units * 1e-6
        c = fp.read(1)
        if c == 'Q':
            signal = 1
        elif c == '':
            signal = 2

    return signal

def pace_ventricle():
    global present_charge_in_supercapacitor, battery_capacity, pv_by_battery

    if present_charge_in_supercapacitor >= current_to_pace_ventrium * pulse_duration * coulomb_to_charge_units * 1e-6:
        present_charge_in_supercapacitor -= current_to_pace_ventrium * pulse_duration * coulomb_to_charge_units * 1e-6
    else:
        pv_by_battery += 1
        battery_capacity -= current_to_pace_ventrium * pulse_duration * coulomb_to_charge_units * 1e-6
 
def wait_PVARP(fp):
    global battery_capacity, present_charge_in_supercapacitor
    for i in range(int(PVARP_length)):     
        charge_sc = min(rate_at_which_supercapacitor_is_charged, max_charge_in_supercapacitor - present_charge_in_supercapacitor)
        battery_capacity -= charge_sc
        present_charge_in_supercapacitor += charge_sc
        fp.read(1)    
         


def is_change_rate():
    pass


def update_VAI():
    pass


