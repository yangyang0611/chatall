
## Environments
>OS: Ubuntu 22.04 server
* Install virtualenv and requirements
```
sudo apt-get install -y libmariadb-dev virtualenv
```

* Create virtualenv 
```
virtualenv env/
source env/bin/activate

# in virtualenv
pip3 install -r requirements.txt
```

## Start Mariadb
>In this Lab, we use another server as DB 
```
sudo docker run --name mariadb -e MYSQL_ROOT_PASSWORD=demo -p 3306:3306 -d mariadb:10.5
```
* Create DB
```
# in container
mysql -p
MariaDB [(none)]> CREATE DATABASE app;
```

## Setup application
### Setup uWSGI as system service
>Reference to conf/
```
sudo vim /etc/system/systemd/lab1-demo.service
sudo chgrp www-data /home/{user}
sudo systemctl start lab1-demo
sudo systemctl enable lab1-demo
```

### Setup NGINX as proxy
>Install NGINX first: 
```
sudo apt install nginx -y
```

```
# Reference to conf/lab1
sudo vim /etc/nginx/sites-available/lab1

# soft link to sites-enabled
sudo ln -s /etc/nginx/sites-available/lab1 /etc/nginx/sites-enabled
sudo unlink /etc/nginx/sites-enabled/default

# test syntax
sudo nginx -t

# restart nginx
sudo systemctl restart nginx
```

## Interact
### API Doc
>You can visit api through http://www.icsdtg2.nycu:5000/<api> after configure host resolve on client manually.
* Welcome message
```
<url>:5000/
```
* init db table
```
<url>:5000/init 
```

* visitor counter
```
<url>:5000/api/v1/hi
```

* Query table data
```
<url>:5000/data
```

### Support
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-22-04
