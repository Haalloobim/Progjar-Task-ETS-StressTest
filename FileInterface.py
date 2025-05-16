import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('uploads/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}", 'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))
        
    def add(self, params=[]):
        try:
            paramsCount = len(params)
            filename = params[0]
            
            if (paramsCount < 2 or filename == ''):
                return dict(status='ERROR', data="Parameter tidak lengkap")

            fileContent = base64.b64decode(params[1])
            
            file = open(filename, 'wb+')
            file.write(fileContent)
            file.close()
            
            checkFileWritten = os.path.exists(filename)
            
            if checkFileWritten:
                return dict(status='OK', data=f"File {filename} berhasil diupload")
            else:
                return dict(status='ERROR', data=f"File {filename} gagal diupload")
            
        except Exception as e:
            return dict(status='ERROR', data=str(e))
    
    def delete(self, params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return dict(status='ERROR', data="Parameter tidak lengkap")
            
            os.remove(filename)
            
            checkFileDeleted = os.path.exists(filename)
            
            if checkFileDeleted:
                return dict(status='ERROR', data=f"File {filename} gagal dihapus")
            
            return dict(status='OK', data=f"File {filename} berhasil dihapus")
        except Exception as e:
            return dict(status='ERROR', data=str(e))



if __name__=='__main__':
    f = FileInterface()
    print(f.list())