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


