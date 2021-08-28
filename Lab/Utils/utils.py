import os
import yaml

def get_dir_names(path_training_images):
    return [dI for dI in os.listdir(path_training_images) 
        if os.path.isdir(os.path.join(path_training_images,dI))]

def update_project_id_config (config_path,project_id):
    fd=open(config_path,"r")
    d=fd.read()
    fd.close()
    m=d.split("\n")
    s="\n".join(m[:-1]) + "\n  ProjectID: " + project_id
    fd=open(config_path,"w+")
    for i in range(len(s)):
        fd.write(s[i])
    fd.close()

def project_path():
    cwd = os.getcwd()
    project_dir =os.path.abspath(os.path.join(cwd, os.path.join(os.pardir, os.pardir)))
    return project_dir

def load_configs(relative_path):
    config_file = os.path.join(project_path(), relative_path)

    with open(config_file, 'r') as ymlfile:
        return yaml.load(ymlfile, Loader=yaml.FullLoader)

def get_project_dir():
    return os.path.abspath(os.path.join(os.getcwd(), os.path.join(os.pardir, os.pardir)))

