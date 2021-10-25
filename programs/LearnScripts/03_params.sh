#!/bin/bash

echo $#
echo $0
echo $1
echo $2
echo $3

echo "-- \$* --"
for I in "$*"; do
	echo $I
done

echo "-- \$@ --"
for I in "$@"; do
	echo $I
done
