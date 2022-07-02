from flask import Flask, render_template, request, url_for
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import numpy as np

app = Flask(__name__)

dic = {0 : 'Fresh', 1 : 'Spoiled'}

modelBanana = load_model('BananaModel.h5')

modelBanana.make_predict_function()

def the_predict(model, img):
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    predictions = model.predict(img_array)
    print(predictions)
    predicted_class = dic.get(np.argmax(predictions[0]))
    confidence = round(100 * (np.max(predictions[0])),2)
    return predicted_class, confidence

def predict_label_banana(img_path):
	i = image.load_img(img_path, target_size=(224,224))
	#i = image.img_to_array(i)/255.0
	#i = i.reshape(1, 224,224,3)
	the_class, con = the_predict(modelBanana,i)
	return the_class

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submitBanana", methods = ['GET', 'POST'])
def get_output4():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/Banana/" + img.filename	
		img.save(img_path)

		p = predict_label_banana(img_path)

	return render_template("index.html", prediction4 = p, img_path4 = img_path)

if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)