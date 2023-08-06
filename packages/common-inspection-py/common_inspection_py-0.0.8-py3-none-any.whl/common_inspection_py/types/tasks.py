from enum import Enum


class TaskType(Enum):
    INSPECTION_ML = 'IN_ML'
    INSPECTION_IMAGE = 'IN_IMG'
    INSPECTION_NER = 'IN_NER'
    INSPECTION_CLASSIFY = 'IN_CLS'
    TEST = 'TEST'


class TaskConfigs(Enum):
    INSPECTION_ML = './config/iml.yml'
    INSPECTION_IMAGE = './config/iimg.yml'
    INSPECTION_NER = './config/iner.yml'
    INSPECTION_CLASSIFY = './config/icls.yml'
    TEST = './config/test.yml'
