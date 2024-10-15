import pandas as pd
import os
import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0'
}

failed_list = []
def download_pdb(accession_id):
    url = f'https://alphafold.ebi.ac.uk/files/AF-{accession_id}-F1-model_v1.pdb'
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()

        pdb_file = os.path.join('./PDB', f'{accession_id}.pdb')
        if os.path.exists(pdb_file):
            print(f'{accession_id}.pdb has already been downloaded')
            return

        with open(pdb_file, 'w') as file:
            file.write(response.text)
        print(f'{accession_id}.pdb has been downloaded successfully.')
    except Exception as err:
        print(f'An error occurred: {err}')
        failed_list.append(f'{accession_id}.pdb')

if __name__ == '__main__':
    required_file = 'required_protein.xlsx'
    df = pd.read_excel(required_file)

    output = './PDB'
    if not os.path.exists(output):
        os.makedirs(output)

    for index, row in df.iterrows():
        accession_id = row['Accession']
        download_pdb(accession_id)
    print(f'\nThe following ids are downloaded failed.\n {failed_list}')
    print("Done!")