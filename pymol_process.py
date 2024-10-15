from pymol import cmd
import os
import pandas as pd
import zipfile
import shutil

def unzip_protein(docker_dir):
    zip_dir = os.path.join(docker_dir, 'zip')

    for zip_filename in os.listdir(zip_dir):
        if zip_filename.endswith('.zip'):
            zip_path = os.path.join(zip_dir, zip_filename)
            # extract_dir = os.path.join(zip_path, zip_filename[:-6])
            output = os.path.join(docker_dir, zip_filename[-10:-4])
            if not os.path.exists(output):
                os.mkdir(output)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output)

            for file in os.listdir(os.path.join(output, 'GRAMMresults')):
                if file not in ['receptor.pdb', 'ligand_model1.pdb']:
                    os.remove(os.path.join(os.path.join(output, 'GRAMMresults'), file))
                else:
                    shutil.copy(os.path.join(os.path.join(output, 'GRAMMresults'), file), output)
            shutil.rmtree(os.path.join(output, 'GRAMMresults'), ignore_errors=True)

    print("Extract done!")

def pymol_process(docker_dir):
    for protein in os.listdir(docker_dir):
        if protein.endswith("zip") or protein.endswith(".xlsx"):
            continue
        protein_dir = os.path.join(docker_dir, protein)
        requirement = pd.read_excel(os.path.join(protein_dir, f'{protein}.xlsx'))
        # print(requirement['receptor_res'])

        cmd.load(os.path.join(protein_dir, 'receptor.pdb'), 'receptor')
        for i in range(200,500):
            cmd.remove(f"resi {i}")

        cmd.load(os.path.join(protein_dir, 'ligand_model1.pdb'), 'ligand_model1')

        objects = ['receptor', 'ligand_model1']
        for object in objects:
            cmd.show('cartoon', object)
            cmd.set('cartoon_transparency', 0.5, object)

        for index, element in requirement.iterrows():
            res1 = element['receptor_res']
            res2 = element['ligand_res']
            cmd.show('sticks', f'receptor and resi {res1}')
            #cmd.set('transparency', 1, f'receptor and resi {res1}')
            cmd.show('sticks', f'ligand_model1 and resi {res2}')
            #cmd.set('transparency', 1, f'ligand_model1 and resi {res2}')
            cmd.distance('hbonds',
                         f"receptor and resi {element['receptor_res']} and name {element['receptor_atom']}",
                         f"ligand_model1 and resi {element['ligand_res']} and name {element['ligand_atom']}",
                         mode=2,
                         label=0)

        cmd.pseudoatom(name='receptor_pos', selection="receptor", label="5L71(Gpx4)")
        cmd.pseudoatom(name='ligand_pos', selection="ligand_model1", label=f"{protein}")

        cmd.set('ray_opaque_background', 0)
        cmd.set('cartoon_transparency', 0.5, "receptor and ligand_model1")
        cmd.png(os.path.join(protein_dir, f'{protein}.png'), width=4000, height=4000, ray=0)
        print(f'{protein}.png Done!')
        #cmd.hide("cartoon", "receptor")
        #cmd.hide("cartoon", "ligand_model1")

        cmd.zoom("hbonds",1, complete=1)
        cmd.set("cartoon_transparency", 0.9, f"receptor and ligand_model1")
        cmd.png(os.path.join(protein_dir, f'{protein}_docking_area.png'), width=4000, height=4000, ray=0)
        print(f'{protein}_docking_area.png Done!')

        cmd.delete("receptor")
        cmd.delete("ligand_model1")

if __name__ == '__main__':
    docker = os.path.join(os.getcwd(), 'protein')
    # unzip_protein(docker)
    '''
    Move the required_protein.xlsx to the docker
    '''
    pymol_process(docker)
