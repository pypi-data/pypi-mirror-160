from base import *


# a=cli.render('''
#    my name is {{name}}.
#    {%- for i in [1,2,3,4,5,6,7] %}
#     {{i}}
#    {%- endfor %}
# ''',{'name':"jqzhang"})
#
# # print(a)
#
#
# dsn='mysql://root:root@localhost:3306/ferry'
#
# conn=cli.get_mysql_connection(dsn)
# print(cli.mysql_query(conn,'show tables'))
# print(cli.mysql_query(conn,'select * from test'))



# conn=cli.get_sqlite_connection(":memory:")
#
# cli.sqlite_query(conn,'''
# CREATE TABLE COMPANY(
#    ID INT PRIMARY KEY     NOT NULL,
#    NAME           TEXT    NOT NULL,
#    AGE            INT     NOT NULL,
#    ADDRESS        CHAR(50),
#    SALARY         REAL
# );
# ''')

# i="insert into COMPANY(NAME,ID,AGE) values('jqzhang','1',30)"
# cli.sqlite_query(conn,i)
# i="insert into COMPANY(NAME,ID,AGE) values('hello','2',35)"
# cli.sqlite_query(conn,i)

# sql='''
# INSERT INTO COMPANY (`ID`,`NAME`,`AGE`,`ADDRESS`,`SALARY`)
# VALUES
# (1,'jqzhang',30,NULL,NULL),
# (2,'hello',35,NULL,NULL);'''
# cli.sqlite_query(conn,sql)
#
# rows=cli.sqlite_query(conn,'select * from COMPANY')
#
# print(cli.dict2sql('COMPANY',rows))
#
#
# dsn = os.environ.get("DSN", "mysql://root:root@127.0.0.1:3306/pjm_db")
#
# dsn='mysql://root:root@localhost:3306/ferry'
# conn=cli.get_mysql_connection(dsn)
# cli.dump_mysql_data(conn,"/tmp/ferry")
# cli.dump_mysql_ddl(conn,"/tmp/ferry")
#
# print(cli.get_dependencies())



# tpl='''
# <dl>
#     {% for key, value in d.items() %}
#     <dt>{{ key }}</dt>
#     <dd>{{ value }}</dd>
#     {% endfor %}
# </dl>
# '''
#
# d={'key1':'value1','key2':'value2'}
# print(cli.render(tpl,globals()))


# cli.example()
#
# req=cli.requests.get('https://www.baidu.com')
# print(req.content)

# print(cli.get_dependencies(True))

# html=cli.requests.get("https://www.baidu.com").content
# for i in cli.pq(html,'a','items'):
#     print(cli.pq(i,'a','text'))


# xml='''
# <note>
# <to>Tove</to>
# <from name="xxx">Jani</from>
# <heading>Reminder</heading>
# <body>Don't forget me this weekend!</body>
# </note>
# '''
#
# for i in cli.pq(xml,'from','items'):
#     print(i.attr('name'))



# cli.example()


# cli.get_redis()
#
# import dsnparse
#
# print(cli.parse_dsn(dsn))

# dsn='redis://localhost:63790/0'
# r=cli.get_redis(dsn)
# r.set('a','b')
# print(r.get('a'))

# import kafka

#

#
# def cc():
#     dsn="kafka://127.0.0.1:9092/test?group_id=2&bootstrap_servers=127.0.0.1:9092"
#     consumer=cli.get_kafka_consumer(dsn)
#     for m in consumer:
#         print(m)
# import threading
#
# c=threading.Thread(target=cc)
# c.setDaemon(True)
# c.start()
# #
# dsn="kafka://127.0.0.1:9092/?bootstrap_servers=127.0.0.1:9092"
#
# p=cli.get_kafka_producer(dsn)
# k=cli.kafka
#
# import time
# for i in range(1,1000):
#     p.send('test','xxx')
#     time.sleep(1)


