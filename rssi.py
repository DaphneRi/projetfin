from machine import SPI, I2C, Pin
from rfm69 import RFM69
from bme280 import BME280, BMP280_I2CADDR
import time
import math

# Configuration Constants
FREQ = 432.9
ENCRYPTION_KEY = b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
NODE_ID = 120
BASESTATION_ID = 100

def setup_radio():
    """Initialize RFM69 radio module."""
    spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
    nss = Pin(5, Pin.OUT, value=True)
    rst = Pin(3, Pin.OUT, value=False)
    
    rfm = RFM69(spi=spi, nss=nss, reset=rst)
    rfm.frequency_mhz = FREQ
    rfm.encryption_key = ENCRYPTION_KEY
    rfm.node = NODE_ID
    rfm.destination = BASESTATION_ID
    
    return rfm

def main():
    # Setup
    rfm = setup_radio()
    i2c = I2C(0)
    bmp = BME280(i2c=i2c, address=BMP280_I2CADDR)
    led = Pin(0, Pin.OUT)
    
    # Mission Variables
    counter = 1
    start_time = time.time()
    
    try:
        while True:
            # Read sensor data
            temp, pressure, _ = bmp.raw_values
            altitude = round(-8000 * math.log(pressure / 1013))
            
            # Create message
            msg = f"DATA::{counter}::{time.time() - start_time}::{pressure:.2f}hPa::{temp:.2f}°C::{altitude:.2f}m"
            
            # Transmission
            led.on()
            print("Transmitting:", msg)
            rfm.send(bytes(msg, "utf-8"))
            led.off()
            
            counter += 1
            time.sleep(0.5)
    
    except Exception as e:
        print(f"Mission error: {e}")
        led.off()

if __name__ == "__main__":
    main()