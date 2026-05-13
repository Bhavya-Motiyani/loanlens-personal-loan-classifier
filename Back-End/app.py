from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import shap
import numpy as np

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Load trained pipeline
model = joblib.load("final_rfc_model.pkl")

# Extract Random Forest model
final_model = model.named_steps["RFC Model"]

# Create SHAP explainer
explainer = shap.TreeExplainer(final_model)

print("Model Loaded Successfully")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        print("Received Data:", data)

        # -------------------------
        # INPUT VALUES
        # -------------------------

        age = float(data["age"])
        income = float(data["income"])
        ccavg = float(data["ccavg"])
        cd_account = float(data["cd_account"])
        mortgage = float(data["mortgage"])
        education = float(data["education"])

        # Derived feature
        cc_to_income_ratio = (
            ccavg / income
            if income != 0
            else 0
        )

        # -------------------------
        # CREATE INPUT DATAFRAME
        # -------------------------

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

        # -------------------------
        # PREDICTION
        # -------------------------

        prediction = int(
            final_model.predict(input_data)[0]
        )

        probability = float(
            final_model
            .predict_proba(input_data)[0][1]
        )

        # -------------------------
        # SHAP VALUES
        # -------------------------

        shap_values = explainer.shap_values(input_data)

        # Convert to numpy array
        shap_values = np.array(shap_values)

        print("SHAP VALUES SHAPE:", shap_values.shape)

        """
        YOUR MODEL RETURNS:
        (samples, features, classes)

        Example:
        (1, 7, 2)

        We want:
        sample 0
        all features
        class 1
        """

        class_1_shap = shap_values[0, :, 1]

        # -------------------------
        # BASE VALUE
        # -------------------------

        expected_value = np.array(
            explainer.expected_value
        )

        print("EXPECTED VALUE:", expected_value)

        # Class 1 base value
        base_value = float(expected_value[1])

        # -------------------------
        # FEATURE INFO
        # -------------------------

        feature_names = [
            "Age",
            "Income",
            "CD Account",
            "Mortgage",
            "Education",
            "CCAvg",
            "CCToIncomeRatio"
        ]

        feature_values = [
            age,
            income,
            cd_account,
            mortgage,
            education,
            ccavg,
            cc_to_income_ratio
        ]

        shap_analysis = []

        for feature, value, shap_val in zip(
            feature_names,
            feature_values,
            class_1_shap
        ):

            shap_analysis.append({

                "feature": feature,

                "value": round(
                    float(value),
                    2
                ),

                "shap_value": round(
                    float(shap_val),
                    5
                ),

                "direction": (
                    "positive"
                    if shap_val >= 0
                    else "negative"
                )

            })

        # -------------------------
        # RESPONSE
        # -------------------------

        return jsonify({

            "prediction": prediction,

            "probability": round(
                probability,
                4
            ),

            "base_value": round(
                base_value,
                5
            ),

            "shap_values": shap_analysis

        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500
    

@app.route("/analysis", methods=["POST"])
def analysis():

    try:

        data = request.json

        # LOAD DATASET
        df = pd.read_csv(
            "Bank_Personal_Loan_Modelling.csv"
        )

        print("TOTAL DATASET ROWS:", len(df))

        age = data.get("age")
        income = data.get("income")
        ccavg = data.get("ccavg")

        print("FILTER DATA:", data)

        # -------------------------
        # AGE FILTER
        # -------------------------

        if age not in [None, ""]:

            age = int(age)

            df = df[
                (df["Age"] >= age - 15) &
                (df["Age"] <= age + 15)
            ]

            print("AFTER AGE:", len(df))

        # -------------------------
        # INCOME FILTER
        # -------------------------

        if income not in [None, "", "0"]:

            income = int(income)

            df = df[
                (df["Income"] >= income - 80) &
                (df["Income"] <= income + 80)
            ]

            print("AFTER INCOME:", len(df))

        # -------------------------
        # CCAVG FILTER
        # -------------------------

        if ccavg not in [None, "", "0"]:

            ccavg = float(ccavg)

            df = df[
                (df["CCAvg"] >= ccavg - 5) &
                (df["CCAvg"] <= ccavg + 5)
            ]

            print("AFTER CCAVG:", len(df))

        # -------------------------
        # IF EMPTY
        # -------------------------

        if len(df) == 0:

            return jsonify({

                "table": [],

                "stats": {

                    "total_rows": 0,
                    "avg_income": 0,
                    "loan_percentage": 0,
                    "cd_percentage": 0,

                    "education_counts": {
                        "edu1": 0,
                        "edu2": 0,
                        "edu3": 0
                    }
                }
            })

        # -------------------------
        # TABLE
        # -------------------------

        table_data = df[[
            "Age",
            "Income",
            "Family",
            "CCAvg",
            "Education",
            "Mortgage",
            "CD Account",
            "Online",
            "Personal Loan"
        ]].head(20)

        # -------------------------
        # STATS
        # -------------------------

        total_rows = len(df)

        avg_income = round(
            float(df["Income"].mean()),
            1
        )

        loan_percentage = round(
            float(df["Personal Loan"].mean()) * 100,
            1
        )

        cd_percentage = round(
            float(df["CD Account"].mean()) * 100,
            1
        )

        education_counts = {

            "edu1":
                int((df["Education"] == 1).sum()),

            "edu2":
                int((df["Education"] == 2).sum()),

            "edu3":
                int((df["Education"] == 3).sum())
        }

        return jsonify({

            "table":
                table_data.to_dict(
                    orient="records"
                ),

            "stats": {

                "total_rows":
                    total_rows,

                "avg_income":
                    avg_income,

                "loan_percentage":
                    loan_percentage,

                "cd_percentage":
                    cd_percentage,

                "education_counts":
                    education_counts
            }

        })

    except Exception as e:

        print("ANALYSIS ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

