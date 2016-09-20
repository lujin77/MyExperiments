#!/usr/bin/python
# -*- coding:utf-8 -*-

import subprocess

config = {

  "hadoop" : {
    "path" : "/usr/local/Cellar/hadoop/2.7.2/libexec",
    "start_cmd" : "sh sbin/start-all.sh && sh sbin/mr-jobhistory-daemon.sh start historyserver",
    "stop_cmd" : "sh sbin/stop-all.sh && sh sbin/mr-jobhistory-daemon.sh stop historyserver"
  },

  "spark" : {
    "path" : "/usr/local/Cellar/apache-spark/2.0.0/libexec",
    "start_cmd" : "sh sbin/start-all.sh",
    "stop_cmd" : "sh sbin/stop-all.sh"
  },

  "zookeeper" : {
    "path" : "/usr/local/Cellar/kafka/0.10.0.1/libexec",
    "start_cmd" : "sh bin/zookeeper-server-start.sh config/zookeeper.properties &",
    "stop_cmd" : "sh bin/zookeeper-server-stop.sh"
  },

  "kafka" : {
    "path" : "/usr/local/Cellar/kafka/0.10.0.1/libexec",
    "start_cmd" : "sh bin/kafka-server-start.sh config/server.properties &",
    "stop_cmd" : "sh bin/kafka-server-stop.sh"
  },

  "ALL" : {
    "path" : "",
    "start_cmd" : "",
    "stop_cmd" : ""
  }
}

def call_shell(service, opt):
  if service == "ALL":
    for info in config:
      if info != "ALL":
        #print "[TRACE] starting {service_name} ...".format(service_name=info)
        service_conf = config[info]
        str_cmd = "cd {path} && {opt}".format(path=service_conf["path"], opt=service_conf[opt + "_cmd"])
        print "[TRACE] -> " + str_cmd
        retcode = subprocess.call(str_cmd, shell=True)

  else:
    #print "[TRACE] starting {service_name} ...".format(service_name=service)
    service_conf = config[service]
    str_cmd = "cd {path} && {opt}".format(path=service_conf["path"], opt=service_conf[opt + "_cmd"])
    print "[TRACE] -> " + str_cmd
    retcode = subprocess.call(str_cmd, shell=True)

if __name__ == "__main__":

  # 提示信息
  cmd_list = []
  print "[NOTICE] install component as follow:"
  for i, info in enumerate(config):
    print "{index}\t{name}".format(index=i, name=info)
    cmd_list.append(info)

  # 入参获取及检查
  opt = ""
  index = 0
  while True:

    cmd = raw_input("\n[INFO] input start/stop N: ")

    if cmd.find(' ') < 1:
      print "[ERROR] input format is wrong! please input: start/stop [number]"
      continue
    segs = cmd.split(' ')
    opt = segs[0].strip()

    if not str.isdigit(segs[1]):
      print "[ERROR] input choose index is not a number! please input: start/stop [number]"
      continue
    else:
      index = int(segs[1])

    if opt not in ["start", "stop"] :
      print "[ERROR] input operation is wrong! please input: start/stop [number]"
      continue

    if index < 0 or index >= len(cmd_list):
      print "[ERROR] input choose index is wrong! please input between 0 and {upper_bound}".format(upper_bound=(len(cmd_list)-1))
      continue

    # 满足要求，退出循环执行命令
    break

  # 命令执行
  call_shell(cmd_list[index], opt)

  print "[NOTICE] all is done"
