#!/bin/bash
###########################################################
#
# Copyright (c) 2013, 2014 Veristorm Incorporated
#
###########################################################
#!/bin/sh
echo " "
echo " Stopping vStore Servers..."
echo " Stopping Hadoop..."
z_base="/opt/vse"
z_hadoop="hadoop"
z_zookeeper="zookeeper"
z_hbase="hbase"

$z_base/$z_hadoop/sbin/mr-jobhistory-daemon.sh stop historyserver
$z_base/$z_hadoop/sbin/stop-yarn.sh
$z_base/$z_hadoop/sbin/stop-dfs.sh
$z_base/$z_hbase/bin/stop-hbase.sh
$z_base/$z_zookeeper/bin/zkServer.sh stop

pkill -f HiveServer2
pkill -f metastore
sleep 30
echo " done..."
