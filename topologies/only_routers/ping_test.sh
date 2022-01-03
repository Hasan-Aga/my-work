#!/bin/bash

# call script with interface names of device
for arg
do ip link set $arg down



echo "Started ping test ..."

read -t 10 -p "Waiting for 10 seconds ..."

for arg
do ip link set $arg up
