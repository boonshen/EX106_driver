#!/bin/bash
#This file is to clean .pyc files
rm *.pyc 2>/dev/null
if [ "$?" = "1" ];then
	echo "no trash file"
fi
