#!/bin/bash
set -evx

mkdir ~/.sucrcore

# safety check
if [ ! -f ~/.sucrcore/.sucr.conf ]; then
  cp share/sucr.conf.example ~/.sucrcore/sucr.conf
fi
