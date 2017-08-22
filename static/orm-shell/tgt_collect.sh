#!/bin/bash
#


DIR=$(pwd)
SOFT_DIR=$1


#动作状态标志符  0停止(不检查日志) ;1 待机(不检查日志) ; 2  全量 ; 3 增量
active_flag=0

#-1 异常 0 停止  1  OK （对应动作的 待机 全量 增量无报错）
sync_flag=0


vag_cnt=$(ps -ef | grep $SOFT_DIR/bin/vagentd | grep -v grep | wc -l)
ld_s_cnt_tmp=$(ps -ef | grep -E "$SOFT_DIR/bin/loader -s" | grep -v grep | wc -l)
ld_r_cnt_tmp=$(ps -ef | grep -E "$SOFT_DIR/bin/loader -r" | grep -v grep | wc -l)

ld_s_cnt=`expr $ld_s_cnt_tmp \/ 2`
ld_r_cnt=`expr $ld_r_cnt_tmp \/ 2`

#echo "ld_s_cnt "$ld_s_cnt
#echo "ld_r_cnt "$ld_r_cnt

#ld_s_profile启动脚本定义的loader -s数
#ld_r_profile启动脚本定义的loader -r数
ld_s_profile=$(cat $SOFT_DIR/scripts/start_vagentd | grep "^\$DBPS_HOME/bin/loader -s" | wc -l)
ld_r_profile=$(cat $SOFT_DIR/scripts/start_vagentd | grep "^\$DBPS_HOME/bin/loader -r" | wc -l)

if [ $vag_cnt -eq 2 -a $ld_s_cnt -eq $ld_s_profile -a $ld_r_cnt -eq $ld_r_profile ]
then
  #进程正常
  #echo "all processes are ok."
  #rmp目录不存在cfg.xf1t.struct  cfg.sync  imp_*目录,状态：待机
  if [ ! -e $SOFT_DIR/rmp/cfg.xf1t.struct -a ! -d $SOFT_DIR/rmp/sync0 -a ! -e cfg.sync ]
  then
    #echo "waitting replication"
    #待机不检查日志
    active_flag=1
    sync_flag=1
    #collect_cnt,接收进程数
    echo $vag_cnt
    #vagentd进程数正常不正常都抓取日志
    collect_err=$(cat $SOFT_DIR/log/log.vagentd | tail -100 |grep -E "retry|ORA" | wc -l)
    #collect_err接收进程报错数
    echo $collect_err
    #loader_s_cnt loader -s数
    echo $ld_s_cnt
    #loader_r_cnt  loader -r数
    echo $ld_r_cnt
    #loader_s_p_cnt loader -s配置进程数
    echo $ld_s_profile
    #loader_r_cnt  loader -r配置进程数
    echo $ld_r_profile
    #loader_time
    echo ""
    #loader_err
    echo ""
    #active
    echo $active_flag
    #loader_rate
    echo ""
    #sync_status
    echo $sync_flag
  else
    syncno=$(cat $SOFT_DIR/rmp/cfg.sync | grep -v "^$")
	if [ $syncno -eq 0 -a -d $SOFT_DIR/rmp/real0 ]
	then
	  #如果cfg.sync=0且存在real0目录,则增量
	  #echo "active:real"
	  active_flag=3
      sync_flag=1
	  #collect_cnt,接收进程数
      echo $vag_cnt
      #vagentd进程数正常不正常都抓取日志
      collect_err=$(cat $SOFT_DIR/log/log.vagentd | tail -100 |grep -E "retry|ORA" | wc -l)
      #collect_err接收进程报错数
      echo $collect_err
      #loader_s_cnt loader -s数
      echo $ld_s_cnt
      #loader_r_cnt  loader -r数
      echo $ld_r_cnt
      #loader_s_p_cnt loader -s配置进程数
      echo $ld_s_profile
      #loader_r_cnt  loader -r配置进程数
      echo $ld_r_profile
	  
      #loader_time
	  loader_time=""
      tflag=0
	  while(($tflag<$ld_r_profile))
	  do
	    tcnt=$(tail -5 "$SOFT_DIR/log/log.r$tflag" | grep Time | tail -1 | awk -F"Time" '{print $2}' | wc -l)
		#echo "tflag:"$tflag"-----------tcnt:"$tcnt
		if [ $tcnt -gt 0 ]
		then
	      time_mes=$(tail -5 "$SOFT_DIR/log/log.r$tflag" | grep Time | tail -1 | awk -F"Time" '{print $2}')
	      loader_time=$loader_time"r"$tflag"("$time_mes" );"
		fi
	    tflag=`expr $tflag + 1`
	  done
	  echo $loader_time
	  
	  #依次取得r0~rn的日志报错数,格式:s0-11;s1-error;
	  loader_err=""
          rflag=0
	  while(($rflag<$ld_r_profile))
	  do
	    ldr_err_cnt=$(ps -ef | tail -100 "$SOFT_DIR/log/log.r$rflag" | grep -E "xf1|ORA-00604|rowid not found" | wc -l)
	    if [ $ldr_err_cnt -gt 0 ]
	    then
	      loader_err=$loader_err"r"$rflag"-"$ldr_err_cnt";"
	      sync_flag=-1
	    fi
	    rflag=`expr $rflag + 1`
	  done
      echo $loader_err
	 
      #active
      echo $active_flag
	  
	  loader_rate=""
      #loader_rate,增量查看依次取cfg.loaderno,格式:r0(11);
	  flag=0
	  while(($flag<$ld_r_profile))
	  do
	    if [ -e $SOFT_DIR/rmp/real$flag/cfg.loaderno ]
		then
		  no1=$(cat $SOFT_DIR/rmp/real$flag/cfg.loaderno | awk '{print $1}')
		  no2=$(cat $SOFT_DIR/rmp/real$flag/cfg.loaderno | awk '{print $2}')
		  no3=`expr $no2 - $no1`
		  loader_rate=$loader_rate"r"$flag"("$no3");"
		fi
	    flag=`expr $flag + 1`
	  done
	  
      echo $loader_rate
	  
	  
      #sync_status
      echo $sync_flag
	  
	  
	else
	  #否则全量
	  #echo "active:full"
	  active_flag=2
      sync_flag=1
      #collect_cnt,接收进程数
      echo $vag_cnt
      #vagentd进程数正常不正常都抓取日志
      collect_err=$(cat $SOFT_DIR/log/log.vagentd | tail -100 |grep -E "retry|ORA" | wc -l)
      #collect_err接收进程报错数
      echo $collect_err
      #loader_s_cnt loader -s数
      echo $ld_s_cnt
      #loader_r_cnt  loader -r数
      echo $ld_r_cnt
      #loader_s_p_cnt loader -s配置进程数
      echo $ld_s_profile
      #loader_r_cnt  loader -r配置进程数
      echo $ld_r_profile
      #loader_time
      echo ""
      
	  
	  #依次取得s0~sn的日志报错数,格式:s0-11;s1-error;
	  loader_err=""
      sflag=0
	  while(($sflag<$ld_s_profile))
	  do
	    lds_err_cnt=$(ps -ef | tail -100 "$SOFT_DIR/log/log.s$sflag" | grep -E "ORA-00604" | wc -l)
	    if [ $lds_err_cnt -gt 0 ]
	    then
	      loader_err=$loader_err"s"$sflag"-"$lds_err_cnt";"
		  sync_flag=-1
	    fi
	    sflag=`expr $sflag + 1`
	  done
      echo $loader_err
	 
      #active
      echo $active_flag
      #loader_rate,全量查看cfg.sync数
      echo $syncno
      #sync_status
      echo $sync_flag
	fi
  fi

  
elif [ $vag_cnt -eq 0 -a $ld_s_cnt -eq 0 -a $ld_r_cnt -eq 0 ]
then
  #进程停止
  active_flag=0
  sync_flag=0
  #collect_cnt,接收进程数
  echo 0
  #collect_err接收进程报错数
  echo 0
  #loader_s_cnt loader -s数
  echo $ld_s_cnt
  #loader_r_cnt  loader -r数
  echo $ld_r_cnt
  #loader_s_p_cnt loader -s配置进程数
  echo $ld_s_profile
  #loader_r_cnt  loader -r配置进程数
  echo $ld_r_profile
  #loader_time
  echo ""
  #loader_err
  echo ""
  #active
  echo $active_flag
  #loader_rate
  echo ""
  #sync_status
  echo $sync_flag
else
  #进程不正常
  #echo "prcess number is not ok"
  if [ ! -e $SOFT_DIR/rmp/cfg.xf1t.struct -a ! -d $SOFT_DIR/rmp/sync0 -a ! -e cfg.sync ]
  then
	#待机状态
	sync_flag=-1
	active_flag=1
  else
    #同步状态
	if [ $syncno -eq 0 -a -d $SOFT_DIR/rmp/real0 ]
	then
		#增量
		sync_flag=-1
		active_flag=3
	else
		#全量 
		sync_flag=-1
		active_flag=2
	fi
	
  fi
  
  
  #collect_cnt,接收进程数
  echo $vag_cnt
  
  #如果vagentd进程数正常不正常都抓取日志
  collect_err=$(cat $SOFT_DIR/log/log.vagentd | tail -100 |grep -E "retry|ORA" | wc -l)
  #collect_err接收进程报错数
  echo $collect_err
 
 
  #loader_s_cnt loader -s数
  echo $ld_s_cnt
  #loader_r_cnt  loader -r数
  echo $ld_r_cnt
  #loader_s_p_cnt loader -s配置进程数
  echo $ld_s_profile
  #loader_r_cnt  loader -r配置进程数
  echo $ld_r_profile
  
  #进程数不正常,读取loader -s日志,loader -r日志
  #loader -s 不正常
  loader_err=""
  #echo "begin to check loader -s"
  #如果loader -s 数不等于配置进程数
  if [ ! $ld_s_cnt -eq $ld_s_profile ]
  then
    sflag=0
	#echo "sflag :"$sflag
	while(($sflag<$ld_s_profile))
	do
	  #依次取得s0~sn的进程数,如果不等于2,则显示出来,格式:s0-error;s1-error;
	  pro_s_cnt=$(ps -ef | grep -E "$SOFT_DIR/bin/loader -s -qno $sflag" | grep -v grep | wc -l)
	  #echo "pro_s_cnt :"$pro_s_cnt
	  if [ $pro_s_cnt -lt 2 ]
	  then
	    loader_err=$loader_err"s"$sflag"-Error;"
	  fi
	  sflag=`expr $sflag + 1`
	done
  fi
  
  
  #echo "begin to check loader -r"
  #如果loader -r 数不等于配置进程数
  if [ ! $ld_r_cnt -eq $ld_r_profile ]
  then
    rflag=0
	while(($rflag<$ld_s_profile))
	do
	  #依次取得r0~rn的进程数,如果不等于2,则显示出来,格式:r0-error;r1-error;
	  pro_s_cnt=$(ps -ef | grep -E "$SOFT_DIR/bin/loader -s -qno $rflag" | grep -v grep | wc -l)
	  if [ $pro_s_cnt -lt 2 ]
	  then
	    loader_err=$loader_err"r"$rflag"-Error;"
	  fi
	  rflag=`expr $rflag + 1`
	done
  fi
 
  #loader_time
  echo ""
  #loader_err
  echo $loader_err
  #active
  echo $active_flag
  #loader_rate
  echo ""
  #sync_status
  echo $sync_flag
fi
