#!/bin/bash
epydoc -v --html ../infobiotics -o ./epydoc --name "Infobiotics Dashboard `cat ../VERSION.txt`" --docformat plaintext --graph all --inheritance grouped $*
