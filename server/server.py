from flask import Flask
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import os
from AutoGuide_version_2 import *
app= Flask (__name__)

@app.route('/image',methods=['GET','POST'])


def upload_image():
    if request.method == 'POST':
        print(request.files)
        print (request.files['image'])
        f=request.files['image']
        testPath='Tests'
        savePath="Tests\\uploaded\\"+secure_filename(f.filename)
        n_clusters=100
        f.save(savePath)
        predictedName=testingMain(n_clusters,testPath)
        deletepath=testPath+'\\uploaded'+'\\*'
        for each in glob(deletepath):
            os.remove(each)
        # os.system('python AutoGuide_version_2.py {}'.format(secure_filename(f.filename)))
        return jsonify({"name":predictedName})


    if request.method =='GET':
        return jsonify({"image":"Not yet"})







if __name__ == '__main_':
    app.run(debug=True)    