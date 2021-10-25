#!/bin/bash

VAL=`expr 1 + 2`
echo "1+2=$VAL"

VALA=10
VALB=20
VAL=`expr $VALA \* $VALB`
echo "$VALA * $VALB = $VAL"

if [ $VALA -lt $VALB ]
then
	echo "VALA is less than VALB"
elif [ $VALA -eq $VALB ]
then
	echo "VALA is equal to VALB"
else
	echo "VALA is greater than VALB"
fi

if [ $VALA -le 10 -a $VALB -ge 20 ]; then
	echo "VALA less than 10 and VALB greater than 20"
fi

if [[ $VALA -le 10 && $VALB -ge 20 ]]; then
	echo "VALA less than 10 and VALB greater than 20"
fi
