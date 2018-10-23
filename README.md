# ops-system
ops system

Quick start
===========

> You need a mysql instance running locally or remotely to connect. 
>
> ops runs on Python 3.7
>

1. Get ops
```bash
# git clone https://github.com/spark8103/ops-system.git
# cd ops-system
# python3 -m venv venv
# source venv/bin/activate
(venv) # pip install -r requirements.txt
```

2. Edit .env
Create uuid
```shell
python3 -c "import uuid; print(uuid.uuid4().hex)"
```

vim .env
```vim
SECRET_KEY=hdQj5yE6ywaSQKC8FucEZvM9Xanypgryw
DATABASE_URL=mysql+pymysql://ops:<db-password>@localhost:3306/ops
OPS_ADMIN=admin
```

3. Edit .flaskenv
vim .flaskenv
```vim
FLASK_APP=ops-system
#FLASK_ENV=development
FLASK_ENV=production
```

3. Setting Mysql 
```bash
yum install mysql mysql-devel
docker run -d --restart=always --name mysql -v /home/mysql:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -e TZ="Asia/Shanghai" mysql:5.6.30

mysql -uroot -p123456 -h localhost
mysql> CREATE DATABASE IF NOT EXISTS ops COLLATE utf8_general_ci;  
mysql> GRANT all privileges on ops.* to ops@'%' identified by 'ops12345678';
mysql> flush privileges;

# cat ops/settings.py
```

4. Run
```bash
$ flask db init
$ flask db
$ flask db upgrade
$ flask run -h 0.0.0.0
```

5. Create admin
```bash
$ flask shell
>>> from flask_security.utils import hash_password
>>> r = Role(name='admin')
>>> db.session.add(r)
>>> u = User(email='admin@admin.com', password=hash_password('admin123'), roles=[r])
>>> db.session.add(u)
>>> db.session.commit()
```

6. Create test user db
```bash
$ flask shell
>>> import range, string
>>> from flask_security.utils import hash_password
>>> r = Role(name='user')
>>> db.session.add(r)
>>> db.session.commit(r)
>>>
>>> r = Role.query.get(1)
>>> for i in [ "%s@tt.com" % ''.join(random.choices(string.ascii_letters + string.digits, k=8)) for i in range(200) ]:
>>>     db.session.add(User(email=i,password=hash_password(i), roles=[r]))
>>>     db.session.commit()
```

## License
This project is licensed under the [MIT license](https://opensource.org/licenses/MIT).
