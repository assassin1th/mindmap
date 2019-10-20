import os
import re

def parse_image_dir (image_dir, image_format='.png'):
    images = []

    if (not image_dir.endswith ('/')):
        image_dir += '/'

    for d in os.listdir (image_dir):
        for f in os.listdir (image_dir + '/' + d):
            if (f.endswith (image_format)):
               image_path = os.path.abspath (image_dir + d + '/'  + f)
               master_name = parse_image_name (f)
               images.append ({'id' : int (d), 'image_path' : image_path, 'master_name' : master_name})
    return images

def parse_image_name (file_name):
    result = re.search (r'[А-Яа-я]+', file_name)
    return result.group (0)

if __name__ == '__main__':
    print (parse_image_dir ('../images/'))

