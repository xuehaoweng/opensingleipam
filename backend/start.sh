#cd /home/ipam_backend
#pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
#pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

echo -e "yes" | python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate
web(){
    mkdir -p /home/ipam_backend/logs/celery_logs
    mkdir -p /var/log/supervisor
    rm -rf /home/ipam_backend/logs/celery_logs/w*.log
    rm -rf *.pid
    echo 'uwsgi done'
    supervisord -n -c /home/ipam_backend/supervisord_prd.conf
}
default(){
    sleep 10
    celery -A IpamV1 worker -Q default -c 10 -l info -n default
}
ipam(){
    sleep 10
    celery -A IpamV1 worker -Q ipam -c 10 -l info -n ipam
}


case "$1" in
web)
web
;;
default)
default
;;
ipam)
ipam
;;
*)
echo "Usage: $1 {web|default|ipam}"
;;
esac
echo "start running!"