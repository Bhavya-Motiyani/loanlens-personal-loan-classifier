# LoanLens - Personal Loan Classifier


End-to-end ML project to predict personal loan acceptance for a retail bank (Thera Bank). Includes business-driven EDA, feature engineering, imbalance handling with SMOTENC, GridSearchCV tuning, model comparison, SHAP-based explainability, interactive analytics dashboards, bulk CSV prediction support, and Flask-based deployment. Optimized for high recall to minimize missed revenue opportunities.

Personal Loan Acceptance Prediction 🧠
Project Overview
Feature	Description
Domain	Banking / Predictive Analytics
Business Problem	Convert liability customers into personal loan customers
Goal	Predict which customers are likely to accept a personal loan
Algorithms Used	Logistic Regression, Random Forest Classifier
Dataset Size	5,000 customer records
Target Variable	Personal Loan (1 – Accepted, 0 – Not Accepted)
Deployment	Interactive Flask-based web application
Hosting Platform	Render
Explainability	SHAP (SHapley Additive exPlanations)
Additional Features	Real-time prediction, CSV batch prediction, analytics dashboard, dynamic feature simulation
📊 Dataset Information
Feature	Description
Source	Thera Bank Personal Loan Dataset
Customer Type	Existing depositors
Data Nature	Demographic, Financial & Behavioral
Class Distribution	~10% positive class (highly imbalanced)
🧾 Feature Description
Category	Features
Demographics	Age, Experience, Family, Education
Financial	Income, Mortgage
Banking Behavior	CCAvg, CD Account, Online, Credit Card
Engineered Features	Age Group, CCToIncomeRatio, Mortgage Category
🔍 Exploratory Data Analysis (EDA)
Key Insights
Observation	Business Insight
Income < $50k → No loan acceptance	Low-income customers should not be targeted
CD Account holders → ~6.5× acceptance	Highest priority campaign group
High income + high mortgage	Higher likelihood of loan acceptance
Graduates & professionals dominate loan takers	Education impacts loan decisions
Only ~10% acceptance rate	Severe class imbalance problem
🎯 Business Recommendations
Focus Area	Action
Income	Target customers with income > $50,000
Age Group	Focus on customers aged 30–60
Banking Products	Prioritize CD Account holders
Mortgage	Target high-mortgage customers
Education	Prefer graduates & professionals
🛠 Feature Engineering
Feature	Purpose
CCToIncomeRatio	Captures spending behavior
Age Group	20-30,30-40,etc...
Mortgage Category	None,Low,Normal,High
🤖 Model Development
Model	Preprocessing	Imbalance Handling	Pipeline
Logistic Regression	ColumnTransformer (scaling + encoding)	SMOTENC	Yes
Random Forest Classifier	Not required	SMOTENC	Yes
⚖️ Model Evaluation Strategy
Metric	Reason
Recall (Primary)	False negatives = missed revenue
Confusion Matrix	Error analysis
ROC-AUC Curve	Threshold-independent evaluation
Classification Report	Overall model performance
🏆 Model Comparison & Selection
Model	Performance Summary
Logistic Regression	Baseline model
Random Forest Classifier	Higher recall & ROC-AUC
Final Choice	Random Forest Classifier
🌟 Web Application Features

The project includes a fully interactive multi-page web application integrated with the trained ML model.

🧠 Page 1 — Predictor Dashboard
Functionalities
Feature	Description
Real-time Prediction	User inputs customer details and receives instant prediction
Probability Visualization	Semi-circle probability gauge displays loan acceptance confidence
Decision Output	Displays Accepted / Rejected prediction
SHAP Explainability	Dynamic SHAP bars explain feature contribution
Batch CSV Prediction	Predicts loan acceptance for entire uploaded dataset
Download Predictions	Export predicted CSV containing Personal Loan column
Prediction Workflow
User enters customer feature values
Frontend sends data to Flask backend
Backend preprocesses data using trained pipeline
Model predicts:
Loan Decision
Prediction Probability
SHAP values are generated dynamically
Results are displayed visually in frontend
Bulk CSV Prediction

Users can upload datasets containing:

Same input columns as training dataset
Without Personal Loan column

The backend:

Predicts all rows
Adds prediction column
Generates downloadable CSV output
📊 Page 2 — Smart Dataset Analysis
Functionalities
Feature	Description
Dataset Upload	Upload custom customer dataset
Default Dataset Support	Uses training dataset if no upload is provided
Dynamic Filtering	Filter rows using selected customer features
Flexible Inputs	Filters are optional and combinable
Live Statistics	Real-time metrics update based on filtered rows
Export CSV	Download filtered dataset
Smart Filtering Logic

For numerical features:

Income
CCAvg
Mortgage

Filtering uses:

>= entered_value

Example:

Income = 60
→ Selects rows where Income ≥ 60
Analytics Dashboard

The dashboard dynamically displays:

Metric	Description
Total Rows	Count of filtered customers
Average Income	Mean income
Loan Acceptance %	% who accepted loan
CD Account %	% with CD account
Education Count	Education category distribution
Filtered Data Table

Displayed table includes:

All dataset columns
Loan values converted into:
Accepted
Rejected
📈 Page 3 — Feature Effects Simulator
Functionalities
Feature	Description
Interactive Feature Controls	Dynamically change feature values
Live Probability Updates	Probability changes instantly
Dynamic SHAP Values	SHAP contributions update in real time
Feature Sensitivity Analysis	Observe how features affect prediction
SHAP Visualization
Color	Meaning
🔴 Red	Positive impact toward loan acceptance
🔵 Blue	Negative impact toward rejection

The simulator demonstrates:

Model sensitivity
Feature influence strength
Real-time explainable AI behavior
🚀 Deployment
Step	Description
Model Saving	Serialized using pickle
Backend Framework	Flask
Hosting Platform	Render
Prediction Type	Real-time + batch prediction
Explainability	SHAP integration
Frontend	HTML, CSS, JavaScript
📁 Project Structure
Component	Description
EDA Notebook	Business insights & campaign strategy
Model Notebook	Pipelines, training & evaluation
Pickle File	Final trained model
Flask Backend	Prediction & filtering APIs
Frontend UI	Interactive dashboards
CSV Export System	Prediction & filtering downloads
SHAP Integration	Explainable AI visualizations
🧠 Key Learnings
Area	Takeaway
Business Analytics	Translating EDA into decisions
ML Pipelines	End-to-end, leakage-free modeling
Imbalance Handling	Effective use of SMOTENC
Model Evaluation	Metrics aligned with business cost
Deployment	From notebook to deployed web application
Explainable AI	Understanding predictions using SHAP
Full Stack ML	Frontend-backend-model integration
Data Filtering Systems	Building pandas-based analytics pipelines
Batch Inference	Predicting on uploaded datasets
Interactive Dashboards	Real-time analytics visualization
Deployment Platforms	Hosting Flask applications using Render
🧰 Tech Stack
Category	Tools
Data Processing	Pandas, NumPy
Visualization	Matplotlib, Seaborn
Modeling	Scikit-learn, Imbalanced-learn
Explainability	SHAP
Backend	Flask
Frontend	HTML, CSS, JavaScript
Deployment	Render
Model Saving	Pickle
📜 License
License	Description
MIT License	Free for learning & reference with attribution
👩‍💻 Authors
Bhavya Motiyani

B.Tech in Computer Science and Engineering (Data Science Specialization)
Gujarat Technological University — VGEC

Contributions
Exploratory Data Analysis (EDA)
Feature Engineering
SMOTENC imbalance handling
Machine Learning model development & evaluation
SHAP explainability integration
Backend development and Flask integration
CSV prediction and analytics pipeline implementation
Project Collaborator
Contributions
Frontend UI/UX design and implementation
Interactive dashboard development
Frontend functionality integration
Backend integration and application workflow
User interaction and visualization components
Development Note

Certain implementation, debugging, and integration tasks were completed with AI-assisted development tools.

📧 Email: bhavyamotiyani68@gmail.com

🔗 LinkedIn Profile
