<p align="center">
    <img src="readme/logo.png" alt="netaxe" />
</p>
<p align="center">
    <img src="https://img.shields.io/badge/Python-brightgreen.svg"/>
    <img src="https://img.shields.io/badge/Django-orange.svg"/>
    <img src="https://img.shields.io/badge/FastAPI-brightgreen.svg"/>
    <img src="https://img.shields.io/badge/Vue3-blue.svg"/>
    <img src="https://img.shields.io/badge/Vite-orange.svg"/>
    <img src="https://img.shields.io/badge/NaiveUI-blue.svg"/>
    <img src="https://img.shields.io/badge/license-Apache-green.svg"/>
    <a href="https://gitee.com/NetAxeClub" target="_blank">
        <img src="https://img.shields.io/badge/Author-NetAxeClub-orange.svg"/>
    </a>
</p>
<p align="center">
 <a target="_blank" href="https://netaxe.github.io">IPAM官方文档</a> |  <a target="_blank" href="http://47.99.86.164:32092">在线预览</a>
</p>

## 项目介绍

**专注网络自动化领域的整体架构解决方案**

[ NetAxe ]是一个网络自动化领域解决方案框架，通过微服务和微前端的方式构建的应用集合，主要有资源管理、配置管理、自动化、网络拓扑、地址定位、地址管理等等功能集合，同时各个微应用支持插件形式的能力集成，方便用户自行扩展。

## 组织地址

[NetAxeClub](https://gitee.com/NetAxeClub)

致力于网络自动化工具和平台开发

联系邮箱:netaxe@qun.mail.163.com

##  地址管理组件

![地址管理组件](https://cdn.staticaly.com/gh/xuehaoweng/netaxe-image@master/ipam.3vspimj3jf20.webp)

### 基本能力

- 地址分配
- 树结构展示子网
- 地址回收
- 子网段地址使用详情
- EXCEL导出
- IPAM操作日志记录


### IPAM Admin 后台

 1. 后台树结构
 2. 后台矩阵展示使用状况


### 自动化任务

 1. 自动地址回收
 2. 自动修改特定描述信息
 3. **地址探活检测更新**
 > 需结合CMDB应用,根据设备信息采集ARP记录,进行地址更新。


### 应用部署

>

```
Mysql数据库已经包含在一键部署脚本中


git clone https://gitee.com/NetAxeClub/IPAM.git

cp config/default.json config/config.json

修改config.json内的local_dev为true、mysql_host为"single-mysql-server"

指定file模式启动容器

docker compose --file single-docker-compose.yml build && docker compose --file single-docker-compose.yml down -v && docker compose --file single-docker-compose.yml up -d

```
