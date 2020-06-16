import gpiod
import time
import requests
from threading import Thread 
import asyncio
from time import sleep
URL = 'http://127.0.0.1:8810' 

class BlinkTask:
    def __init__(self):
        self.running = True
    def terminate(self):
        self.running = False
    def run(self,led):
        self.running = True
        while(self.running):
            led.set_value(1)
            sleep(0.5)
            led.set_value(0)
            sleep(0.5)

class MonitorTask:
    def __init__(self):
        self.running = True

    def terminate(self):
        self.running = False

    def run(self, button, name):
        self.running = True
        while True:
            ev_line = button.event_wait(sec=2)
            if ev_line:
                event = button.event_read()
                if event.type == gpiod.LineEvent.RISING_EDGE:
                    print("Clicked "+name+" on GPIO")
                    try:
                        # clear event queue
                        requests.post(url=URL + '/'+name+'/')
                        while button.event_wait(sec=1):
                            button.event_read()    
                    except:
                        pass


class GpioHandler:
    blinker = BlinkTask()
    prevTask = MonitorTask()
    nextTask = MonitorTask()
    stopTask = MonitorTask()
    volUpTask = MonitorTask()
    volDownTask = MonitorTask()
    is_blinking = False

    def __init__(self):
        self.chip = gpiod.Chip('10008000.gpio')
        # configure necessary lines
        self.led = self.chip.get_line(24)
        self.led.request(consumer="Blink",type=gpiod.LINE_REQ_DIR_OUT)

        self.prev_button = self.chip.get_line(12)
        self.prev_button.request(consumer="Prev",type=gpiod.LINE_REQ_EV_BOTH_EDGES)

        self.stop_button = self.chip.get_line(13)
        self.stop_button.request(consumer="Stop",type=gpiod.LINE_REQ_EV_BOTH_EDGES)

        self.next_button = self.chip.get_line(14)
        self.next_button.request(consumer="Next",type=gpiod.LINE_REQ_EV_BOTH_EDGES)

        self.vol_up_button = self.chip.get_line(22)
        self.vol_up_button.request(consumer="Stop",type=gpiod.LINE_REQ_EV_BOTH_EDGES)

        self.vol_down_button = self.chip.get_line(23)
        self.vol_down_button.request(consumer="Next",type=gpiod.LINE_REQ_EV_BOTH_EDGES)

    def start_blink(self):
        if not self.is_blinking:
            t = Thread(target=self.blinker.run,args=(self.led,))
            t.start()
            self.is_blinking = True

    def stop_blink(self):
        self.blinker.terminate()
        self.is_blinking = False

    def start_monitors(self):
        
        t1 = Thread(target=self.prevTask.run,args=(self.prev_button,'prev'))
        t1.start()
        
        t2 = Thread(target=self.nextTask.run,args=(self.next_button,'next'))
        t2.start()
        
        t3 = Thread(target=self.stopTask.run,args=(self.stop_button,'stop'))
        t3.start()

        t4 = Thread(target=self.volUpTask.run,args=(self.vol_up_button,'soundUp'))
        t4.start()

        t5 = Thread(target=self.volDownTask.run,args=(self.vol_down_button,'soundDown'))
        t5.start()
    
    def stop_monitors(self):
        self.prevTask.terminate()
        self.nextTask.terminate()
        self.stopTask.terminate()
        
