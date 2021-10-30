#!/bin/bash

fun_with_out_return(){
	echo "There are $# params"

	for ITEM in $@; do
		echo $ITEM
	done
}


fun_with_out_return a b c d e f

fun_with_return(){
	echo "There are $# params"
	
	SUM=0
	for ITEM in $@; do
		SUM=`expr $SUM + $ITEM`
	done

	return $SUM
}

fun_with_return 1 2 3
echo "The sum is $?"
