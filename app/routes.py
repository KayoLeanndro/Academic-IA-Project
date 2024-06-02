import base64
from io import BytesIO
from json import encoder
from flask import render_template, request, jsonify
from . import app
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def import_model():
    modelo_path = os.path.abspath('./data/models/logistic_regression.pkl')
    encoder_path = os.path.abspath('./data/models/encoder.pkl')
    scaler_path = os.path.abspath('./data/models/scaler.pkl')
    modelo = pickle.load(open(modelo_path, 'rb'))
    encoder = pickle.load(open(encoder_path, 'rb'))
    scaler = pickle.load(open(scaler_path, 'rb'))
    return modelo, encoder, scaler

    modelo, encoder, scaler = import_model()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
            # Obter os parâmetros do formulário
        age = float(request.form['age'])
        balance = float(request.form['balance'])
        duration = float(request.form['duration'])
        campaign = float(request.form['campaign'])
        pdays = float(request.form['pdays'])
        previous = float(request.form['previous'])

        job = request.form['job']
        marital = request.form['marital']
        education = request.form['education']
        default = request.form['default']
        housing = request.form['housing']
        loan = request.form['loan']
        contact = request.form['contact']
        month = request.form['month']
        poutcome = request.form['poutcome']

         # Codificar variáveis categóricas usando o encoder carregado
        categorical_data = np.array([[job, marital, education, default, housing, loan, contact, month, poutcome]])
        categorical_encoded = encoder.transform(categorical_data).toarray()

        # Concatenar variáveis categóricas e numéricas
        numerical_data = np.array([[age, balance, duration, campaign, pdays, previous]])
        parametros = np.hstack((categorical_encoded, numerical_data))

        # Normalizar os dados
        parametros_scaled = scaler.transform(parametros)

        ##Fazer a predição
        resultado = modelo.predict(parametros_scaled)[0]

         # Interpretação do resultado
        if resultado == 'no':
            resultado_texto = 'Não há chances de subscrição'
        else:
             resultado_texto = 'Há chances de subscrição'

        return f'Seu resultado é: "{resultado_texto}"!'
    except Exception as e:
            return jsonify({'error': f'400 Bad Request: {str(e)}'}), 400
        

@app.route('/ecclientes', methods=['GET'])
def mostrarEcClientes():
    df = pd.read_csv('data/processed/bank_marketing_processed.csv')
            
    job_counts = df['job'].value_counts()

     # Convertendo os dados para um formato JSON
    data = {
         'labels': job_counts.index.tolist(),
           'values': job_counts.values.tolist()
        }

    return jsonify(data)

@app.route('/maritalstatusclients', methods=['GET'])
def showMaritalStatusClients():
        df = pd.read_csv('data/processed/bank_marketing_processed.csv')
            
        marital_counts = df['marital'].value_counts()

        # Convertendo os dados para um formato JSON
        data = {
            'labels': marital_counts.index.tolist(),
            'values': marital_counts.values.tolist()
        }

        return jsonify(data)

@app.route('/educationclients', methods=['GET'])
def showEducationClients():
        df = pd.read_csv('data/processed/bank_marketing_processed.csv')
            
        education_counts = df['education'].value_counts()

        # Convertendo os dados para um formato JSON
        data = {
            'labels': education_counts.index.tolist(),
            'values': education_counts.values.tolist()
        }

        return jsonify(data)
    
    