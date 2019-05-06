# # pylint: disable=no-member

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from AutoGuide_version_2 import *

# Init app
app = Flask(__name__)


@app.route('/image', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        print(request.files)
        print(request.files['image'])
        f = request.files['image']
        testPath = 'Tests'
        savePath = "Tests\\uploaded\\"+secure_filename(f.filename)
        n_clusters = 100
        f.save(savePath)
        predictedName = testingMain(n_clusters, testPath)
        deletepath = testPath+'\\uploaded'+'\\*'
        for each in glob(deletepath):
            os.remove(each)
        # os.system('python AutoGuide_version_2.py {}'.format(secure_filename(f.filename)))
        return jsonify({"name": predictedName})


@app.route('/image', methods=['GET'])
def test():
    return jsonify({"info": "Server is running"})


# Run Server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4200)
