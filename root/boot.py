# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import network
import lib.display.DISPLAY

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
#sta_if.scan()                             # Scan for available access points
sta_if.connect("SSID", "It's a Secret") # Connect to an AP
sta_if.isconnected()                      # Check for successful connection

sta_if.ifconfig()

_calibration = None

#import webrepl
#webrepl.start()
