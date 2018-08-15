import time

class Button:
    def __init__(self, gpio_pin, keyboard_key):
        try:
            import RPi.GPIO as GPIO
            import time
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(
                gpio_pin, 
                GPIO.IN, 
                pull_up_down=GPIO.PUD_UP
            )
            self.use_gpio = True
            self.GPIO = GPIO
        except ImportError:
            self.use_gpio = False
            print("No GPIO library found, " \
                "listening for key '{}' instead".format(keyboard_key)
            )
            import cv2
            self.cv2 = cv2
            self.keyboard_key = keyboard_key

        self.press_start_time = None

    def pressed(self, min_press_time=0, key_state=None):
        if self.use_gpio:
            input_state = not self.GPIO.input(18)
        else:
            if key_state is None:
                raise ValueError("you must provide a key_state to function pressed" \
                        " when in keyboard mode")
            input_state = (key_state & 0xff) == ord(self.keyboard_key)

        if input_state == True:
            self.debounce_counter = 4

        if input_state == True and self.press_start_time is None:
            self.press_start_time = time.time()
        elif input_state == False and self.press_start_time is not None:
            self.debounce_counter -= 1
            if self.debounce_counter == 0:
                self.press_start_time = None

        if self.press_start_time is None:
            return False
        else:
            return (time.time() - self.press_start_time) > min_press_time
