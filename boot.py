from machine import I2C, Pin, PWM
import utime
import sh1107

keydict = {
  69 : "Button: 1",
  70 : "Button: 2",
  71 : "Button: 3",
  68 : "Button: 4",
  64 : "Button: 5",
  67 : "Button: 6",
  7 : "Button: 7",
  21 : "Button: 8",
  9 : "Button: 9",
  22 : "Button: *",
  25 : "Button: 0",
  13 : "Button: #",
  24 : "Button: UP",
  8 : "Button: LEFT",
  28 : "Button: OK",
  90 : "Button: RIGHT",
  82: "Button: DOWN"
}


PIN = Pin(13, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
display = sh1107.SH1107_I2C(128, 64, i2c, 0x3c)

display.fill(1)
display.text('www.magazin', 0, 45, 0)
display.text('mehatronika.com', 5, 55, 0)
display.line(0, 43, 128, 43, 0)
display.show()

for i in range (0, 4):
    display.text("Wait: {}".format(4-i), 30, 18, 1)
    display.text("Wait: {}".format(3-i), 30, 18, 0)
    display.show()
    utime.sleep(1)

display.text("Wait: {}".format(3-i), 30, 18, 1)
display.text("Press key", 30, 18, 0)
display.show()

N=0

while True:
    if PIN.value() == 0:
        count = 0
        while PIN.value() == 0 and count < 200:
            count += 1
            utime.sleep_us(60)
        count = 0
        while PIN.value() == 1 and count < 80:
            count += 1
            utime.sleep_us(60)
        idx = 0
        cnt = 0
        data = [0,0,0,0]
        for i in range(0,32):
            count = 0
            while PIN.value() == 0 and count < 15:
                count += 1
                utime.sleep_us(60)
            count = 0
            while PIN.value() == 1 and count < 40:
                count += 1
                utime.sleep_us(60)
            if count > 8:
                data[idx] |= 1<<cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1
        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:
            
            N=data[2]
            display.fill(0)
            display.text(keydict[N], 0, 10, 1)
            display.text("Key Value: {}".format(N), 0, 26, 1)
            display.text('www.magazin', 0, 45, 1)
            display.text('mehatronika.com', 5, 55, 1)
            display.line(0, 43, 128, 43, 1)
            display.show()
