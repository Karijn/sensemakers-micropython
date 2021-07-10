import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()                             # Scan for available access points
sta_if.connect("MICSHOME", "Attcogb1!Wessing") # Connect to an AP
sta_if.isconnected()                      # Check for successful connection
