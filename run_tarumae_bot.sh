#!/bin/bash

cd ~/tarumae-bot

mkdir log
mkdir data

./run_tarumae_bot_1.sh 1>>log/console.log 2>>log/error.txt &

