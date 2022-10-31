#!/bin/bash


for i in ${pkglist[@]}; do
  code --install-extension $i
done