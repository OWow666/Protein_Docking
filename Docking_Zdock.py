import os

import requests

url = 'https://zdock.wenglab.org/'

data = {
    'email': 'xxx@xxx.edu.cn',
    # 'select_zdock_version': '3.1.2',
    'skip_residue_selection': 'on',
}

def submit(files, filename):
    try:
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        print(f'Success! {filename} \'s docking request has been submitted.')
    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')
    except Exception as err:
        print(f'An error occurred: {err}')
    finally:
        files['protein1'].close()
        files['protein2'].close()

if __name__ == '__main__':
    for filename in os.listdir('./PDB'):
        file_path = os.path.join('./PDB', filename)
        files = {
            'protein1': open(file_path, 'rb'),
            'protein2': open(r'E:\Protein_Docking\5l71.pdb', 'rb'),
        }
        submit(files,filename)
    print("Done!")