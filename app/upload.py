from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import time
from datetime import timedelta
import model
from PIL import Image

import numpy as np
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


import logging


log = logging.getLogger()

log.setLevel('INFO')

handler = logging.StreamHandler()

handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))

log.addHandler(handler)

#from cassandra.cluster import Cluster

#from cassandra import ConsistencyLevel

from cassandra.cluster import Cluster

from cassandra.query import SimpleStatement


KEYSPACE = "mykeyspace"






def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})



        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        #upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        upload_path = os.path.join(basepath, 'static/images','test.png')
        f.save(upload_path)
        print(upload_path)

        Img = Image.open(upload_path)
        res,predictions = model.cloth_predict(Img)
        #model.plot_image(predictions,Img)
        t = datetime.now()
        Time = str(t)
        name = f.filename
        cluster = Cluster(contact_points=['127.0.0.1'], port=9042)

        session = cluster.connect()
        session.set_keyspace(KEYSPACE)
        try:

            session.execute("INSERT INTO pictable (filename,res,time)values(%s,%s,%s);",(name,res,Time))



        except Exception as e:

            log.error("Unable to add data")

            log.error(e)
        rows = session.execute('select * from pictable;')
        for row in rows:
            print(row)

        return render_template('upload_ok.html', userinput=res, val1=time.time())

    return render_template('upload.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(debug=True)

