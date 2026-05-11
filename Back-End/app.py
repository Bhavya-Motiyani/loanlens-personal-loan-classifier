from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)

# Enable CORS properly
CORS(app, resources={r"/*": {"origins": "*"}})

# Load model
model = joblib.load("final_rfc_model.pkl")
print(model.feature_names_in_)

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        print("Received Data:", data)

        age = float(data["age"])
        income = float(data["income"])
        ccavg = float(data["ccavg"])
        cd_account = float(data["cd_account"])
        mortgage = float(data["mortgage"])
        education = float(data["education"])

        cc_to_income_ratio = ccavg / income

        input_data = pd.DataFrame([[
            age,
            income,
            cd_account,
            mortgage,
            education,
            ccavg,
            cc_to_income_ratio
        ]], columns=[
            "Age",
            "Income",
            "CD Account",
            "Mortgage",
            "Education",
            "CCAvg",
            "CCToIncomeRatio"
        ])

        print(input_data)

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0][1]

        analysis_data = [

            {
                "feature": "Income",
                "value": income,
                "impact": min(income / 50000, 1)
            },

            {
                "feature": "CCAvg",
                "value": ccavg,
                "impact": min(ccavg / 5000, 1)
            },

            {
                "feature": "Education",
                "value": education,
                "impact": education / 3
            },

            {
                "feature": "CD Account",
                "value": cd_account,
                "impact": 0.8 if cd_account == 1 else 0.2
            },

            {
                "feature": "Mortgage",
                "value": mortgage,
                "impact": min(mortgage / 50000, 1)
            },

            {
                "feature": "Age",
                "value": age,
                "impact": -min(age / 100, 1)
            }

        ]

        return jsonify({
            "prediction": int(prediction),
            "probability": round(float(probability), 2),
            "analysis": analysis_data
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)