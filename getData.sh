# 00 04 * * * sh /root/bantest/tool/AutoData/Code/getData.sh 

export LANG=zh_CN.GB18030
echo $LANG

n=`date +%Y%m%d-%H%M%S`
mv /root/bantest/tool/AutoData/Code/log/stdout.log /root/bantest/tool/AutoData/Code/log/stdout_$n.log
mv /root/bantest/tool/AutoData/Code/log/stderr.log /root/bantest/tool/AutoData/Code/log/stderr_$n.log

/usr/local/bin/python -u /root/bantest/tool/AutoData/Code/main.py 1>>/root/bantest/tool/AutoData/Code/log/stdout.log 2>>/root/bantest/tool/AutoData/Code/log/stderr.log &

