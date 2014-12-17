#!/bin/bash
###########################################################
#
# Copyright (c) 2013, 2014 Veristorm Incorporated
#
###########################################################
#!/bin/bash

NNIPADDRESS=$1
JAVAHOME=$(echo $2 | awk '{gsub("/","\\/");print;}')
DBIPADDR=$3
DBPORT=$4

#configure hadoop
/opt/vse/sbin/_configure_hadoop.sh $NNIPADDRESS $JAVAHOME

source /opt/vse/sbin/.bashrc
#configure Hive
/opt/vse/sbin/_configure_hive.sh $NNIPADDRESS $JAVAHOME $DBIPADDR $DBPORT

#configure Hbase
/opt/vse/sbin/_configure_hbase.sh $NNIPADDRESS $JAVAHOME

#configure pig
/opt/vse/sbin/_configure_pig.sh $JAVAHOME "\/opt\/vse\/hadoop" "\/opt\/vse\/hadoop\/etc\/hadoop" "\/opt\/vse\/hbase" "\/opt\/vse\/hbase\/conf" "\/opt\/vse\/zoo" "\/opt\/vse\/pig" "\/opt\/vse\/pig\/conf" 

#configure sqoop
/opt/vse/sbin/_configure_sqoop.sh "\/opt\/vse\/hadoop" "\/opt\/vse\/hadoop" "\/opt\/vse\/hbase" "\/opt\/vse\/hive" "\/opt\/vse\/zoo" "\/opt\/vse\/sqoop" "\/opt\/vse\/sqoop\/conf" 

#configure flume with twitter
#sed -i "s/SED_NMIPADDRESS_FLUME/$NNIPADDRESS/g" /opt/vse/flume/conf/*.conf
#sed -i "s/SED_FLUME_HOME/\/opt\/vse\/flume/g" /opt/vse/flume/conf/*.sh
#configure hbase
#sed -i "s/SED_JAVA_HOME/$JAVAHOME/g" /opt/vse/hbase-0.96.0.2.0.6.0-76-hadoop2/conf/*.sh
#sed -i "s/SED_NMIPADDRESS_HBASE/$NNIPADDRESS/g" /opt/vse/hbase-0.96.0.2.0.6.0-76-hadoop2/conf/regionservers
#sed -i "s/SED_NMIPADDRESS_HBASE/$NNIPADDRESS/g" /opt/vse/hbase-0.96.0.2.0.6.0-76-hadoop2/conf/*.xml
#sed -i "s/SED_MASTERBINDADDRESS_HBASE/$NNIPADDRESS/g" /opt/vse/hbase-0.96.0.2.0.6.0-76-hadoop2/conf/*.xml
#sed -i "s/SED_ZOOKEEPERQUORUM_HBASE/$NNIPADDRESS/g" /opt/vse/hbase-0.96.0.2.0.6.0-76-hadoop2/conf/*.xml
#configure zookeeper
#sed -i "s/SED_JAVA_HOME/$JAVAHOME/g" /opt/vse/zookeeper-3.4.5.2.0.6.0-76/conf/*.sh
#sed -i "s/SED_NMIPADDRESS_HBASE/$NNIPADDRESS/g" /opt/vse/zookeeper-3.4.5.2.0.6.0-76/conf/regionservers
#sed -i "s/SED_NMIPADDRESS_HBASE/$NNIPADDRESS/g" /opt/vse/zookeeper-3.4.5.2.0.6.0-76/conf/*.xml
#sed -i "s/SED_MASTERBINDADDRESS_HBASE/$NNIPADDRESS/g" /opt/vse/zookeeper-3.4.5.2.0.6.0-76/conf/*.xml
#sed -i "s/SED_ZOOKEEPERQUORUM_HBASE/$NNIPADDRESS/g" /opt/vse/zookeeper-3.4.5.2.0.6.0-76/conf/*.xml
#sed -i "s/SED_ZKSERVERHOSTNAME/$NNIPADDRESS/g" /opt/vse/zookeeper-3.4.5.2.0.6.0-76/conf/zoo.cfg