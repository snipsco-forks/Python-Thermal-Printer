#/usr/bin/env bash -e

VENV=venv

if [ ! -d "$VENV" ]
then

	PYTHON=`which python2`

	if [ ! -f $PYTHON ]
	then
		echo "could not find python"
	fi
	virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate

sudo apt-get install git cups wiringpi build-essential libcups2-dev libcupsimage2-dev python-serial python-pil python-unidecode

git clone https://github.com/adafruit/zj-58
cd zj-58
make
sudo ./install
cd ..
sudo lpadmin -p ZJ-58 -E -v serial:/dev/serial0?baud=19200 -m zjiang/ZJ-58.ppd
sudo lpoptions -d ZJ-58

pip install -r requirements.txt
