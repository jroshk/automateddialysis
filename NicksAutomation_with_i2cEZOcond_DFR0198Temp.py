
#!/usr/bin/python
import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)

#!/usr/bin/env python
import os

# if __name__ == '__main__':
#     try:
#         serialNum = sensor()
#         loop(serialNum)
#     except KeyboardInterrupt:
#         kill()

def print_devices(device_list, device):
    for i in device_list:
        if(i == device):
            print("--> " + i.get_device_info())
        else:
            print(" - " + i.get_device_info())
    #print("")
    
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    
    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        try:
            moduletype = response.split(",")[1] 
            response = device.query("name,?").split(",")[1]
        except IndexError:
            print(">> WARNING: device at I2C address " + str(i) + " has not been identified as an EZO device, and will not be queried") 
            continue
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 

#function to pull conductivity from probes EZO probe

    

def sensor():
        for i in os.listdir('/sys/bus/w1/devices'):
            global ds18b20
            if i != 'w1_bus_master1':
               ds18b20 = i
        return ds18b20

def read(ds18b20):
        location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
        tfile = open(location)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        global celsius
        celsius = temperature / 1000
        #farenheit = (celsius * 1.8) + 32
        return celsius#, farenheit
    
    def kill():
        quit()
        
    if __name__ == '__main__':
        try:
            serialNum = sensor()
        except KeyboardInterrupt:
            kill()
            
        
    device_list = get_devices()
        
    device = device_list[0]
   
    
def get_conductivity():  
    delaytime = device.long_timeout
    while True:
        for dev in device_list:
        #added these next 3 lines to push temperature correction to EZO probe
          read(ds18b20)
          dev.write("T,%0.2f" % celsius)
          time.sleep(delaytime)
          #read function from before (note there is read + temperature correction command in newer EZO circuit  boards)
          dev.write("R")
          time.sleep(delaytime)
        for dev in device_list:
          print(dev.read())
			    print(celsius)
                
            except KeyboardInterrupt:       # catches the ctrl-c command, which breaks the loop above
                print("Continuous polling stopped")
                print_devices(device_list, device)
                
        # send a command to all the available devices
        elif user_cmd.upper().strip().startswith("ALL:"):
            cmd_list = user_cmd.split(":")
            for dev in device_list:
                dev.write(cmd_list[1])
            
            # figure out how long to wait before reading the response
            timeout = device_list[0].get_command_timeout(cmd_list[1].strip())
            # if we dont have a timeout, dont try to read, since it means we issued a sleep command
            if(timeout):
                time.sleep(timeout)
                for dev in device_list:
                    print(dev.read())
                
        # if not a special keyword, see if we change the address, and communicate with that device
        else:
            try:
                cmd_list = user_cmd.split(":")
                if(len(cmd_list) > 1):
                    addr = cmd_list[0]
                    
                    # go through the devices to figure out if its available
                    # and swith to it if it is
                    switched = False
                    for i in device_list:
                        if(i.address == int(addr)):
                            device = i
                            switched = True
                    if(switched):  
                        print(device.query(cmd_list[1]))
                    else:
                        print("No device found at address " + addr)
                else:
                    # if no address change, just send the command to the device
                    print(device.query(user_cmd))
            except IOError:
                print("Query failed \n - Address may be invalid, use list command to see available addresses")

                    
if __name__ == '__main__':
    main()
