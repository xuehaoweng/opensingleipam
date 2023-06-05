# 地址管理组件IPAMTEST

## 基本能力

- 地址分配
- 树结构展示子网
- 地址回收
- 子网段地址使用详情
- EXCEL导出
- IPAM操作日志记录


## IPAM Admin 后台

 1. 后台树结构
 2. 后台矩阵展示使用状况


## 自动化任务

 1. 自动地址回收
 2. 自动修改特定描述信息
 3. **地址探活检测更新**
 > 需结合CMDB应用,根据设备信息采集ARP记录,进行地址更新。


## 应用部署

> 部署前置条件：Mysql数据库、Redis缓存配置
### 单应用部署
``` bash

1. 修改web/.env.production内的VITE_LOCAL_ROUTER 为 true

echo "VITE_LOCAL_ROUTER = true" > .env.production

2. 修改config/config.json

cp config/default.json config/config.json

local_dev:true

3. 修改nginx/vue_nginx.conf

sed -i 's/server_ip/your_server_ip/g' nginx/vue_nginx.conf


```

### 微服务注册

``` bash

1. 修改web/.env.production内的VITE_LOCAL_ROUTER 为 false

echo "VITE_LOCAL_ROUTER = false" > .env.production

2. 修改config/config.json

cp config/default.json config/config.json

local_dev:false

配置 apisix 和 nacos

3. 修改nginx/vue_nginx.conf

sed -i 's/server_ip:38005/apisix:9080/g' nginx/vue_nginx.conf


```


