import os, werkzeug.utils

def write(name : str, data : str):
	
	f = open(f"{os. getcwd()}/folderbase/{werkzeug.utils.secure_filename(name)}", 'w')
	f.write(data)
	f.close()
def write(name, data : int):
	f = open(f"{os. getcwd()}/folderbase/{werkzeug.utils.secure_filename(name)}", 'w')
	f.write(str(data))
	f.close()
def ishere(name):
	return os.path.exists(f"{os. getcwd()}/folderbase/{werkzeug.utils.secure_filename(name)}")
def read(name):
	if ishere(name):
		f = open(f"{os. getcwd()}/folderbase/{werkzeug.utils.secure_filename(name)}", 'r')
		r = f.read()
		f.close()
		return r
	else:
		return False
def delete(name):
	os.remove(f"{os. getcwd()}/folderbase/{werkzeug.utils.secure_filename(name)}")
