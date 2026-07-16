from flask import Flask, render_template, request,url_for
import joblib

# Load ML Model
model = joblib.load(r"Model/dtc_load.lb")

app = Flask(__name__)

# Store prediction history
prediction_history = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/history')
def history():
    return render_template(
        'history.html',
        history=prediction_history
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/project')
def project():
    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def predict():
    income = float(request.form['income'])
    credit_score = float(request.form['credit_score'])
    loan_amount = float(request.form['loan_amount'])
    years_employed = float(request.form['years_employed'])
    points = float(request.form['points'])

    data = [[
        income,
        credit_score,
        loan_amount,
        years_employed,
        points
    ]]

    pred = model.predict(data)

    print("Prediction:", pred)

    if pred[0] == 1:
        result = "Loan Approved ✅"
    else:
        result = "Loan Rejected ❌"

    prediction_history.append({
        "income": income,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "years_employed": years_employed,
        "points": points,
        "result": result
    })

    return render_template(
        "predict.html",
        prediction=result,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)