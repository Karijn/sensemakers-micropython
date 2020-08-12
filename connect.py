import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("MICSHOME", "Attcogb1!Wessing")
station.isconnected()
station.ifconfig()
