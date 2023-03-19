#!/bin/bash

cd ~/tarumae-bot

# ヘッドレスモード設定
export TARUMAE_BOT_HEADLESS=YES

# 二重起動防止

[[ $$ != `pgrep -fo "$0"`  ]] && [[ $PPID != `pgrep -fo "$0"`  ]] && echo "$0 is already running" && exit 2 

# ディレクトリ生成
mkdir log
mkdir data

# configがない場合は生成
cd config
if [ ! -e config.txt ]; then
  cp config_def.txt config.txt
fi
cd ..

python3 -u main.py
