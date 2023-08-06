import os
import os.path as osp
import traceback
from collections import OrderedDict
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from icecream import ic
from loguru import logger

from . import utils

app = Flask(__name__, template_folder="./assets", static_folder="./assets", static_url_path="")
app.config['JSON_AS_ASCII'] = False
cors = CORS(app)

upload_dir = "upload/"
savepath = "result.csv"
# for progress
total = 0

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/test')
def test():
    return jsonify({"message": "this is test!"})

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    ic(file)
    save_dir = Path(upload_dir)
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = f"{save_dir}/{file.filename}"
    file.save(save_path)
    return jsonify({"message": "upload result test"})

@app.route('/search', methods=['POST', 'GET'])
async def search():
    try:
        params = request.get_json(force=True)
        ic(params)
        if os.path.exists(savepath):
            os.remove(savepath)
        if params['mode'] == '1': # 单个查询
            data1, data2 = [], []
            if "1" in params['ranges']:
                data1 = utils.searchInCCF(params['query'])
            if "2" in params['ranges']:
                data2 = await utils.searchInLetpub(params['query'], headless=params['headless'])
            data = {
                "ccf": data1,
                "letpub": data2,
            }
            ic(data)
            res = {"status": "ok", "data": data}
        elif params['mode'] == '2': # 批量查询
            data1, data2 = [], []
            field_name = params['field_name'].strip()
            query_list = []
            for file in params['fileList']:
                path = osp.join(upload_dir, file['name'])
                ic(path)
                ext = osp.splitext(path)[1]
                if ext == ".csv":
                    df = pd.read_csv(path)
                elif ext == ".xlsx":
                    df = pd.read_excel(path)
                elif ext == ".txt":
                    with open(path, 'r') as f:
                        lines = f.readlines()
                    df = pd.DataFrame({"name": lines})
                    field_name = "name"
                else:
                    return jsonify({"status": 'error', "message": f"暂不支持{ext}格式文件！"})
                if field_name not in df.columns:
                    return jsonify({"status": 'error', "message": f"没有找到提供的字段名：'{field_name}'！"})
                df = df.dropna(subset=[field_name])
                df = df.drop_duplicates(subset=[field_name])
                temp_list = df[field_name].tolist()
                query_list.extend(temp_list)
            d = OrderedDict()
            for i in query_list:
                d[i]  = True
            query_list =list(d.keys())
            global total
            total = len(query_list)
            ic(total)
            ic(query_list)
            if "1" in params['ranges']:
                data1 = utils.searchInCCFBatch(query_list)
            if "2" in params['ranges']:
                data2 = await utils.searchInLetpubBatch(query_list, savepath, headless=params['headless'], gap=params['gap'])
            res = {
                "status": "ok", "data": {
                    'ccf': data1,
                    'letpub': data2,
                }
            }
        return jsonify(res)
    except:
        logger.error(traceback.format_exc())
        return jsonify({"status": 'error', "message": "服务器错误，请联系管理员！"})

@app.route("/progress", methods=["GET"])
def progress():
    global total
    if not os.path.exists(savepath):
        return jsonify({"status": "ok", "data": [0, total]})
    with open(savepath, "r", encoding="utf-8") as f:
        n = len(f.readlines())
    return jsonify({"status": "ok", "data": [n, total]})

@app.route('/ccf_filter', methods=['POST', 'GET'])
def ccf_filter():
    params = request.get_json(force=True)
    ic(params)
    category = params['category'] if params['category'] != ["all"] else ['journal', 'cn_journal', 'conference']
    level = params['level'] if params['level'] != ["all"] else ['A', 'B', 'C']
    domain = params['domain'] if params['domain'] != ["0"] else ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','10']
    publisher = params['publisher'] if params['publisher'] != ["all"] else ['Springer', 'IEEE', 'ACM', 'Elsevier', 'other']
    data = utils.ccf_filter(category=category, level=level, domain=domain, publisher=publisher)
    if data is not None:
        res = {"status": "ok", "data": data}
    else:
        res = {"status": "error", "message": "服务器错误！"}
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
