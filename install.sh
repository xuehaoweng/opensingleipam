#!/bin/bash

# abort on errors
set -e

port="$1"

# 安装docker
if ! [ -x "$(command -v docker)" ]; then
  echo '检测到 Docker 尚未安装，正在尝试安装 Docker ...'

  if [ -x "$(command -v yum)" ]; then
    sudo yum install -y python3-pip yum-utils device-mapper-persistent-data lvm2
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    yum list docker-ce --showduplicates | sort -r
    sudo yum install docker-ce
  else
    sudo apt-get update
    sudo dpkg --configure -a
    sudo apt-get install python3-pip apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install docker-ce
  fi

  # 启动docker和开机自启动
  sudo systemctl start docker
  sudo systemctl enable docker
fi


 # 安装docker-compose
if ! [ -x "$(command -v docker-compose)" ]; then
  echo '检测到 Docker-Compose 尚未安装，正在尝试安装 Docker-Compose ...'
  if ! [ -x "$(command -v pip3)" ]; then
      curl -L https://github.com/docker/compose/releases/download/1.25.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
      chmod +x /usr/local/bin/docker-compose
  else
      pip3 install --upgrade pip
      pip3 install docker-compose
  fi
fi


 # 开始安装 ipam
if [ -x "$(command -v docker)" -a -x "$(command -v docker-compose)" ]; then
  docker version
  docker-compose -version

  # 安装ipam-获取ipam的compose
#  if [ ! -f "docker-compose.yml" ];then
#    wget *****docker-compose.yml
#  fi
#
#  if [[ "$port" != "" ]]; then
#    perl -pi -e "s/8080:8080/$port:8080/g" docker-compose.yml
#  fi
# 创建docker_netaxe网络
docker network inspect docker_netaxe
if [ $? -ne 0 ]; then
    docker network create  --subnet=1.1.38.0/24 \
    --ip-range=1.1.38.0/24 \
    --gateway=1.1.38.254 \
    docker_netaxe
fi

  if [ ! -f "/etc/docker/daemon.json" ];then
    sudo mkdir -p /etc/docker
    echo -E '{"registry-mirrors": ["https://kn77wnbv.mirror.aliyuncs.com"]}' > /etc/docker/daemon.json
    sudo systemctl daemon-reload
    sudo systemctl restart docker
  fi

  docker-compose build && docker-compose up -d

else

  if ! [ -x "$(command -v docker)" ]; then
    echo 'Docker 安装失败，请检测您当前的环境（或网络）是否正常。'
  fi


  if ! [ -x "$(command -v docker-compose)" ]; then
    echo 'Docker-Compose 安装失败，请检测您当前的环境（或网络）是否正常。'
  fi

fi

echo " IPAM 组件单应用已经启动完毕,请打开ip:9005端口进行前端验证"

#rm -f install.sh