class FileModel:
    def __init__(self):
        self.file_path = None

    def set_file_path(self, path):
        self.file_path = path

    def get_file_path(self):
        return self.file_path