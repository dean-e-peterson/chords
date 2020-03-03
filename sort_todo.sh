#!/bin/bash

THIS_DIR=`dirname $0`
cp $THIS_DIR/todo.txt{,.bak} && sort $THIS_DIR/todo.txt.bak > $THIS_DIR/todo.txt

if [ -f $THIS_DIR/toprint.txt ]; then
    cp $THIS_DIR/toprint.txt{,.bak} && sort $THIS_DIR/toprint.txt.bak > $THIS_DIR/toprint.txt
fi

