#!/bin/bash

MYARRAY=(a b c "abc")

echo ${MYARRAY[*]}

MYARRAY[0]="bcd"

echo ${MYARRAY[@]}

echo "Length of MYARRAY: "${#MYARRAY[*]}

echo "Items in MYARRAY: "
for ITEM in ${MYARRAY[@]}; do
	echo $ITEM
done

