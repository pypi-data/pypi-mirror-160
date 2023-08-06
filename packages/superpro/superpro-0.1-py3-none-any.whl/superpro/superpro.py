def load_from_dir(file_dir):
    file = open(file_dir, 'r')
    loaded = file.read()
    file.close()
    return loaded


def save_to_dir(str2save, file_dir):
    file = open(file_dir, 'w')
    file.write(str2save)
    file.close()
