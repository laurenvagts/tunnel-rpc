#!/bin/bash
while read -r CMD ; do 
    echo "\$ $CMD"
    $CMD 
    printf "\n%d" $?
done