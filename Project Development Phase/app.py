import base64
from flask import Flask, render_template, request, send_file, send_from_directory
from twilio.rest import Client
import datetime
from io import BytesIO
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import numpy as np
from PIL import Image
import requests

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
app = Flask(__name__)
model = load_model(r"UCF.h5", compile = False)

# for twilio
account_sid = 'AC4512273a08e04745bc4313e8740bb483'
auth_token = 'e86a599b868eae767e62cc2c19dfe8d3'
client = Client(account_sid, auth_token)

#for saving input to folder
UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#get current date time day and location
global date, day, time
dt = datetime.datetime.now()
date = str(dt.date())
day = str(dt.strftime('%A'))
time = str(dt.time().strftime('%H:%M:%S'))

ACCESS_TOKEN = '2dd3de5dc9a453'
def Location():
    url = f'https://ipinfo.io?token={ACCESS_TOKEN}'
    try:
        response = requests.get(url)
        data = response.json()

        location = data.get('loc')
        city = data.get('city')
        region = data.get('region')
        country = data.get('country')

        return [location, city, region, country]
        # print(f"Location: {location}")
        # print(f"City: {city}")
        # print(f"Region: {region}")
        # print(f"Country: {country}")
    except Exception as e:
        # print(f"Error: {e}")
        return "Error detecting location"
location = Location()

#checek if filename has allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#delete files
def delete_files_in_uploads():
    files = os.listdir(UPLOAD_FOLDER)
    for file in files:
        os.remove(os.path.join(UPLOAD_FOLDER, file))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def Home():
    return render_template('index.html')

@app.route('/LearnMore.html')
def LearnMore():
    return render_template('LearnMore.html')

@app.route('/TandC.html')
def TandC():
    return render_template('TandC.html')

@app.route('/AboutUs.html')
def AboutUs():
    return render_template('AboutUs.html')

@app.route('/LawEnforcement')
def lawEnforcement():
    return render_template('LawEnforcement.html')

@app.route('/Public')
def Public():
    return render_template('Public.html')
#########################################################
# send message to phone
@app.route('/send_sms', methods = ['POST'])
def send_sms():
    
    message = "Alert!!! " + res + " Detected on " + date + "(" + day + ")" + " at " + time +".\nLocation: " + location[0] + "\nCity: " + location[1] + "\nRegion: " + location[2] + "\nCountry: " + location[3]
    try:
        message = client.messages.create(
            body = message,
            from_ = +12192242908,
            to = +919740963263
        )
        return "message sent"
    except Exception as e:
        return 'Failed to send message'
    
#Upload image to folder
@app.route('/Upload_to_folder',methods = ['POST'])
def Upload_to_folder():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        delete_files_in_uploads()
        # Save the uploaded file to the "uploads" directory
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return 'File successfully uploaded and saved.'
    
    return 'Invalid file type. Only JPG, JPEG, and PNG files are allowed.'

@app.route('/Upload_to_folder_camera', methods = ['POST'])
def Upload_to_folder_camera():
    delete_files_in_uploads()
    image_data = request.json.get('image', None)
    if image_data:
        try:
            image_bytes = base64.b64decode(image_data.split(',')[-1])
            filename = secure_filename('capturedImage.jpg')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(file_path, 'wb') as f:
                f.write(image_bytes)
            return "FIle successfully uploaded"
        except Exception as e:
            return f"Error:{str(e)}"
    return "invalid image data"

#Classification
@app.route('/Classify', methods = ['POST'])
def Classify():
    global res
    button = request.headers.get('currentButton')
    if button == '1':
        if 'filename' in request.form:
            filename = request.form['filename']
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # img = image.load_img(image_path, target_size = (64,64))
            # x = image.img_to_array(img)
            # x = np.expand_dims(x, axis = 0)
            # pred = np.argmax(model.predict(x), axis = 1)
            # index = ['Abuse', 'Arrest', 'Arson', 'Assult', 'Burglary', 'Explosion', 'Fighting', 'Normal', 'Accident', 'Robbery', 'Shooting', 'Shoplifting', 'Stealing', 'Vandalism']
            # res = str(index[pred[0]])
            # return res
    if button == '0':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'capturedImage.jpg')

    img = image.load_img(image_path, target_size = (64,64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    pred = np.argmax(model.predict(x), axis = 1)
    index = ['Abuse', 'Arrest', 'Arson', 'Assult', 'Burglary', 'Explosion', 'Fighting', 'Normal', 'Accident', 'Robbery', 'Shooting', 'Shoplifting', 'Stealing', 'Vandalism']
    res = str(index[pred[0]])
    return res

#generate and download pdf of the input image
@app.route('/generate_pdf/<filename>')
def generate_pdf(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(image_path):
        return 'File not found'
    
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    img1 = Image.open(image_path)
    # image_width, image_height = img1.size
    image_width, image_height = 256,256
    page_width, page_height = letter
    # image_width, image_height = page_width, page_height
    x = (page_width - image_width)/2
    y = (page_height - image_height)/2
    c.drawImage(image_path, x, y, width=image_width, height=image_height)
    
    c.setFont("Times-Bold", 26)
    header_text = 'Crime Vision'
    c.drawCentredString(page_width/2, page_height - 50, header_text )

    res_text = "Classification Result: " + res
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 20,res_text)
    y-=30
    res_text2 = "Date: " + date
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text2)
    y-=25
    res_text3 = "Day: " + day
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text3)
    y-=25
    res_text4 = "Time: " + time
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text4)

    y-=25
    res_text5 = "Location: " + location[0]
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text5)

    y-=25
    res_text6 = "City: " + location[1]
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text6)

    y-=25
    res_text7 = "Region: " + location[2]
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text7)

    y-=25
    res_text8 = "Country: " + location[3]
    c.setFont("Times-Roman", 18)
    c.drawString(50, y - 10,res_text8)

    footer_text = "Location and Time data is purley based on the location of device generating pdf and NOT the image depicted"
    c.setFont("Times-Roman",14)
    # c.showPage()
    # c.drawCentredString(50, page_height - 50, footer_text)
    c.drawCentredString(page_width/2, 10, footer_text)
    c.showPage()
    c.save()

    pdf_buffer.seek(0)

    # return send_file(pdf_path, as_attachment = True)
    return send_file(pdf_buffer, as_attachment=True, download_name='result.pdf')
    
@app.route('/Back')
def clear():
    delete_files_in_uploads()
if __name__ == "__main__":
    app.run(debug=True)