import nibabel as nib


class TrkFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.header = None
        self.streamlines = None
        self.load_trk_file()

    def load_trk_file(self):
        trk_file = nib.streamlines.load(self.file_path)
        self.header = trk_file.header
        self.streamlines = trk_file.streamlines

    def get_header(self):
        return self.header


# Example usage:
# handler = TrkFileHandler('/path/to/your/file.trk')
# header = handler.get_header()
# print(header)
