# -*- coding: utf-8 -*-
from model import  Model
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau


class Settings():
    """设置参数"""
    def __init__(self):
        self.root = 'D:/work/large'
        self.model_name = 'resnet18'
        self.loss_function = 'criterion'
        self.optimizer = 'SGD'
        self.batch_size = 32
        self.learning_rate = 0.001
        self.lr_scheduler = True
        self.momentum = 0.9
        self.gpu = True
        self.epoches = 20

    def get_root(self):
        """返回数据集路径"""
        return self.root

    def get_modelname(self):
        """返回模型名称"""
        return self.model_name

    def get_model(self):
        """返回模型"""
        model = Model()
        if self.model_name == 'vgg11':
            return model.vgg11()

        if self.model_name == 'vgg13':
            return model.vgg13()

        if self.model_name == 'vgg16':
            return model.vgg16()

        if self.model_name == 'vgg19':
            return model.vgg19()

        if self.model_name == 'resnet18':
            return model.resnet18()

        if self.model_name == 'resnet34':
            return model.resnet34()

        if self.model_name == 'resnet50':
            return model.resnet50()

    def get_lossfunction(self):
        """返回损失函数"""
        if self.loss_function == 'criterion':
            return nn.CrossEntropyLoss()

        if self.loss_function == 'MSELoss':
            return nn.MSELoss()

    def get_optimizer(self, model):
        """返回优化方法"""
        if self.optimizer == 'SGD':
            return optim.SGD(model.parameters(), self.learning_rate, self.momentum)
        if self.optimizer == 'Adam':
            return optim.Adam(model.parameters(), self.learning_rate, self.momentum)

    def get_batchsize(self):
        """批处理大小"""
        return self.batch_size

    def get_lrscheduler(self,model):
        """返回学习率调整函数"""
        return ReduceLROnPlateau(self.get_optimizer(model), 'min', factor=0.5, patience=3, verbose=True)

    def get_gpu(self):
        """返回GPU状态"""
        return self.gpu

    def get_epoches(self):
        """返回迭代次数"""
        return self.epoches


