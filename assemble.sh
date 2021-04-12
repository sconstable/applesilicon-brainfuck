#!/usr/bin/env zsh
sourcefile=$1
prefix=$(basename $sourcefile .s)
as -o ${prefix}.o $sourcefile
ld -e _start -arch arm64 -o $prefix -lSystem -L$(xcode-select -p)/SDKs/MacOSX.sdk/usr/lib $prefix.o
