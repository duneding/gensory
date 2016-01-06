# -*- coding: utf-8 -*-

from monkeylearn import MonkeyLearn

ml = MonkeyLearn('e8eae74a9f2d5f20d01e91ca3bc4bfbfadbe4322')
module_id = 'cl_9mso8PPo'

text_list = [
    u'Por obras, la #LíneaC prestará servicio entre las estaciones Constitución y Gral. San Martín hasta el 31/1: ',
    u'#Subte Línea D | Comenzó a regularizar su servicio.'
]

res = ml.classifiers.classify(module_id, text_list, sandbox=True)

print res.result