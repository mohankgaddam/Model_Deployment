from flask import Flask, jsonify, render_template, request
import tensorflow as tf
import tensorflow_datasets as tfds


app = Flask(__name__)
padding_size = 800
model = tf.keras.models.load_model("sentiment_analysis.hdf5")
text_encoder = tfds.features.text.TokenTextEncoder.load_from_file("vocab")

print("Model and Vocabulary Loaded")

def pad_to_size(vec, size):
    zeros = [0] * (size-len(vec))
    vec.extend(zeros)
    return vec

def predict_fn(predict_text, pad_size):
    encoded_text = text_encoder.encode(predict_text)
    encoded_text = pad_to_size(encoded_text, pad_size)
    encoded_text = tf.cast(encoded_text, tf.int64)
    predictions = model.predict(tf.expand_dims(encoded_text, 0))

    return predictions.tolist()

@app.route('/predict', methods=['GET', 'POST'])
def predict_sentiment():
    text = str(request.form['review_text'])
    print(text)
    predictions = predict_fn(text, padding_size)
    print(predictions)
    if float(''.join(map(str, predictions[0]))) > 0:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'

    temp = jsonify({'predictions': predictions, 'sentiment': sentiment})
    print(temp)
    return render_template('home.html', prediction = 'Sentiment of the review is {}'.format(sentiment))

@app.route('/')
def home():
    return render_template('home.html')

"""
@app.route('/model', methods=['POST'])
def predict_sentiment():
    text = request.get_json()['text']
    print(text)
    predictions = predict_fn(text, padding_size)
    if float(''.join(map(str, predictions[0]))) > 0:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'

    return jsonify({'predictions': predictions, 'sentiment': sentiment})

@app.route('/test')
def hello():
    return "Testing the flask app"
"""

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5003')
