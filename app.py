import numpy as np
import io
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, Response, render_template, request, abort
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from preprocessing.ndvi import get_ndvi
from preprocessing.preprocessing import angles_to_pixel
from parse.parse_angles import parse_angles
from plot.plot_ndvi import plot_ndvi
from configs.config import *

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MAX_CONTENT_LENGTH'] = 5000 * 2000 * 200
app.config['UPLOAD_EXTENSIONS'] = ['.tif', '.txt']
app.config['UPLOAD_PATH'] = 'static/process_images'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_files():
    red_img = None
    nir_img = None
    key_points = None
    files = request.files.getlist('file')
    filenames = []
    if (request.files['file'].filename == ''):  # Нет файлов
        return ('', 204)
    for uploaded_file in files:
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            filenames.append(filename)
            if "B4" in filename:
                red_img = Image.open(uploaded_file.stream)
                red_img = np.array(red_img).astype('float64')
                print(red_img)
            if "B3" in filename:
                nir_img = Image.open(uploaded_file.stream)
                nir_img = np.array(nir_img).astype('float64')
                print(nir_img)
            if "MTL" in filename:
                angles_dict = parse_angles(uploaded_file.stream)
                shape = red_img.shape
                points_angle = [point_a, point_b, point_c, point_d]
                key_points = [angles_to_pixel(shape, point, angles_dict) for point in points_angle]
                x, y = key_points[0]
                dx = abs(key_points[0][0] - key_points[1][0])
                dy = abs(key_points[0][1] - key_points[2][1])

    if (red_img is None) or (nir_img is None) or (key_points is None):
        print('Files not exist')
        abort(400)

    ndvi = get_ndvi(nir_img, red_img)
    ndvi_city = ndvi[y:y+dy, x:x+dx]
    fig = plot_ndvi(ndvi_city)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if (__name__ == '__main__'):
    app.run(debug=True, use_reloader=False)
