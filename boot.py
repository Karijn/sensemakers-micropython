import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("SSID", "geheim")
station.isconnected()
station.ifconfig()


# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
webrepl.start()
