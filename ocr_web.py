import json
import logging
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import pymysql


def init_log():
    # 设置打印到控制台的格式和等级
    logging.basicConfig(format='%(asctime)s %(filename)s %(levelname)s %(message)s', datefmt='%a %d %b %Y %H:%M:%S',
                        level=logging.INFO)
    # 设置输出到的文件和编码
    file_handler = logging.FileHandler("ocr.log", encoding="utf-8")
    # 设置输出等级
    file_handler.setLevel(logging.INFO)
    # 设置输出到文件的日志格式
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(filename)s %(levelname)s %(message)s'))
    logger = logging.getLogger()
    logger.handlers.append(file_handler)


init_log()

# 连接 MySQL 数据库
db = pymysql.connect(host="@localhost", user="root", password="123456",
                     database="ocr")
cursor = db.cursor()

app = Flask(__name__)
ocr = PaddleOCR(usr_angle_cls=True, use_gpu=False)

@app.route("/ocr", methods=["POST"])
def learn_post_method():
    try:
        img_path = request.json.get("imgPath")
        logging.info("ocr imgPath : %s", img_path)
        ocr_result = ocr.ocr(img_path)

        # 将 OCR 结果存储到 MySQL 数据库
        save_to_mysql(img_path, ocr_result)

        return jsonify({"code": 0, "msg": "ok", "data": ocr_result}), 200
    except Exception as e:
        logging.error("ocr error: %s", str(e))
        ocr_result = {"code": -1, "msg": str(e)}
    return jsonify(ocr_result), 200

@app.route("/ocrData", methods=["GET"])
def get_ocr_data():
    sql = 'SELECT * FROM ocr_result_2;'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    return jsonify(results)

def save_to_mysql(image_path, ocr_result):
    result_text = json.dumps(ocr_result, ensure_ascii=False)

    # 将数据插入到数据库表中
    insert_query = f"INSERT INTO ocr_results (image_path, result) VALUES ('{image_path}', '{result_text}')"
    cursor.execute(insert_query)
    db.commit()

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', debug=True, port=8888)