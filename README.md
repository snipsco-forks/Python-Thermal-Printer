Python-Thermal-Printer
======================


sudo raspi-config


Under “Interfacing Options,” select “Serial.” Turn OFF the login shell over serial, and ENABLE the hardware serial port. NO and YES, respectively.


sudo apt-get install git cups wiringpi build-essential libcups2-dev libcupsimage2-dev python-serial python-pil python-unidecode

git clone https://github.com/adafruit/zj-58
cd zj-58
make
sudo ./install
cd ..
sudo lpadmin -p ZJ-58 -E -v serial:/dev/serial0?baud=19200 -m zjiang/ZJ-58.ppd
sudo lpoptions -d ZJ-58
sudo adduser _snips-skills dialout
