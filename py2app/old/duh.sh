#!/bin/bash

du -h dist > duh && cat duh | cut -d/ -f2- -s > duh_

