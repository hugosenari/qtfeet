yes | sudo add-apt-repository ppa:ubuntu-sdk-team/ppa
sudo apt-get update -qq
sudo apt-get upgrade -qq
sudo apt-get install python-dev python3-dev  qt5-qmake qt5-default qtchooser 
sudo ln -s /usr/include/python2.7 /usr/local/include/python2.7
mkdir build_pyqt
cd build_pyqt
curl -OL http://sourceforge.net/projects/pyqt/files/sip/sip-4.15.1/sip-4.15.1.tar.gz
tar -xvf sip-4.15.1.tar.gz
cd sip-4.15.1
python configure.py
make
sudo make install
cd ..
curl -OL http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.0.1/PyQt-gpl-5.0.1.tar.gz
tar -xvf PyQt-gpl-5.0.1.tar.gz
cd PyQt-gpl-5.0.1
python configure.py --confirm-license
make -j
sed -i -r "s/.+strip.+pyuic5/ /" Makefile
sudo make install
