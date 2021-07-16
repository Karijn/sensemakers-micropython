esptool.py -p com4 -b 115200 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 bootloader-lv8.1.bin 0x8000 partition-table-lv8.1.bin 0x10000 micropython-lv8.1.bin

pause