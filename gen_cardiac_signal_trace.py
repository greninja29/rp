import random
from pacemaker import *

# max_cycles = 10000
# PVARP_length = 350
# VAI_length = 850
# p_wavelength = 110
# AVI_length = 150

def main():
    with open("cardiac_signal_trace.txt", "w") as fp:
        pace_atrium_counter = 0
        pace_ventricle_counter = 0

        for c in range(max_cycles):
            for pvarp_counter in range(PVARP_length):
                fp.write('-')

            for v in range(PVARP_length, VAI_length - p_wavelength):
                fp.write('-')

            pflag = 0
            for p in range(p_wavelength):
                atrial_signal = random.randint(0, 99)
                if not atrial_signal and not pflag:
                    fp.write('P')
                    pflag = 1
                else:
                    fp.write('-')

            if not pflag:
                pace_atrium_counter += 1

            qflag = 0
            for a in range(AVI_length):
                ventricle_signal = random.randint(0, 99)
                if not ventricle_signal and not qflag:
                    fp.write('Q')
                    qflag = 1
                else:
                    fp.write('-')

            if not qflag:
                pace_ventricle_counter += 1

    print(f"#pace_atrium={pace_atrium_counter}  #pace_ventricle={pace_ventricle_counter}")

if __name__ == "__main__":
    main()
