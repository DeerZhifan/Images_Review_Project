# -*- coding: utf-8 -*-
from algo.kernal.dataset import MyDataset
import os
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader


class ClassificationEngine(object):
    """图片分类引擎"""
    def __init__(self, imgs_name, model_path):
        """初始化参数"""
        self.imgs_name = imgs_name
        self.model_path = model_path

    def classifier(self, dataloader):
        """分类器"""
        model = torch.load(self.model_path, map_location='cpu')
        model.train(False)
        index = 0
        result = {}
        for count, data in enumerate(dataloader):
            inputs, labels = data
            outputs = model(Variable(inputs))
            _, predictions = torch.max(outputs.data, 1)
            if predictions.item() == 0:
                result[self.imgs_name[index]] = 0
            else:
                result[self.imgs_name[index]] = 1
            index += 1
        return result


if __name__ == '__main__':
    imgs_path = '../images'
    imgs_name = os.listdir(imgs_path)
    if '.DS_Store' in imgs_name:
        imgs_name.remove('.DS_Store')
    model_path = 'resnet18.model'
    datasets = MyDataset(imgs_path)
    dataloader = DataLoader(datasets, batch_size=1)
    engine = ClassificationEngine(imgs_name, model_path)
    classified_result = engine.classifier(dataloader)
    print(classified_result)
