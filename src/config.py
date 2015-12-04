__author__ = 'root'
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def value(levels):
    ret = cfg[levels[0]]
    for level in levels[1:]:
        ret = ret[level]
    return ret
