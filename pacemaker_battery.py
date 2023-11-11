import sys
import pacemaker
import os

AVI_length = 0
VAI_length = 0

if len(sys.argv) <= 1:
    print("Assuming that the person is in a neutral state")
else:
    if sys.argv[1] == "rest":
        AVI_length = 100
        VAI_length = 750
    elif sys.argv[1] == "neutral":
        AVI_length = 150
        VAI_length = 850
    elif sys.argv[1] == "working":
        AVI_length = 200
        VAI_length = 950
    else:
        print("Assuming that the person is in a neutral state")
        
exit_status=os.system("python .\gen_cardiac_signal_trace")
if exit_status == 0:
    print("Compilation successful")
else:
    print(f"Compilation failed with exit status {exit_status}")
c = 0
pace_atrium_counter = 0
pace_ventricle_counter = 0
print(f"Initial Battery Capacity: {int(pacemaker.battery_capacity)}")

while c < pacemaker.max_cycles:
    pacemaker.wait_PVARP(pacemaker.fp)  
    # Sense atrium
    atrium_sense_result = pacemaker.sense_atrium(pacemaker.fp)
    if atrium_sense_result == 0:
        pacemaker.pace_atrium()  # Pacing atrium if atrium not sensed
        pace_atrium_counter += 1
    elif atrium_sense_result == 2:
        print("EOF reached.")  # Stop if EOF reached
        c = pacemaker.max_cycles
    # Sense ventricle
    ventricle_sense_result = pacemaker.sense_ventricle(pacemaker.fp)
    if ventricle_sense_result == 0:
        pacemaker.pace_ventricle()  # Pacing ventricle if ventricle not sensed
        pace_ventricle_counter += 1
    elif ventricle_sense_result == 2:
        print("EOF reached.")  # Stop if EOF reached
        c = pacemaker.max_cycles
    if pacemaker.is_change_rate():  # Check rate change
        pacemaker.update_VAI()
    c += 1
    # print(f"Cycle: {c}")

# print(f"Final Battery Capacity: {int(pacemaker.battery_capacity)}")
# print(f"pace_atrium_counter = {pace_atrium_counter}\npace_ventricle_counter = {pace_ventricle_counter}")
# print(f"pa_by_battery = {pacemaker.pa_by_battery}\npv_by_battery = {pacemaker.pv_by_battery}")
with open('output.txt', 'a') as file:
    # Write the values to the file
    file.write(f"{pacemaker.rate_at_which_supercapacitor_is_charged} {pacemaker.pa_by_battery} {pacemaker.pv_by_battery} \n")

# The file is automatically closed when exiting the "with" block

    