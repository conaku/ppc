"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

from resource_management import *

# server configurations
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

#RPM versioning support
rpm_version = default("/configurations/hadoop-env/rpm_version", None)

#hadoop params
if rpm_version is not None:
  hadoop_conf_dir = format("/usr/hdp/{rpm_version}/etc/hadoop/conf")
  hadoop_bin_dir = format("/usr/hdp/{rpm_version}/hadoop/bin")
  hadoop_home = format('/usr/hdp/{rpm_version}/hadoop')
  pig_conf_dir = format('/usr/hdp/{rpm_version}/etc/pig/conf')
  pig_bin_dir = format('/usr/hdp/{rpm_version}/pig/bin')
else:
  hadoop_conf_dir = "/opt/vse/hadoop/etc/hadoop"
  hadoop_bin_dir = "/opt/vse/hadoop/bin"
  hadoop_home = '/opt/vse/hadoop'
  pig_conf_dir = "/opt/vse/pig/conf"
  pig_bin_dir = "/opt/vse/pig/bin"

hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
smokeuser = config['configurations']['cluster-env']['smokeuser']
user_group = config['configurations']['cluster-env']['user_group']
security_enabled = config['configurations']['cluster-env']['security_enabled']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
kinit_path_local = functions.get_kinit_path(["/usr/bin", "/usr/kerberos/bin", "/usr/sbin"])
pig_env_sh_template = config['configurations']['pig-env']['content']

# not supporting 32 bit jdk.
java64_home = config['hostLevelParams']['java_home']

pig_properties = config['configurations']['pig-properties']['content']

log4j_props = config['configurations']['pig-log4j']['content']