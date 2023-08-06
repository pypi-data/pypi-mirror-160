from time import sleep

from neopixel import Neopixel


class LEDRing():

    def __init__(self):
        self.pixels = Neopixel(12, 0, 10, "GRB")
        self.running = True

    def startup(self):
        while True:
            for hue in range(0, 65535, 300):
                if not self.running:
                    break
                color = self.pixels.colorHSV(hue, 255, 255)
                self.pixels.fill(color)
                self.pixels.show()
                sleep(0.1)
            else:
                continue
            break
        self.pixels.clear()

    def blink(self):
        self.pixels.fill((255, 100, 100))
        self.pixels.show()
        sleep(0.25)
        self.pixels.clear()

    def click(self):
        for b in range(255, 0, -10):
            self.pixels.fill((50, 100, 50), b)
            self.pixels.brightness(b)
            self.pixels.show()
            sleep(0.05)
        self.pixels.brightness(255)
        self.pixels.clear()
