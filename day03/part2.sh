#!/bin/bash
SUM=0
for NUM in $(grep -oE "(don't\(\)|do\(\)|mul\([0-9]{1,3},[0-9]{1,3}\))" input | sed -re 's/^do/#do/g' | tr \\n " " | tr "#" \\n | grep -vF "don't()" | grep -oE "(don't\(\)|do\(\)|mul\([0-9]{1,3},[0-9]{1,3}\))" | grep -vF "do()" | sed -re 's/mul\(([0-9]{1,3}),([0-9]{1,3})\)/\1*\2/' | bc); do
	SUM=$((SUM+NUM))
done
echo $SUM
