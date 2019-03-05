#!/bin/ksh

LOGFILE=/home/appadmin/suresh/logs/test_run_$(date +%y%m%d%H%M).log
#sudo salt vlingursrv0787 state.apply test_suresh > $LOGFILE
#sudo salt vlingursrv0795.maxlife.max.com state.apply test_suresh > $LOGFILE
sudo salt vlingursrv0795.maxlife.max.com state.apply test_db > $LOGFILE
