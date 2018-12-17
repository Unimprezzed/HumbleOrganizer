import shutil, os, sys, hashlib, time, re
import multiprocessing

def get_abspath_all_children(dir_name):
    f_list = []
    for root, dirs, files in os.walk(dir_name):
        f_list.extend([os.path.join(root, x) for x in files])
    return f_list

def sha256_hash(file, blocksize=2**20):
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            sha256.update(buf)
            buf = f.read(blocksize)
    return sha256.digest()

def get_title(filename):
    base = os.path.basename(filename)
    return base[:base.index('.')]

def normalize_title(title):
    newTitle = os.path.splitext(os.path.basename(title))[0]
    replacement_keys = {
        r'\_supplement| supplement':'',
        r'\_video| video':'',
        r'\_dvd| dvd':'',
        r'\(\d+\)':'',
        r'_\ded':'',
        r'_\d+':'',
        r'_vol\d+':'',
        r' ': '_',
        r'\_': ' '
    }

    for k,v in replacement_keys.items():
        newTitle = re.sub(k, v, newTitle)
    return newTitle.strip()

def get_file_ext(filename):
    return os.path.splitext(os.path.basename(filename))[1].upper()[1:]

if __name__ == "__main__":
    root_dir = sys.argv[1]
    dest_dir = sys.argv[2]
    print('-'*5,'ACQUIRING FILE INFORMATION','-'*5)
    file_list = [x for x in get_abspath_all_children(root_dir)]
    entries = []
    '''
    1. Get the filenames and their sizes in kilobytes. 
    2. Get the file hash for each file. 
    3. Get the unique file entries. 
    '''
    for f in file_list:
        entries.append({'file': f, 'size': round(os.path.getsize(f) / 1024), 'ext': get_file_ext(f),
                        'title': normalize_title(get_title(f))})
    entries.sort(key=lambda x: x['size'])
    print('-'*5, 'OBTAINING FILE HASHES', '-'*5)
    for i, e in enumerate(entries):
        sys.stdout.write("\rHashing {}, {} out of {}".format(e, i, len(entries) - 1))
        sys.stdout.flush()
        e['hash'] = sha256_hash(e['file'])
    sys.stdout.write('\rCOMPLETE!\n')
    sys.stdout.flush()
    unique = []
    encountered = set()
    numDuplicates = 0
    for e in reversed(entries):
        if e['hash'] not in encountered:
            unique.append(e)
            encountered.add(e['hash'])
        else:
            numDuplicates += 1
    print("{} duplicate files detected".format(numDuplicates))
    del entries
    entries = [x for x in unique]
    del unique
    #Generates the new path based on information that is already known
    print('-' * 5, 'DETERMINING FILE DESTINATIONS', '-' * 5)
    for i,e in enumerate(entries):
        sys.stdout.write("\rProcessing {}, {} out of {}".format(e, i, len(entries) - 1))
        sys.stdout.flush()
        e['destination'] = os.path.join(dest_dir, e['title'],e['ext'],os.path.basename(e['file']))
    sys.stdout.write('\rCOMPLETE!\n')
    sys.stdout.flush()
    for i,e in enumerate(entries):
        sys.stdout.write("\rMoving {}, {} out of {}".format(e, i, len(entries) - 1))
        sys.stdout.flush()
        try:
            parent_dir = os.path.dirname(e['destination'])
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            os.rename(e['file'],e['destination'])
        except FileExistsError as e:
            print('\r'+str(e))
    sys.stdout.write('\rCOMPLETE!\n')
    sys.stdout.flush()