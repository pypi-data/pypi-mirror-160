import os


class CCIO:

    @staticmethod
    def read_string(file_name):
        if os.path.isfile(file_name):
            with open(file_name) as f:
                lst = f.read()
                return lst
        else:
            return None

    @staticmethod
    def save_string(string, file_name):
        dir_path = os.path.dirname(file_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_name, "w") as f:
            f.write(string)
