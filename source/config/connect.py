print('in connect')
import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("MICSHOME", "Attcogb1!Wessing")
for i in range(100):
    if sta_if.isconnected():
        break
    print('waiting...')

try:
    import ntptime
    ntptime.settime()
except:
    print('error in ntptime')
    
