echo off

cd /d %~dp0

mkdir log
mkdir data
cd config
if not exist config.txt (
  copy config_def.txt config.txt
)
cd ..

python -u main.py >> log\console.log 2>> log\error.log
