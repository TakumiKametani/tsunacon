import yaml
from .base import *

with open('secure.yml') as file:
    yml = yaml.load(file)
