# my-work
This is a guide on how to create a simple topology inside Mininet, the first part guides you through installing Quagga which is a routing software suite, providing implementations of several routing protocols which we use to create routers for our topology, the second part of the guide contains instructions on how to run the Python script that will actually fire up Mininet and build the topology.
note that you must be inside Mininet VM for the 2nd part to work.

## part one: install quagga:
first clone this repo using Git, then find and unzip quagga-1.2.1.tar.gz (make sure that you grant yourself write permissions for the new folder) and cd into it, then:
```
sudo apt update

sudo apt install gawk

sudo apt install libreadline-dev

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

There is a zebra.conf.sample file in ```/usr/local/etc``` under the quagga folder,You need to create a zebra.conf file and copy the content of zebra.conf.sample into it, so run the follwoing:
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
then, test if OSPFD by running:
```
sudo ospfd -d
```
if you get an error, then run:
```
cd /usr/local/lib
sudo cp libospf.* /lib
```

## part two: run the experiment
to run the experiment, first copy one of the topology folders and edit the ```addressConfiguration.json``` file so it has all the routers and the connections between them, the edit the python script by adding your hosts if any and connecting them to the router (edit the builder function where it says ```addHost``` and ```addLink```

## note
when modifying the "links" section of the json file, make sure that the order is correct by first listing the interface with the smaller number, ex:
say we want to link `r1-eth1` with `s1` and `r1-eth0` with `s1` as well, then the correct order is:
    ```
    "r1-eth0": "s1",
    "r1-eth1": "s1"
    ```
and the same applies for the rest of the links in the topology.