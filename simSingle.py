
import os

for i in range(80000,500000,5000):
    os.environ['ARG_FROM_PARENT'] = str(i)
    command_to_run = 'python pacemaker_batterySingle.py'
    os.system(command_to_run)


