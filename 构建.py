# -*- coding: utf-8 -*-

import requests
from ipaddress import IPv4Network
import os

地方 = {
    "440300": "深圳", 
    "350600": "漳州"
}

运营商 = {
    "chinanet": "电信",
    "unicom": "联通", 
    "cmcc": "移动"
}

def 获取前缀(url, name):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.encode('utf-8').decode('utf-8').strip().split('\n')
    else:
        print(f"{name}获取失败。")
        exit()

def 计算子网(前缀一, 前缀二):
    子网前缀 = []
    for 前缀甲 in 前缀一:
        网段甲 = IPv4Network(前缀甲)
        for 前缀乙 in 前缀二:
            网段乙 = IPv4Network(前缀乙)
            if 网段甲.overlaps(网段乙):
                intersection = 网段甲.subnet_of(网段乙)
                if intersection == True:
                    子网前缀.append(str(网段甲))
    return 子网前缀

def 创建目录(目录):
    if not os.path.exists(目录):
        os.makedirs(目录)

# 获取当前文件所在目录
当前路径 = os.path.dirname(os.path.abspath(__file__))

# 创建存储结果的目录
创建目录(os.path.join(当前路径, "地方与运营商"))
创建目录(os.path.join(当前路径, "运营商与地方"))
创建目录(os.path.join(当前路径, "地方"))
创建目录(os.path.join(当前路径, "运营商"))

# 存储地方和运营商的前缀
地方前缀 = {}
运营商前缀 = {}

for 城市代码, 城市名称 in 地方.items():
    城市_IPv4_前缀_资源定位 = f"https://quantil.jsdelivr.net/gh/metowolf/iplist@master/data/cncity/{城市代码}.txt"
    城市_IPv4_前缀 = 获取前缀(城市_IPv4_前缀_资源定位, f'{城市名称} IPv4 前缀')
    地方前缀[城市名称] = 城市_IPv4_前缀

    for 运营代码, 运营名称 in 运营商.items():
        运营_IPv4_前缀_资源定位 = f"https://quantil.jsdelivr.net/gh/JwietPuj-Drin/china-operator-ip@ip-lists/{运营代码}4.txt"
        运营_IPv4_前缀 = 获取前缀(运营_IPv4_前缀_资源定位, f'{城市名称}{运营名称} IPv4 前缀')
        
        if 运营名称 not in 运营商前缀:
            运营商前缀[运营名称] = 运营_IPv4_前缀

        子网前缀 = 计算子网(城市_IPv4_前缀, 运营_IPv4_前缀)
        IPv4_前缀 = '\n'.join(子网前缀)
        
        with open(os.path.join(当前路径, "地方与运营商", f"{城市名称}{运营名称}_IPv4_前缀.txt"), "w", encoding='utf-8', newline='') as file:
            file.write(IPv4_前缀)
        print(f"{城市名称}与{运营名称}的 IPv4 前缀交集子网已生成为 `./地方与运营商/{城市名称}{运营名称}_IPv4_前缀.txt`")

        with open(os.path.join(当前路径, "运营商与地方", f"{运营名称}{城市名称}_IPv4_前缀.txt"), "w", encoding='utf-8', newline='') as file:
            file.write(IPv4_前缀)
        print(f"{运营名称}与{城市名称}的 IPv4 前缀交集子网已生成为 `./运营商与地方/{运营名称}{城市名称}_IPv4_前缀.txt`")

# 生成地方前缀文件
for 城市名称, 城市前缀 in 地方前缀.items():
    with open(os.path.join(当前路径, "地方", f"{城市名称}_IPv4_前缀.txt"), "w", encoding='utf-8', newline='') as file:
        file.write('\n'.join(城市前缀))
    print(f"{城市名称}的 IPv4 前缀已生成为 `./地方/{城市名称}_IPv4_前缀.txt`")

# 生成运营商前缀文件  
for 运营名称, 运营前缀 in 运营商前缀.items():
    with open(os.path.join(当前路径, "运营商", f"{运营名称}_IPv4_前缀.txt"), "w", encoding='utf-8', newline='') as file:
        file.write('\n'.join(运营前缀))
    print(f"{运营名称}的 IPv4 前缀已生成为 `./运营商/{运营名称}_IPv4_前缀.txt`")

# 生成总前缀文件
总前缀 = []
for 城市前缀 in 地方前缀.values():
    总前缀.extend(城市前缀)
for 运营前缀 in 运营商前缀.values():   
    总前缀.extend(运营前缀)
总前缀 = list(set(总前缀))  # 去重

with open(os.path.join(当前路径, "虞夏_IPv4_前缀.txt"), "w", encoding='utf-8', newline='') as file:
    file.write('\n'.join(总前缀))
print(f"总 IPv4 前缀已生成为 `./虞夏_IPv4_前缀.txt`")
