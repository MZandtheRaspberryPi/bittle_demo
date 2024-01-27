# bittle_demo
A repository to show off a demo with the bittle.

1. [Replicating](#Replicating)
    1. [Pi Setup](#PiSetup)
    2. [Hardware Setup](#HardwareSetup)
    3. [Camera & Wlan](#Camera&Wlan)
    4. [Demo](#Demo)  

### Demo
## Replicating

My hardware setup looked like this and included a Raspberry Pi Zero 2 W, Male to Female 2.54 dupont cables, a MU3 Vision sensor, some 3d printed parts, and a Bittle wtih a NyBoard V1_2.  

![full_setup](./assets/full_hardware_setup.jpg)


### PiSetup

I used a raspberry pi zero 2 w. I thought the small size and weight of this would be helpful for the Bittle's walking. The CPU with 4 cores running at 1GHz is punchy.  

I used Ubuntu 22.04 as the operating system. I used the raspberry pi imager tool to flash an SD card and input wlan details and enable ssh. I first booted without a connection to the NyBoard to disable the serial console and such as per below.  

On Raspberry Pi OS the the relevant files are in a different folder, /boot i believe.
1. Ensure that the line `enable_uart=1` is uncommented in the /boot/firmware/config.txt file, it should be by default.
2. remove any reference to console in /boot/firmware/cmdline.txt, ie remove `console=serial0,115200`.
3. disable the serial console `sudo systemctl stop serial-getty@ttyS0.service && sudo systemctl disable serial-getty@ttyS0.service`

From here I considered briefly how the raspberry pi is a non-real time operating system and doing things using software with the GPIO pins can be difficult as the OS taketh and giveth resources. Then I installed a software serial port to talk to the camera to setup wlan.  


```
git clone https://github.com/adrianomarto/soft_uart
cd soft_uart
make
sudo apt-get update && sudo apt-get install checkinstall
sudo checkinstall # a menu will come up, follow instructions and accept defaults
```  

Install some code we will use later
```
pip install my-bittle my-mu3
```

### HardwareSetup
The below steps mostly use internal labels (from 1 to 40) to refer to pin numbers, NOT Broadcom (BCM) Naming (such as GPIO2). 
1. Flip the two switches labelled output on the left of the MU3 camera to up to set the MU3 to image transmission mode.  
2. Plug the MU3 power into the pi zero 3.3 volt power, pin 17. Plug the MU3 ground into the pi ground pin 20. Plug the MU3 RX pin (white cable often) into the pi pin 24 (GPIO 8 in BCM convention). Plug the MU3 TX pin (yellow cable often) into the pi pin 26 (GPIO7). 
3. Plug the pi zero 2 w into the Bittle via the NyBoard.

### Camera&Wlan
You will have to do this each time the camera is powered on. It will not save after a camera reset.  
1. ssh into the pi (I use MobaXterm).  
2. bring up the software serial port to talk to the camera `sudo insmod ~/soft_uart/soft_uart.ko gpio_tx=8 gpio_rx=7`
3. connect the MU3 to your wlan, inputting your wlan (wifi) details into the command. Note no spaces in the ssid name or in the password.  `setup-wlan my_ssid my_password /dev/ttySOFT0`. You should see the front lights on the MU3 turn off and the back light turn on indicating it is connected. You should also see an IP Address printed in the terminal that the camera received. On a computer connected to the same network, you should be able to type this ip address into your url bar and see a camera interface, including an image stream. You could also use developer tools in chrome to see the address and port of the stream.    
4. Unload the kernel module for the software serial port `sudo rmmod soft_uart.ko`

### Demo
The first time you run this script it may be helpful to have the Bittle on a test stand where its legs can't touch the ground to prevent hurting it in case of bugs/errors. A stack of books can work nicely for this.  

```
git clone https://github.com/MZandtheRaspberryPi/bittle_demo.git  
cd bittle_demo
# input your mu3 ip address into the global variable 'IP_ADDRESS' in come_to_me.py
python3 come_to_me.py
```

If you move your face in front of the camera, the Bittle should start to walk forward. Detection is not great, so you may need to move your face around and try different angles. To exit the script, hold 'q'.

It will print out the frame rate of the camera and of the face detection algorithm. It will also create a timestamped folder with images from the camera. You may wish to make a video of the output images, to do so you could use ffmpeg inputting the framerate that the script prints.   

```
ffmpeg -framerate 5.3 -i ./20240122-233344/frame_%d.png -c:v libx264 -pix_fmt yuv420p my_bittle.mp4
```


## Connecting to the Camera

pixels resolution, object resolution

data transfer

mu 3 capabilities
no firmware, 
4 modes, image transmission last
at commands
wlan connecting

solution
http stream

face detection

## Connecting to the Bittle Robot

serial commands, serial bug in pyserial

own library, other library found


## Ideas for Extensions
Follow left/right?
Better method thans harscascade
