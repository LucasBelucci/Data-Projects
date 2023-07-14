import requests
import pandas as pd
import os.path

folder = 'C:\Kaggle\Alura - Challenge\Data'
valores = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


for i in valores:
    if len(str(i)) == 1:
        file_name = f'CEAPS_200{i}.csv'
        url = f'https://www.senado.gov.br/transparencia/LAI/verba/despesa_ceaps_200{i}.csv'
        file_path = os.path.join(folder, file_name)

    else:
        file_name = f'CEAPS_20{i}.csv'
        url = f'https://www.senado.gov.br/transparencia/LAI/verba/despesa_ceaps_20{i}.csv'
        file_path = os.path.join(folder, file_name)

    print('Dowloanding: ', url)
    file = requests.get(url, allow_redirects=True)
    url_content = file.content

    csv_file = open(file_path, 'wb')
    csv_file.write(url_content)
    csv_file.close()
    print('Done!')
