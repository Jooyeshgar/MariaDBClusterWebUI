#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sébastien Reuiller"
import pymysql
import configparser
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def home():

    conf = configparser.RawConfigParser()
    conf.read('nodes.conf')

    nodes_item = conf.items("nodes")
    nodes = []
    for key, host in nodes_item:
        dict_wsrep = {}

        try:
            cnx = pymysql.connect(host=host, port=int(conf.get('access', 'port')), user=conf.get('access', 'user'), passwd=conf.get('access', 'pass'), db='mysql')
            with cnx.cursor() as cursor:
                cursor.execute("SELECT @@hostname as hostname;")
                dict_wsrep['hostname'] = cursor.fetchone()[0]

                cursor.execute("SHOW STATUS LIKE 'wsrep%';")
                res = cursor.fetchall()

                for row in res:
                    dict_wsrep[row[0]] = row[1]
            cnx.close()
        except:
            dict_wsrep['hostname'] = host
            dict_wsrep['wsrep_local_state'] = 0
            dict_wsrep['wsrep_local_state_comment'] = 'Error'

        nodes.append(dict_wsrep)

    return render_template('home.html', nodes=nodes)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

