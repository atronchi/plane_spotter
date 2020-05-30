import RPi.GPIO as GPIO
import time
from datetime import datetime

Motordir = [
    'forward',
    'backward',
]

class DRV8825():
    def __init__(self, dir_pin, step_pin, enable_pin, mode_pins):
        self.dir_pin = dir_pin
        self.step_pin = step_pin        
        self.enable_pin = enable_pin
        self.mode_pins = mode_pins
        self.min_step_secs = 7.85e-5  # an educated guess
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.mode_pins, GPIO.OUT)
        
    def digital_write(self, pin, value):
        GPIO.output(pin, value)

    def step(self, pin):
        GPIO.output(pin, 1)
        GPIO.output(pin, 0)
        
    def Start(self):
        self.digital_write(self.enable_pin, 0)
    
    def Stop(self):
        self.digital_write(self.enable_pin, 1)
    
    def SetMicroStep(self, mode, steps_per_step):
        """
        (1) mode
            'hardware' :    Use the switch on the module to control the microstep
            'software' :    Use software to control microstep pin levels
                Need to put the All switch to 0
        (2) steps_per_step : [1, 2, 4, 8, 16, 32]
        """
        sps_dict = {
                1: (0, 0, 0),
                2: (1, 0, 0),
                4: (0, 1, 0),
                8: (1, 1, 0),
                16: (0, 0, 1),
                32: (1, 0, 1)}

        print("Control mode: ",mode)
        if mode == 'software':
            print("set pins")
            for pin, value in zip(self.mode_pins, sps_dict[steps_per_step]):
                self.digital_write(pin, value)

    def calibrateStepTiming(self, n=10000, dt=0.01/32):
        self.digital_write(self.enable_pin, 1)  # 1=disable
        self.digital_write(self.dir_pin, 0)  # 0=forward

        tic = datetime.now()
        for i in range(n):
            self.step(self.step_pin)
            time.sleep(dt)
        toc = datetime.now()

        self.min_step_secs = (toc-tic).total_seconds() / n - dt

        print(f"minimum {self.min_step_secs} sec per step")

        
    def TurnStep(self, dir, steps, stepdelay=0.005):
        print(dir)
        if (dir == 'forward'):
            self.digital_write(self.enable_pin, 0)
            self.digital_write(self.dir_pin, 0)
        elif (dir == 'backward'):
            self.digital_write(self.enable_pin, 0)
            self.digital_write(self.dir_pin, 1)
        else:
            print("the dir must be : 'forward' or 'backward'")
            self.digital_write(self.enable_pin, 1)
            return

        if (steps == 0):
            print("no steps left")
            return

        if self.min_step_secs is not None:
            print(f"subtracting {self.min_step_secs} from requested stepdelay {stepdelay}")
            delay = stepdelay - self.min_step_secs
            if delay < 0:
                raise Exception(f"requested delay {stepdelay} is less than min_step_secs={self.min_step_secs}")
            else:
                delay
            
        print(f"turn step: {steps}, step delay {stepdelay}")
        tic = datetime.now()
        for i in range(steps):
            self.step(self.step_pin)
            time.sleep(delay)
        toc = datetime.now()
        print(f"{toc} step {i}, delay {toc-tic}, avg time per step {(toc-tic).total_seconds() / i} seconds", flush=True)
