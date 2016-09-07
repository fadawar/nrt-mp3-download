#!/usr/bin/env bash
source /home/fadawar/.venv/nrt_download/bin/activate
cd /home/fadawar/PycharmProjects/nrt_mp3_download/
python run.py
date +%Y-%m-%d:%H:%M:%S >> access.log
