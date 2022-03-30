from flask import Flask, url_for, render_template, request
import joblib
import numpy as np

app = Flask(__name__)
filename = 'calories_burnt.sav'
model = joblib.load(filename=filename)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try: 
            gender = request.form['gender']
            age = int(request.form['age'])
            height = int(request.form['height'])
            weight = int(request.form['weight'])
            duration = int(request.form['duration'])
            heartRate = int(request.form['heartRate'])
            bodyTemp = int(request.form['bodyTemp'])
        except ValueError:
            error_message = "Please Ensure All Values Are Numerical"
            return render_template('index.html', prediction_text=error_message)

        gender = 0 if gender[0].lower == 'm' else 1

        prediction = model.predict(np.array([gender, age, height, weight, duration, heartRate, bodyTemp]).reshape(1, -1))
        output = round(prediction[0], 2)

        return render_template('index.html', prediction_text=f'You burned {output} calories today')
    else:
        return render_template('index.html', prediction_text='')


if __name__ == "__main__":
    app.run(debug=True)