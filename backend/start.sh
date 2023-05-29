#cd /app
#pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
#pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
web(){
    mkdir -p /app/logs/celery_logs
    mkdir -p /var/log/supervisor
    rm -rf /app/logs/celery_logs/w*.log
    rm -rf *.pid
    echo 'uwsgi done'
    supervisord -n -c /app/supervisord_prd.conf
}
#default(){
#    sleep 10
#    celery -A IpamV1 worker -Q default -c 10 -l info -n default
#}
#ipam(){
#    sleep 10
#    celery -A IpamV1 worker -Q ipam -c 10 -l info -n ipam
#}


case "$1" in
web)
web
;;
*)
echo "Usage: $1 {web}"
;;
esac
echo "start running!"