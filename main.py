""" Mission 1 - Cansat Emitter Module

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
BMP280 breakout   : https://shop.mchobby.be/product.php?id_product=1118
TMP36             : https://shop.mchobby.be/product.php?id_product=59
Raspberry-Pi PICO : https://shop.mchobby.be/product.php?id_product=2025

See Tutorial
   https://wiki.mchobby.be/index.php?title=ENG-CANSAT-PICO-BELGIUM

See GitHub
   https://github.com/mchobby/cansat-belgium-micropython/tree/main/mission1
"""

from machine import SPI, I2C, Pin, ADC
from rfm69 import RFM69
from bme280 import BME280, BMP280_I2CADDR
import time
import math
from machine import Pin, PWM
from time import sleep

FREQ           = 424
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID        = 120 # ID of this node
BASESTATION_ID = 100 # ID of the node (base station) to be contacted

# Buses & Pins
spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
nss = Pin( 5, Pin.OUT, value=True )
rst = Pin( 3, Pin.OUT, value=False )
i2c = I2C(0)

# RFM Module
rfm = RFM69( spi=spi, nss=nss, reset=rst )
rfm.frequency_mhz  = FREQ
rfm.encryption_key = ( ENCRYPTION_KEY )
rfm.node           = NODE_ID # This instance is the node 120
rfm.destination    = BASESTATION_ID # Send to specific node 100
# BMP280 (uses the BME280)
bmp = BME280( i2c=i2c, address=BMP280_I2CADDR )
#sea level pressure
baseline = 1032.0
#TO CHANGE THE DAY OF LAAAAAAUNCH 
# Onboard LED
led = Pin(0, Pin.OUT)
buzzer = PWM(Pin(22))

# Main Loop
print( 'Frequency     :', rfm.frequency_mhz )
print( 'encryption    :', rfm.encryption_key )
print( 'NODE_ID       :', NODE_ID )
print( 'BASESTATION_ID:', BASESTATION_ID )
print( '***HEADER***' )
print( ":iteration_count,time_sec,pressure_hpa,bmp280_temp;" )
print( '***DATA***' )
counter = 1
ctime = time.time() # Now
data_file = open("MyData.txt", "w")

#METTRE LA PRESSION AMBIANTE SUR TERRE AU MOMENT DU DECOLLAGE
pression_ambiante = 988.2
scale_height = 8400
sea_level_pressure = 1013.25

while True:
	# read BMP280
	t,hpa,rh =  bmp.raw_values # Temp, press_hPa, humidity
	p = bmp.raw_values[1]
	
	#pressure variable
	if p < pression_ambiante+1:
		altitude = round(-scale_height * math.log(p / sea_level_pressure))
			# main message: iteration_count,time_sec,pressure_hpa,tmp36_temp,bmp280_temp (coma separated)
		msg = " - : %i, %is, %6.2fhPa, %5.2f°C, %5.2fm; (sol)" % (counter,time.time()-ctime,hpa,t, altitude, ) + " \n"
		led.on() # Led ON while sending data
		print( msg )
		print(  )
		
		# Send a packet without ACK - Send it, don't care if it is received or not
		rfm.send(bytes(msg , "utf-8"))
		led.off()
		counter += 1
		time.sleep(0.5) # wait 0.5 second
		data_file.write( msg )
		data_file.flush()       
		# Initialisation du buzzer sur la broche 22
	else:
		altitude = round(-scale_height * math.log(p / sea_level_pressure))
		# main message: iteration_count,time_sec,pressure_hpa,tmp36_temp,bmp280_temp (coma separated)
		msg = " - : %i, %is, %6.2fhPa, %5.2f°C, %5.2fm;" % (counter,time.time()-ctime,hpa,t, altitude, ) + " \n"
		led.on() # Led ON while sending data
		print( msg )
		print(  )
		
		# Send a packet without ACK - Send it, don't care if it is received or not
		rfm.send(bytes(msg , "utf-8"))
		led.off()
		counter += 1
		time.sleep(0.5) # wait 0.5 second
		data_file.write( msg )
		data_file.flush()
		buzzer.duty_u16(0)
		buzzer.duty_u16(1000)
		buzzer.freq(440)
data_file.close()
print("Data saved succesfuly\n\n")

data_file = open("MyData.txt", "r")
Text_data = data_file.read()
print(Text_data)
data_file.close()
print("\n\nAll done ! ")



