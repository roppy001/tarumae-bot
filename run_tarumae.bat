echo off

cd /d %~dp0

mkdir log
mkdir data

python -u main.py >> log\console.log 2>> log\error.log
