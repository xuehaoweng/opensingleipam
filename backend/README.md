# NETAXE开源
- 基础模型和字段定义
- 获取子网树结构
- 根据子网获取地址使用详情
- 定制化

## 定制化admin 后台

 1.后台树结构
 2.后台矩阵展示使用状况
 3.后台运行定时任务
 
## 自动化任务

 1. 地址回收 回收IPAM中最后在线时间大于90天的IP地址，将其置为自定义空闲 细分多个组别 仅回收大于90天的地址√
 2. 定时修改特定网段描述
 3. 地址信息更新  IPAM地址全网更新main  根据现网中mongo库所有IP地址 Total_ip_list来进行地址更新 √
 
 ## 前端适配、功能验证

 1. ipv4、ipv6 地址展示适配

 2. 功能验证:地址分配、地址批量分配、地址回收、ipv6地址动态滚动刷新
 
