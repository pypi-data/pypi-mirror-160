
__all__ = ['download_china_from_server']

import os, sys
import pandas as pd
from tqdm import tqdm
from colorama import init, Back, Fore
from .stratified_kfold import stratified_train_val_test_splits
from .utils import download_image_from_server, get_dataset_from_server, get_md5, md5_directory
from .configs import get_dataset_config
init(autoreset=True)





def download_china_from_server( token, basepath=os.getcwd() ):

  dataset_name = 'china'
  config = get_dataset_config(dataset_name)
  headers = { "Authorization": token}

  print( Fore.BLUE + 'Downloading china dataset...' )

  # template
  d = {
      'dataset_name': [],
      'project_id': [],
      'target': [],
      'image_md5':[],
      'image_url': [],
      'image_path':[],
      'insertion_date': [],
      'metadata': [],
      'date_acquisition': [],
      'number_reports': [],
      }
  
  imagespath = basepath + '/china_images'

  if not os.path.exists(imagespath): 
    os.makedirs(imagespath)

  images = get_dataset_from_server('china', headers)

  # NOTE: check 1: number of images
  if len(images) != config['nimages']:
    print(Fore.RED + 'Number of images does not match with china dataset criterias. abort')
    sys.exit(1)


  for img in tqdm(images, desc='Downloading images...', ncols=100):
      
      img_path = imagespath + '/' + img['project_id']+".jpg"

      d['dataset_name'].append(img['dataset_name'])
      d['target'].append(img['metadata']['has_tb'])
      d['project_id'].append(img['project_id'])
      d['image_url'].append(img['image_url'])
      d['insertion_date'].append(img['insertion_date'])
      d['metadata'].append(img['metadata'])
      d['date_acquisition'].append(img['date_acquisition'])
      d['number_reports'].append(img['number_reports'])
      d['image_path'].append(img_path)

      if not os.path.exists(img_path):
        download_image_from_server( img['image_url'], img_path, headers)
      
      d['image_md5'].append(get_md5(img_path))

  # NOTE: check 2: compare the integrated images hash
  print( Fore.GREEN + 'Checking downloaded images in (%s)...'%imagespath )
  images_hash = md5_directory(imagespath)
  if  images_hash != config['md5_images']:
    print(Fore.RED + 'Hash not match. Abort!')
    # remove all images
    os.system('rm -rf '+imagespath)
    sys.exit(1)


  print( Fore.GREEN + 'Splitting...' )
  df = pd.DataFrame.from_dict(d)
  df = df.sort_values('project_id')
  splits = stratified_train_val_test_splits(df, 10, seed=config['seed'])
  df_splitted = None

  for test in range(10):
    for sort in range(9):
        
      train_index = splits[test][sort][0]
      val_index   = splits[test][sort][1]
      test_index  = splits[test][sort][2]
      
      df_train = df.iloc[train_index].copy()
      df_train['test'] = test
      df_train['sort'] = sort
      df_train['type'] = 'train'
      
      df_val = df.iloc[val_index].copy()
      df_val['test'] = test
      df_val['sort'] = sort
      df_val['type'] = 'val'       

      df_test = df.iloc[test_index].copy()
      df_test['test'] = test
      df_test['sort'] = sort
      df_test['type'] = 'test'       
      if df_splitted is not None:
          df_splitted = pd.concat((df_splitted, df_train, df_val, df_test) )
      else:
          df_splitted = pd.concat((df_train, df_val, df_test) )      
      df_splitted['dataset_type'] = 'real'
  

  df_splitted.reset_index(inplace=True, drop=True)


  # NOTE: check 3: number of final rows
  if len(df_splitted)!=config['nimages_splitted']:
    print(Fore.RED + 'Number of rows after split not match. Abort!')
    # remove all images
    os.system('rm -rf '+imagespath)
    os.exit(1)


  # NOTE: check 4: hash index columns
  df_splitted[['target', 'test', 'sort', 'type']].to_csv(basepath+'/.check_columns.csv')
  columns_hash = get_md5(basepath+'/.check_columns.csv')
  if columns_hash != config['md5_indexs']:
    print(Fore.RED + 'Indexs hash not match. Abort!')
    # remove all images
    os.system('rm -rf '+imagespath)
    os.system('rm -rf '+basepath+'/.check_columns.csv')
    sys.exit(1)
  
  # Save all
  os.system('rm -rf '+basepath+'/.check_columns.csv')
  df_splitted.to_csv( basepath+'/'+config['output'])  
  print(Fore.GREEN + 'Download completed! all indexs into %s'%(basepath+'/'+config['output']))
  sys.exit(0)


