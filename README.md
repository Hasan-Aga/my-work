# my-work

## install quagga:
first clone this repo using Git, then find and unzip quagga-1.2.1.tar.gz (make sure that you grant yourself write permissions for the new folder) and cd into it, then:
```
sudo apt update

sudo apt install gawk

sudo apt install libreadline6 libreadline6-dev

sudo apt install libtool

sudo libtoolize --force

sudo aclocal

sudo autoheader

sudo automake --force-missing --add-missing

sudo autoconf

sudo apt install libc-ares-dev

sudo ./configure  --enable-vtysh --enable-user=root --enable-group=root --enable-vty-group=root

sudo make install
```

There is a zebra.conf.sample file in /usr/local/etc under the quagga folder,You need to create a zebra.conf file and copy the content of zebra.conf.sample into it, so run the follwoing:
```
cd /usr/local/etc/

sudo cp zebra.conf.sample zebra.conf
```
then run sudo zebra -d

if you get an error, then do the following and try again:
```
cd /usr/local/lib
sudo cp libzebra.* /lib
sudo rm libzebra.*
```
After that you can connect to the zebra console using telnet (password=zebra):
```
telnet localhost 2601
```
then, test if OSPFD can run with no problems by running:
```
sudo ospfd -d
```
if you get an error, then run:
```
cd /usr/local/lib
sudo cp libospf.* /lib
```

## run the experiment
run the python script that is inside the 'advanced' directory.

