#!/bin/sh
cd /home
sudo git clone https://github.com/Quagga/quagga.git

cd quagga/
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

