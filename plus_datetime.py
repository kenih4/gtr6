#!/bin/sh
echo "START	launch_plus.sh"

ps aux | grep gtr_datetime.py | grep -v grep | awk '{ print "kill -9", $2 }' | sh | sleep 3 | sh


#	OK
ans=`/home/xfel/xfelopr/local/anaconda3/bin/python3 -OO /home/xfel/xfelopr/kenichi/gtr/gtr_datetime.py /home/xfel/xfelopr/kenichi/gtr/config_PLUS_setting.xlsx /home/xfel/xfelopr/kenichi/gtr/config_PLUS_sig.xlsx 0`
echo $ans


