from periphery import GPIO

gpio_p13 = GPIO("/dev/gpiochip0", 6, "out")

while True:
    gpio_p13.write(True);
