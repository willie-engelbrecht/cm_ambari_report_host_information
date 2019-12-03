# Introduction
This repo contains a Python scrip that will help you pull host information from your Ambari or Cloudera Managed cluster. This aids in quick and easy information gathering on the hardware profile of each node in your cluster for capacity planning. 

The information will be written out as CSV, and will contain:
* Cluster name
* Version
* Hostname
* OSType
* CPU Count
* MemBytes
* MemMB
* DiskCount
* DiskStorageBytes
* DiskStorageMB
* Host Components/Roles

## Prerequistes
The python scripts has two requirements:
* Python 3 must be installed
* BeautifulSoup4 must be installed through pip3

## Usage
Whether you run Ambari (with or without KNOX) or Cloudera Manager, the python script can accommodate both and will automatically detect the right API to use. 

There are three parameters to pass:
* -u admin_username
* -p admin_password
* -a url_to_Ambari/ClouderaManager

Optionally, you can also save the output to a file instead:
* -o filename_to_save.csv

An example of using Ambari with KNOX:
```
python3 query_ambari_cm.py -u admin -p admin-password1 -a https://X.X.X.X:8443/hdp-prod-dc1/dp-proxy/ambari/ -o output.csv
```

An example of using Cloudera Manager:
```
python3 query_ambari_cm.py -u admin -p admin-password1 -a http://X.X.X.X:7180 -o output.csv
```

## Output
The python script will generate CSV output and print to screen from where you can copy-paste to a file or Excel spreadsheet. You can also save the output to a file instead by using the -o flag. 

```
ClusterName,Version,Hostname,OSType,CPUCount,TotalMemBytes,TotalMemMB,DiskCount,TotalDiskStorage,TotalDiskStorageMB,HostComponents
hdp-prod-dc1,HDP 3.1,ip-10-0-1-195.eu-central-1.compute.internal,redhat7,8,31961352,31212.0,1,52416492,51188.0,APP_TIMELINE_SERVER;ATLAS_CLIENT;BEACON_SERVER;DATANODE;DATA_ANALYTICS_STUDIO_EVENT_PROCESSOR;DATA_ANALYTICS_STUDIO_WEBAPP;DP_PROFILER_AGENT;DRUID_BROKER;DRUID_COORDINATOR;DRUID_OVERLORD;DRUID_ROUTER;HBASE_CLIENT;HDFS_CLIENT;HISTORYSERVER;HIVE_CLIENT;HIVE_METASTORE;HIVE_SERVER;HIVE_SERVER_INTERACTIVE;INFRA_SOLR_CLIENT;KNOX_GATEWAY;LOGSEARCH_LOGFEEDER;MAPREDUCE2_CLIENT;NIFI_REGISTRY_MASTER;RANGER_ADMIN;RANGER_TAGSYNC;RANGER_USERSYNC;REGISTRY_SERVER;SECONDARY_NAMENODE;SPARK2_CLIENT;STREAMSMSGMGR;TEZ_CLIENT;YARN_CLIENT;ZOOKEEPER_CLIENT
hdp-prod-dc1,HDP 3.1,ip-10-0-1-234.eu-central-1.compute.internal,redhat7,8,32305424,31548.0,1,52416492,51188.0,ATLAS_CLIENT;DATANODE;HBASE_CLIENT;HBASE_REGIONSERVER;HDFS_CLIENT;HIVE_CLIENT;KAFKA_BROKER;LOGSEARCH_LOGFEEDER;MAPREDUCE2_CLIENT;METRICS_MONITOR;NIFI_MASTER;NODEMANAGER;SPARK2_CLIENT;TEZ_CLIENT;YARN_CLIENT;ZOOKEEPER_CLIENT;ZOOKEEPER_SERVER
hdp-prod-dc1,HDP 3.1,ip-10-0-1-56.eu-central-1.compute.internal,redhat7,8,31961360,31212.0,1,52416492,51188.0,ATLAS_CLIENT;ATLAS_SERVER;DATANODE;DRUID_HISTORICAL;DRUID_MIDDLEMANAGER;HBASE_CLIENT;HBASE_MASTER;HIVE_CLIENT;INFRA_SOLR;LIVY2_SERVER;LOGSEARCH_LOGFEEDER;LOGSEARCH_SERVER;MAPREDUCE2_CLIENT;METRICS_COLLECTOR;METRICS_GRAFANA;METRICS_MONITOR;NAMENODE;NIFI_CA;RESOURCEMANAGER;SPARK2_CLIENT;SPARK2_JOBHISTORYSERVER;SUPERSET;TEZ_CLIENT;ZOOKEEPER_CLIENT
hdp-prod-dc1,HDP 3.1,ip-10-0-1-79.eu-central-1.compute.internal,redhat7,8,31961360,31212.0,1,52416492,51188.0,ATLAS_CLIENT;DATANODE;HBASE_CLIENT;HBASE_REGIONSERVER;HDFS_CLIENT;HIVE_CLIENT;KAFKA_BROKER;LOGSEARCH_LOGFEEDER;MAPREDUCE2_CLIENT;METRICS_MONITOR;NIFI_MASTER;NODEMANAGER;SPARK2_CLIENT;TEZ_CLIENT;YARN_CLIENT;ZOOKEEPER_CLIENT;ZOOKEEPER_SERVER
hdp-prod-dc1,HDP 3.1,ip-10-0-1-82.eu-central-1.compute.internal,redhat7,8,31961360,31212.0,1,52416492,51188.0,ATLAS_CLIENT;DATANODE;HBASE_CLIENT;HBASE_REGIONSERVER;HDFS_CLIENT;HIVE_CLIENT;KAFKA_BROKER;LOGSEARCH_LOGFEEDER;MAPREDUCE2_CLIENT;METRICS_MONITOR;NIFI_MASTER;NODEMANAGER;SPARK2_CLIENT;TEZ_CLIENT;YARN_CLIENT;ZOOKEEPER_CLIENT;ZOOKEEPER_SERVER
```

If you paste it in Excel and format it by comma-delimited, you'll have something like:
![alt text](https://github.com/willie-engelbrecht/cm_ambari_report_host_information/raw/master/excel_output.JPG "Excel Output")
