from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from second_method import ColorAnalyzer
from PIL import Image

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images'

class UploadFileForm(FlaskForm):
    file = FileField("Insert File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])

@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data 
        filename = secure_filename(file.filename)  #Secure the filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Create the filepath
        file.save(filepath)
        
        #Analyze the image and get the most common colors 
        img = Image.open(filepath)
        analyzer = ColorAnalyzer(img)
        
        common_colors = analyzer.most_common_colors()
        
        return render_template('index.html', form=form, filename=filename, common_colors=common_colors)\
    
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)