from flask import Flask
from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
app= Flask (__name__)

@app.route('/image',methods=['GET','POST'])


def upload_image():
    if request.method == 'POST':
        print(request.files)
        print (request.files['image'])
        f=request.files['image']
        f.save(secure_filename(f.filename))
        
        return jsonify({"name":"Nefrtiti"})


    if request.method =='GET':
        return jsonify({"image":"Not yet"})







if __name__ == '__main_':
    app.run(debug=True)    