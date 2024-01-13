import json
import logging
from flask import Flask, request, jsonify
from datetime import date, datetime
import pymysql
from flask_cors import CORS

# 连接 MySQL 数据库
db = pymysql.connect(host="localhost", user="root", password="123456",
                     database="ocr")
cursor = db.cursor()

app = Flask(__name__)
CORS(app)

from datetime import date, datetime


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


@app.route("/ocrData", methods=["GET"])
def get_ocr_data():
    sql = 'SELECT * FROM ocr_result_2;'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return jsonify(results)



if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=8888)
