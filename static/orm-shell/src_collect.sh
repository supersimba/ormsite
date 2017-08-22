#!/bin/bash
#



DIR=$(pwd)
SOFT_DIR=$1

#动作标志符 
#0停止  1  待机    2  实时分析 
active_flag=0


#同步状态  
#-1 异常 0 停止  1  OK （对应动作的 待机  实时分析无报错）
sync_flag=0


vErr=0
sErr=0

dbps_cnt=$(ps -ef | grep $SOFT_DIR/bin/dbpsd | grep -v grep | wc -l)
vag_cnt=$(ps -ef | grep $SOFT_DIR/bin/vagentd | grep -v grep | wc -l)
snd_cnt=$(ps -ef | grep $SOFT_DIR/bin/sender | grep -v grep | wc -l)


if [ $dbps_cnt -eq 0 -a $vag_cnt -eq 0 -a $snd_cnt -eq 0 ]
#进程未启动
then
    dbps_cnt=0
    vag_cnt=0
    snd_cnt=0
    sync_flag=0
    active_flag=0
    vag_err=""
    snd_err=""
    capture_rate=""
    
    
    
    echo $dbps_cnt
    echo $vag_cnt
    echo $snd_cnt
    echo $sync_flag
    echo $active_flag
    echo $vag_err
    echo $snd_err
    echo $capture_rate
else
    #进程启动
    #如果进程正常
    if [ $dbps_cnt -eq 1 -a $vag_cnt -eq 2 -a $snd_cnt -eq 2 ]
    then
        f1_num=$(ls -lrt $SOFT_DIR/rmp | grep 2.cfg.senderno | wc -l)
        f2_num=$(ls -lrt $SOFT_DIR/rmp | grep cfg.ctl | wc -l)
        #2.cfg.senderno 和cfg.ctl 不存在,待机状态
        #active_flag=0
        if [ $f1_num -eq 0 -a $f2_num -eq 0 ]
        then
          active_flag=1
        else
          active_flag=2
        fi

        if [ -e $SOFT_DIR/log/log.vagentd ]
        then
              vag_err=$(tail -50 $SOFT_DIR/log/log.vagentd | grep -iE "ORA|Err" | wc -l)
              if(($vag_err>5))
              then
                  vErr=-1
              else
                  vErr=0
              fi
        else
          vag_err=-999
        fi
        if [ -e $SOFT_DIR/log/log.sender ]
        then
              snd_err=$(tail -50 $SOFT_DIR/log/log.sender | grep -iE "retry" | wc -l)
              if(($snd_err>5))
              then
                  sErr=-1
              else
                  sErr=0
              fi
        else
          snd_err=-999
        fi
        
        if [ $vErr -eq 0 -a $sErr -eq 0 ]
        then
          sync_flag=1
        else
          sync_flag=-1
        fi
        
        #capture_rate=$(tail rate.tmp | grep -v "^$")
        capture_rate=""
        
        echo $dbps_cnt
        echo $vag_cnt
        echo $snd_cnt
        echo $sync_flag
        echo $active_flag
        echo $vag_err
        echo $snd_err
        echo $capture_rate
    else
        #进程不正常
        #这3个值取具体值
        #dbps_cnt=0
        #vag_cnt=0
        #snd_cnt=0
        
		f1_num=$(ls -lrt $SOFT_DIR/rmp | grep 2.cfg.senderno | wc -l)
        f2_num=$(ls -lrt $SOFT_DIR/rmp | grep cfg.ctl | wc -l)
        #2.cfg.senderno 和cfg.ctl 不存在,待机状态
        #active_flag=0
        if [ $f1_num -eq 0 -a $f2_num -eq 0 ]
        then
          active_flag=1
        else
          active_flag=2
        fi
		
        if [ -e $SOFT_DIR/log/log.vagentd ]
        then
            vag_err=$(tail -50 $SOFT_DIR/log/log.vagentd | grep -iE "ORA|Err" | wc -l)
        else
            vag_err=0
        fi
		
        if [ -e $SOFT_DIR/log/log.sender ]
        then
            snd_err=$(tail -50 $SOFT_DIR/log/log.sender | grep -iE "ORA|Err" | wc -l)
        else
            snd_err=0
        fi
        
        sync_flag=-1
        #active_flag=-1
        capture_rate=""
        
        echo $dbps_cnt
        echo $vag_cnt
        echo $snd_cnt
        echo $sync_flag
        echo $active_flag
        echo $vag_err
        echo $snd_err
        echo $capture_rate
    fi
fi
