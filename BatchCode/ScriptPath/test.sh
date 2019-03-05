for srv in `cat /home/appadmin/webapp/AMP/BatchCode/ScriptPath/serverlist | awk '{print $1}'`
do
    msg="Starting automation tasks for server: $srv ..."
    echo $msg
    echo "sleeping"
    sleep 10
    echo "woke up"
done

