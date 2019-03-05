#!/bin/sh

logpath='/home/appadmin/webapp/AMP/BatchCode/ScriptLogs'
logfilename=$logpath/'crm_maintenance_vineet.log'

logger()
{
    d=`date`
    echo "$d: $@"
    echo "$d: $@" >> $logfilename
}

# Restarting Integration and Escalation services
for srv in VMGURSRV0392
do
    msg="Starting automation tasks for server: $srv ..."
    logger $msg
    retval=`salt $srv state.apply crm_svc_restart`
    if [ $? -eq 0 ]
    then
        msg="... Success: Automation task on server: $srv executed successfully"
        logger $msg
    else
        msg="... Failed: Automation task on server: $srv failed. Please check log file: $logfilename"
        logger $msg
    fi
    printf "%s\n\n" "$retval" >> $logfilename
done

# Restarting IIS services
for srv in vmgursrv0395 vmgursrv0396
do
    msg="Starting automation tasks for server: $srv ..."
    logger $msg
    retval=`salt $srv state.apply crm_iisreset`
    if [ $? -eq 0 ]
    then
        msg="... Success: Automation task on server: $srv executed successfully"
        logger $msg
    else
        msg="... Failed: Automation task on server: $srv failed. Please check log file: $logfilename"
        logger $msg
    fi
    printf "%s\n\n" "$retval" >> $logfilename
done
