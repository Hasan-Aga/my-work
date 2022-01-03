#!/bin/bash


ip link set $1-eth1 down
ip link set $1-eth2 down


echo "Started ping test ..."

read -t 10 -p "Waiting for 10 seconds ..."

ip link set $1-eth1 up
ip link set $1-eth2 up
