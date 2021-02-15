from pdf2image import convert_from_path
import os
import zipfile
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
app = Flask(__name__)

@app.route('/')
def convert_image():
    #print("Hello World")
    return render_template('convert.html')


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        f = request.files['file']
        name = f.filename
        f.save(name)
        image = convert_from_path(name)
        for i in range(len(image)):
            image[i].save('upload/' + str(i) + '.jpeg')
    #!zip upload.rar upload
    zipdir = zipfile.ZipFile('download.zip', 'w', compression=zipfile.ZIP_STORED)
    for root, dir, files in os.walk('upload/'):
        for file in files:
            zipdir.write('upload/'+file)
    zipdir.close()

    for root, dir, files in os.walk('upload/'):
        for file in files:
            os.remove('upload/'+file)

    os.remove(name)

    return send_file('download.zip', mimetype='zip')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=8080)

