#!/bin/bash

MYNAME="vectorwang"

for FILE in `ls /etc`; do
	echo "${MYNAME} ${FILE}"
done

#readonly MYNAME
#MYNAME="2015"
# terminates on the line above, below will not be executed
#echo $!

#unset MYNAME
#echo $MYNAME
#echo $!

echo "Hello, I know you are \"$MYNAME\""
# ' can be used to concat
MYSTRING='Hello, I know you are "'$MYNAME'"'
echo MYSTRING
echo "length of MYSTRING is ${#MYSTRING}"
# need " cause MYSTRING contains spaces
echo "length of MYSTRING is "`expr length "$MYSTRING"`
echo "slice of MYSTRING from place 1, 4 letters \"${MYSTRING:1:4}\""
# this two lines are different cuz expr indexes from 1
echo "slice of MYSTRING from place 1, 4 letters \""`expr substr "$MYSTRING" 1 4`"\""
echo "first v or H in MYSTRING "`expr index "$MYSTRING" Hv`

# arrays in script
MYARRAY=(1 2 3)
# print all elements
echo ${MYARRAY[@]}
echo ${MYARRAY[*]}
# print length
echo ${#MYARRAY[@]}
