def get_data(file):
    f = open(file, "r")
    data = f.read()
    f.close()
    return data