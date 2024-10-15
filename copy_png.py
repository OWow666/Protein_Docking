import os
import shutil

docker = os.path.join(os.getcwd(), 'protein')
origin_dir = r'E:\Protein_Docking\5L71(Gpx4-Mus Musculus)蛋白对接结果'

for origin_docker in os.listdir(origin_dir):
    if not origin_docker.endswith('.xlsx'):
        for file in os.listdir(os.path.join(origin_dir, origin_docker)):
            if file.endswith('.png'):
                print(file, origin_docker)
                print(os.path.join(origin_dir, origin_docker, file))
                shutil.copy(os.path.join(origin_dir, origin_docker, file), os.path.join(docker, origin_docker))