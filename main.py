from flask import Flask, render_template, request
import gzip
import glob
import os

app = Flask(__name__)
app.config["FILE_UPLOADS"] = "/Users/arshad/Desktop/Huffman_Coding/uploads/"


global filename
global ftype

def compress_file(input_filename, output_filename):
    with open(input_filename, 'rt') as input_file:
        with gzip.open(output_filename, 'wt') as output_file:
            output_file.write(input_file.read())


def decompress_file(input_filename, output_filename):
    with gzip.open(input_filename, 'rt') as input_file:
        with open(output_filename, 'wt') as output_file:
            output_file.write(input_file.read())


@app.route("/")
def home():
    # Delete old files
    filelist = glob.glob('uploads/*')
    for f in filelist:
        os.remove(f)
    filelist = glob.glob('downloads/*')
    for f in filelist:
        os.remove(f)
    return render_template("home.html")


@app.route("/compress", methods=["GET", "POST"])
def compress():
    if request.method == 'GET':
        return render_template("compress.html", check=0)

    elif request.method == 'POST':
        up_file = request.files["file"]
        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
        
            compress_file(filename, f'compressed-{filename}.gz')
    
            return render_template("compress.html", check=1)
        
        else:
            print("ERROR")
            return render_template("compress.html", check=-1)


@app.route("/decompress", methods=["GET", "POST"])
def decompress():

    if request.method == "GET":
        return render_template("decompress.html", check=0)

    elif request.method == 'POST':
        up_file = request.files["file"]

        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
            
            decompress_file(filename, f"decompressed-{filename}.gz")

            return render_template("decompress.html", check=1)

        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)


if __name__ == '__main__':
    app.run(debug=True)

