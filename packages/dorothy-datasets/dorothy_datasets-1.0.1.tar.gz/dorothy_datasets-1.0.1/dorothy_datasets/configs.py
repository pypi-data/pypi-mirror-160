
__all__ = ['get_dataset_config']

# Do not change this!
dataset_config = {

    'china' : {
        'seed'            : 512,
        'md5_indexs'      : '551e4dd43f9b3bbdb8e37b8c9133ed73',
        'output'          : 'dataset_china_splitted.csv',
        'nimages'         : 662,
        'md5_images'      : 'e690adf29a28e42d5f500de792b73e30',
        'nimages_splitted': 59580,
    },

    'imageamento' : {
        'md5'           : '',
        'output_path'   : '',
    }

}

def get_dataset_config(dataset_name):
    return dataset_config[dataset_name]
