#!/bin/bash

for I in 1 2 3
do
	echo $I
done

for ((I=1;I<=3;I++))
do 
	echo $I
done

I=1
while [[ $I -le 3 ]]
do
	echo $I
	I=`expr $I + 1`
done

I=1
until [ $I -gt 3 ]; do
	echo $I
	I=`expr $I + 1`
done

echo "I is $I"
if [ $I -eq 1 ]
then
	echo "I is 1"
elif [ $I -eq 2 ]
then
	echo "I is 2"
elif [ $I -eq 3 ]
then
	echo "I is 3"
else
	echo "I is greater than 3"
fi

case $I in
	1)
		echo "I is 1"
		;;
	2)
		echo "I is 2"
		;;
	3)
		echo "I is 3"
		;;
	*)
		echo "I is not 1, 2 or 3"
		;;
esac

