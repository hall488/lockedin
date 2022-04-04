import board
import digitalio

led = digitalio.DigitalInOut(board.GPIO_P37)  # pin 37
led.direction = digitalio.Direction.OUTPUT


try:
  while True:
    led.value = True;
finally:
  led.value = False
  led.deinit()