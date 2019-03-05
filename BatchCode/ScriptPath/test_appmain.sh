#!/bin/sh

logpath='/home/appadmin/suresh/logs'
#logfile=$logpath/"test_maintenance_$(date +%y%m%d%H%M).log"
logfile=$logpath/"test_maintenance.log"

logger()
{
    d=`date`
    echo "$d: $@"
    echo "===============================================================================" >> $logfile
    echo "$d: $@" >> $logfile
}

# Restarting Integration and Escalation services
for srv in `cat serverlist | awk '{print $1}'`
do
    msg="Starting automation tasks for server: $srv ..."
    logger $msg
    retval=`sudo salt $srv state.apply test_suresh`
    if [ $? -eq 0 ]
    then
	echo $retval
        msg="... Success: Automation task on server: $srv executed successfully"
        logger $msg
    else
        msg="... Failed: Automation task on server: $srv failed. Please check log file: $logfile"
        logger $msg
    fi
    printf "%s\n\n" "$retval" >> $logfile
done

# Restarting IIS services
for srv in vlingursrv0795.maxlife.max.com
do
    msg="Starting automation tasks for server: $srv ..."
    logger $msg
    retval=`sudo salt $srv state.apply test_db`
    if [ $? -eq 0 ]
    then
        msg="... Success: Automation task on server: $srv executed successfully"
        logger $msg
    else
        msg="... Failed: Automation task on server: $srv failed. Please check log file: $logfile"
        logger $msg
    fi
    printf "%s\n\n" "$retval" >> $logfile
done