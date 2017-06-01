# sudo python3 /home/ubuntu/www/tamkeen/app/manage.py runserver 0.0.0.0:80 > /dev/null 2>&1 &
sudo systemctl start nginx

sudo kill -9 $(sudo lsof -t -i:8003)
cd /home/ubuntu/www/tamkeen/app && uwsgi --socket :8003 --module tamkeen.wsgi > /dev/null 2>&1 &
