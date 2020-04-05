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

def fix_image_paths (db):
    elems = list (map (lambda x: (x[0], x[2]), db.get_data_by_prop ('image_path')))
    for elem in elems:
        new_path = '../images'
        print (elem[1].split('\\')[-2:])
        for suffix in elem[1].split ('\\')[-2:]:
            new_path = new_path + '/' + suffix

        db.update_prop (int (elem[0]), 'image_path', new_path)

if __name__ == '__main__':
    print (parse_image_dir ('../images/'))

