from periphery import GPIO
from periphery import PWM
import sys

led = GPIO("/dev/gpiochip2", 13, "out")  # pin 37
pwm = PWM(0, 0)

try:
  while True:
    pwm.frequency = 1e3
    pwm.duty_cycle = .75
    pwm.enable()
finally:
  led.write(False)
  led.close()
  pwm.close()