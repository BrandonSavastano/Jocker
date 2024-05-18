import os
from sys import argv
from sys import stdout
from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.msfconsole import MsfRpcConsole
import time
import re

# Get the list of CVEs from STDIN
CVEs = argv[1:]

# These variables will hold the output of the console after command executions
global console_buffer
console_buffer = list()
global console_busy
console_busy = False


# The callback function that sets the above variables after client.execute 
def read_console(console_data):
    global console_buffer
    sigdata = console_data['data'].rstrip().split('\n')
    for line in sigdata:
        console_buffer.append(line)
    global console_busy
    console_busy = False

# Clears the console
def clear_console():
    global console_buffer
    console_buffer = list()

# 创建客户端对象
client = MsfRpcClient(host="127.0.0.1", port=55553, username="hacksh1337", password="hacksh1337", ssl=False)

# 登录Metasploit服务
client.login("hacksh1337", "hacksh1337")
    
# 创建用于访问MSF控制台的对象
console = MsfRpcConsole(client, cb=read_console)

# 查找与每个CVE相关的所有msfmodules
def search_for_cve(cve):
    clear_console()
    global console_busy
    console_busy = True
    console.execute("search cve:{}".format(cve))
    while console_busy:
        time.sleep(1)
    return console_buffer

# 清理搜索结果，仅包含漏洞利用的路径
def clean_cve_search(search_result):
    nl = list()
    for i in search_result:
        if "exploit/" in i and not "Interact with a module by name or index." in i:
            nl.append(i.split()[1])
    return nl

# 搜索每个CVE并将其记录在列表中
cve_data = list()
for i in CVEs:
    cve_data += clean_cve_search(search_for_cve(i))

# 输出CVE数据以供 hack.sh 脚本从 STDIO 中获取
for i in cve_data:
    stdout.write(i + "\n")
stdout.flush()

# 退出程序
os._exit(0)

