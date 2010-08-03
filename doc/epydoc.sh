#!/bin/bash
epydoc --html ../infobiotics/*.py -o ./epydoc --name "Infobiotics Dashboard" --docformat restructuredtext --graph all --inheritance grouped
