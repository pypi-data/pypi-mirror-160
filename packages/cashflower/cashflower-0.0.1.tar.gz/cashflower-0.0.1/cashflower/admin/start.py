import os
import shutil


def startproject(project):
    current_path = os.path.dirname(__file__)
    template_path = os.path.join(current_path, 'template-project')
    shutil.copytree(template_path, project)

    return None


def addmodel(project, model):
    current_path = os.path.dirname(__file__)
    template_path = os.path.join(current_path, 'template-model')
    shutil.copytree(template_path, os.path.join(project, model))

    return None

