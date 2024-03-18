#!/bin/bash

THIS_DIR=`dirname $0`

if [ -f $THIS_DIR/todo.list ]; then
    cp $THIS_DIR/todo.list{,.bak} && sort $THIS_DIR/todo.list.bak > $THIS_DIR/todo.list
    rm $THIS_DIR/todo.list.bak
fi

if [ -f $THIS_DIR/toprint.list ]; then
    cp $THIS_DIR/toprint.list{,.bak} && sort $THIS_DIR/toprint.list.bak > $THIS_DIR/toprint.list
    rm $THIS_DIR/toprint.list.bak
fi

