#!/bin/bash

FILENAME="lextensions.vsix"

EXTENSIONS=$(cat $FILENAME)

for ext in $EXTENSIONS; do
  code --install-extension $ext
done