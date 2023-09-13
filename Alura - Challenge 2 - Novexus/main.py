'''
#### Dicionário de dados

* `customerID`: número de identificação único de cada cliente
* `Churn`: se o cliente deixou ou não a empresa 
* `gender`: gênero (masculino e feminino) 
* `SeniorCitizen`: informação sobre um cliente ter ou não idade igual ou maior que 65 anos 
* `Partner`:  se o cliente possui ou não um parceiro ou parceira
* `Dependents`: se o cliente possui ou não dependentes
* `tenure`:  meses de contrato do cliente
* `PhoneService`: assinatura de serviço telefônico 
* `MultipleLines`: assisnatura de mais de uma linha de telefone 
* `InternetService`: assinatura de um provedor internet 
* `OnlineSecurity`: assinatura adicional de segurança online 
* `OnlineBackup`: assinatura adicional de backup online 
* `DeviceProtection`: assinatura adicional de proteção no dispositivo 
* `TechSupport`: assinatura adicional de suporte técnico, menos tempo de espera
* `StreamingTV`: assinatura de TV a cabo 
* `StreamingMovies`: assinatura de streaming de filmes 
* `Contract`: tipo de contrato
* `PaperlessBilling`: se o cliente prefere receber online a fatura
* `PaymentMethod`: forma de pagamento
* `Charges.Monthly`: total de todos os serviços do cliente por mês
* `Charges.Total`: total gasto pelo cliente

'''

import pandas as pd
import json
import requests
from ast import literal_eval

# data = pd.read_json('Telco-Customer-Churn.json')

# data.to_csv('Customer-Churn.csv', index=False)

# data_dict = json.loads('Telcon-Customer-Churn.json')
# print(data.head())

file = 'Telco-Customer-Churn.json'
file_frame = pd.read_json(file)
# file_json = json.loads(file_frame)
# jsonResponse = file.json()
jsonData = json.dumps(file_frame)
print(jsonData)

'''
file = 'Telco-Customer-Churn.json'
jsonData = json.dumps('Telco-Customer-Churn.json')

jsonDataList = []
jsonDataList.append(jsonData)

# jsonRDD = sc.parallelize(jsonDataList)
# df = spark.read.json(jsonRDD)
# display(df)
print(jsonData)
'''
