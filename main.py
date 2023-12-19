from flask import Flask, render_template, request
import zipfile
import glob
import os
from PIL import Image


app = Flask(__name__)
app.config["FILE_UPLOADS"] = "/Users/arshad/Desktop/Huffman_Coding/uploads/"


global filename
global ftype


def compress_image_size(input_path, output_path, target_size_mb):
    # Open the image file
    with Image.open(input_path) as img:
        # Calculate the target size in bytes
        target_size_bytes = target_size_mb * 1024 * 1024

        # Resize the image while maintaining the aspect ratio
        img.thumbnail((1000, 1000))  # You can adjust the size as needed

        # Set initial compression quality for WebP format
        quality_low, quality_high = 1, 100
        quality = (quality_low + quality_high) // 2

        # Perform binary search to find optimal quality
        while quality_low < quality_high:
            temp_path = "temp_image.webp"
            img.save(temp_path, "WEBP", quality=quality)

            # Check if the temporary file meets the target size
            current_size = os.path.getsize(temp_path)

            if current_size <= target_size_bytes:
                quality_high = quality
            else:
                quality_low = quality + 1

            os.remove(temp_path)
            quality = (quality_low + quality_high) // 2

        # Save the final image with the optimal quality in JPEG format
        img.convert("RGB").save(output_path, "JPEG", quality=30)

def compress_file(input_filename, output_filename):
    with open(input_filename, 'rt') as input_file:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(input_filename, arcname=os.path.basename(input_filename))



def decompress_file(zip_filename, output_folder):
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        # Extract all contents of the zip file into the specified output folder
        zip_file.extractall(output_folder)


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
            decompress_file(filename, f"decompressed-{filename}")
            return render_template("decompress.html", check=1)
        else:
            print("ERROR")
            return render_template("decompress.html", check=-1)


@app.route('/compress-image', methods=['GET', 'POST'])
def compress_image():
    if request.method == 'GET':
        return render_template("compress-image.html", check=0)

    elif request.method == 'POST':
        up_file = request.files["file"]
        if len(up_file.filename) > 0:
            global filename
            global ftype
            filename = up_file.filename
            print(up_file.filename)
            up_file.save(os.path.join(app.config["FILE_UPLOADS"], filename))
        
            target_size_mb = 1

            compress_image_size(filename, f'compressed-{filename}', target_size_mb)
    
            return render_template("compress-image.html", check=1)
        
        else:
            print("ERROR")
            return render_template("compress-image.html", check=-1)


if __name__ == '__main__':
    app.run(debug=True)

