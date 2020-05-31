#!/home/pi/plane_spotter/ve37/bin/python
import RPi.GPIO as GPIO
import time
import traceback
from DRV8825 import DRV8825


try:
    Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
    Motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
    
    Motor1.Stop()
    Motor2.Stop()

    """
    # 1.8 degree: nema23, nema14
    # hardware Control :
    # 'fullstep': A cycle = 200 steps
    # 'halfstep': A cycle = 200 * 2 steps
    # '1/4step': A cycle = 200 * 4 steps
    # '1/8step': A cycle = 200 * 8 steps
    # '1/16step': A cycle = 200 * 16 steps
    # '1/32step': A cycle = 200 * 32 steps
    """
    #Motor1.SetMicroStep('hardware', 'fullstep')

    time_per_full_step = 0.001/8
    nsps = 1
    stepdelay = time_per_full_step / nsps
    steps = 16 * 2048 * nsps

    Motor1.SetMicroStep('software', nsps)
    #Motor1.calibrateStepTiming()
    Motor1.TurnStep(dir='forward', steps=steps, stepdelay=stepdelay)
    Motor1.TurnStep(dir='backward', steps=steps, stepdelay=stepdelay)
    Motor1.Stop()
    
    Motor2.SetMicroStep('software', nsps)
    #Motor2.calibrateStepTiming()
    Motor2.TurnStep(dir='forward', steps=steps, stepdelay=stepdelay)
    Motor2.TurnStep(dir='backward', steps=steps, stepdelay=stepdelay)
    Motor2.Stop()
    
except:
    # GPIO.cleanup()
    Motor1.Stop()
    Motor2.Stop()
    print("Caught exception, stopped motor.")

    raise
