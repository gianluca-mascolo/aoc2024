#!/bin/bash
cat input | sed -re 's/^$/#/' | sed -re 's/[^0-9,#]//g' | sed -re 's/^([0-9]+),([0-9]+)$/\1,\2,/' | tr -d \\n | tr '#' \\n > input.csv
