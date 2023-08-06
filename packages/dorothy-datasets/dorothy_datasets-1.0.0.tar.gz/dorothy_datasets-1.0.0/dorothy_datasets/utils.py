
__all__ = ['download_image_from_server', 'get_md5', 'get_dataset_from_server', 'md5_directory']


import argparse, traceback, json, os
import requests, json
import hashlib,pathlib


def get_md5(path):
    return hashlib.md5(pathlib.Path(path).read_bytes()).hexdigest()

def md5_directory(path):
    digest = hashlib.md5()

    for root, dirs, files in os.walk(path):
        for names in files:
            file_path = os.path.join(root, names)

            # Hash the path and add to the digest to account for empty files/directories
            digest.update(hashlib.sha1(file_path[len(path):].encode()).digest())

            # Per @pt12lol - if the goal is uniqueness over repeatability, this is an alternative method using 'hash'
            # digest.update(str(hash(file_path[len(path):])).encode())

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f_obj:
                    while True:
                        buf = f_obj.read(1024 * 1024)
                        if not buf:
                            break
                        digest.update(buf)

    return digest.hexdigest()

def get_dataset_from_server(dataset, headers):
    response = requests.get('https://dorothy-image.lps.ufrj.br/images/?search={DATASET}'.format(DATASET=dataset), headers=headers)
    data = json.loads(response.content)
    return data

def download_image_from_server(url , output, headers):
      file = open(output,"wb")
      response = requests.get(url, headers=headers)
      file.write(response.content)
      file.close()
