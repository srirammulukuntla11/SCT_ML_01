🏠 House Price Prediction System

An End-to-End Machine Learning Web Application that predicts house prices based on various property features.
The project uses machine learning regression models trained on housing data and provides real-time predictions through a Streamlit web interface.

🚀 Project Overview

House price prediction is an important problem in real estate analytics. This project builds a machine learning model that analyzes housing data and predicts property prices based on user-provided features.

The system demonstrates the complete ML pipeline, including:

Data preprocessing

Model training

Model serialization

Web application deployment

Real-time predictions

The trained model is integrated into a Streamlit application where users can enter house details and instantly receive predicted prices.

📊 Dataset

The dataset used for training contains housing attributes such as:

Property size / area

Number of rooms

House features

Other property attributes affecting price

The data is split into:

train.csv → used for training the model

test.csv → used for testing predictions

🧠 Machine Learning Model

The machine learning model is trained using Scikit-Learn regression algorithms.

Steps in Model Development

Data Preprocessing

Handling missing values

Cleaning dataset

Feature Selection

Selecting important features affecting house prices

Model Training

Training regression model using Scikit-Learn

Model Saving

Saving trained model as house_model.pkl

Deployment

Loading model in Streamlit web application for prediction

🖥️ Web Application

The project includes a Streamlit web interface where users can:

Enter house property details

Submit the information

Get instant predicted house price

This makes the system interactive and user-friendly.

🛠 Technologies Used
Programming Language

Python

Libraries

Pandas

NumPy

Scikit-Learn

Streamlit

Pickle

Tools

Jupyter Notebook

GitHub

📂 Project Structure
SCT_ML_01
│
├── app.py                  # Streamlit Web Application
├── model.py                # Model training script
├── house_model.pkl         # Saved trained ML model
├── train.csv               # Training dataset
├── test.csv                # Testing dataset
├── sample_submission.csv   # Example prediction format
├── requirements.txt        # Required libraries
└── README.md               # Project documentation
⚙️ Installation and Setup
1️⃣ Clone the Repository
git clone https://github.com/srirammulukuntla11/SCT_ML_01.git
cd SCT_ML_01
2️⃣ Install Dependencies
pip install -r requirements.txt

If requirements file is empty install manually:

pip install streamlit pandas scikit-learn numpy
3️⃣ Run the Application
streamlit run app.py
4️⃣ Open in Browser
http://localhost:8501
✨ Features

Machine Learning based price prediction

Real-time predictions

Simple and clean web interface

Pre-trained ML model

Easy to run and beginner friendly

🔮 Future Improvements

Add more advanced ML models (Random Forest, XGBoost)

Deploy the project on Streamlit Cloud

Add data visualizations

Improve UI design

👨‍💻 Author

Sriram Mulukuntla

GitHub:
https://github.com/srirammulukuntla11
