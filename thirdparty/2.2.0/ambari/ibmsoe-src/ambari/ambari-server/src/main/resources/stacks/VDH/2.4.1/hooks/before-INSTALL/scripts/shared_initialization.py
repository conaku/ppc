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

"""

import os

from resource_management import *

def setup_users():
  """
  Creates users before cluster installation
  """
  import params
  
  for group in params.group_list:
    Group(group,
        ignore_failures = params.ignore_groupsusers_create
    )
    
  for user in params.user_list:
    User(user,
        gid = params.user_to_gid_dict[user],
        groups = params.user_to_groups_dict[user],
        ignore_failures = params.ignore_groupsusers_create       
    )
           
  set_uid(params.smoke_user, params.smoke_user_dirs)

  if params.has_hbase_masters:
    set_uid(params.hbase_user, params.hbase_user_dirs)

def set_uid(user, user_dirs):
  """
  user_dirs - comma separated directories
  """
  import params

  File(format("{tmp_dir}/changeUid.sh"),
       content=StaticFile("changeToSecureUid.sh"),
       mode=0555)
  Execute(format("{tmp_dir}/changeUid.sh {user} {user_dirs} 2>/dev/null"),
          not_if = format("test $(id -u {user}) -gt 1000"))
  
def setup_java():
  """
  Installs jdk using specific params, that comes from ambari-server
  """
  import params

  return
  jdk_curl_target = format("{artifact_dir}/{jdk_name}")
  java_dir = os.path.dirname(params.java_home)
  java_exec = format("{java_home}/bin/java")

  if not params.jdk_name:
    return

  environment = {
    "no_proxy": format("{ambari_server_hostname}")
  }

  Execute(format("mkdir -p {artifact_dir} ; \
  curl -kf -x \"\" \
  --retry 10 {jdk_location}/{jdk_name} -o {jdk_curl_target}"),
          path = ["/bin","/usr/bin/"],
          not_if = format("test -e {java_exec}"),
          environment = environment)

  if params.jdk_name.endswith(".bin"):
    install_cmd = format("mkdir -p {java_dir} ; chmod +x {jdk_curl_target}; cd {java_dir} ; echo A | {jdk_curl_target} -noregister > /dev/null 2>&1")
  elif params.jdk_name.endswith(".gz"):
    install_cmd = format("mkdir -p {java_dir} ; cd {java_dir} ; tar -xf {jdk_curl_target} > /dev/null 2>&1")

  Execute(install_cmd,
          path = ["/bin","/usr/bin/"],
          not_if = format("test -e {java_exec}")
  )

def install_packages():
  Package(['unzip', 'curl'])
