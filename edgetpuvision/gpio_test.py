from periphery import GPIO
import sys

led = GPIO("/dev/gpiochip2", 13, "out")  # pin 37
button = GPIO("/dev/gpiochip4", 13, "in")  # pin 36

try:
  while True:
    led.write(True)
    sys.stdout.write(str(button.read()))
finally:
  led.write(False)
  led.close()
  button.close()