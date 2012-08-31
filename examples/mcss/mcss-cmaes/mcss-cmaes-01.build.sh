#!/bin/sh

g++ -Wall -fPIC `pkg-config --cflags mcss` -c mcss-cmaes-01.cpp &&
g++ -Wall `pkg-config --libs mcss` -shared -Wl,-soname,mcss-cmaes-01.so -o mcss-cmaes-01.so mcss-cmaes-01.o &&
echo "ok" ||
echo "error"
