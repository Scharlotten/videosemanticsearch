import pickle
def save(file_name, obj):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj)

def load(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)