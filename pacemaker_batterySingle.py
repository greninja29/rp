import sys
import pacemakerSingle
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
        
# exit_status=os.system("python .\gen_cardiac_signal_trace")
# if exit_status == 0:
#     print("cardiac_signal_trace generation successful")
# else:
#     print(f"cardiac_signal_trace generation failed \nCompilation failed with exit status {exit_status}")
c = 0
pace_atrium_counter = 0
pace_ventricle_counter = 0
print(f"Initial Battery Capacity: {int(pacemakerSingle.battery_capacity)}")

while c < pacemakerSingle.max_cycles:
    pacemakerSingle.wait_PVARP(pacemakerSingle.fp)  
    # Sense atrium
    atrium_sense_result = pacemakerSingle.sense_atrium(pacemakerSingle.fp)
    if atrium_sense_result == 0:
        pacemakerSingle.pace_atrium()  # Pacing atrium if atrium not sensed
        pace_atrium_counter += 1
    elif atrium_sense_result == 2:
        print("EOF reached.")  # Stop if EOF reached
        c = pacemakerSingle.max_cycles
    # Sense ventricle
    ventricle_sense_result = pacemakerSingle.sense_ventricle(pacemakerSingle.fp)
    if ventricle_sense_result == 0:
        pacemakerSingle.pace_ventricle()  # Pacing ventricle if ventricle not sensed
        pace_ventricle_counter += 1
    elif ventricle_sense_result == 2:
        print("EOF reached.")  # Stop if EOF reached
        c = pacemakerSingle.max_cycles
    if pacemakerSingle.is_change_rate():  # Check rate change
        pacemakerSingle.update_VAI()
    c += 1
    # print(f"Cycle: {c}")

print(f"Final Battery Capacity: {int(pacemakerSingle.battery_capacity)}")
# print(f"pace_atrium_counter = {pace_atrium_counter}\npace_ventricle_counter = {pace_ventricle_counter}")
# print(f"pa_by_battery = {pacemaker.pa_by_battery}\npv_by_battery = {pacemaker.pv_by_battery}")
with open('outputSingle.txt', 'a') as file:
    # Write the values to the file
    file.write(f"{pacemakerSingle.rate_at_which_supercapacitor_is_charged} {pacemakerSingle.pa_by_battery} {pacemakerSingle.pv_by_battery} \n")

# The file is automatically closed when exiting the "with" block

    