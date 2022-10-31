#!/bin/bash

FILENAME="extensions.vsix"

EXTENSIONS=$(cat $FILENAME)

for ext in $EXTENSIONS; do
  code --install-extension $ext
done