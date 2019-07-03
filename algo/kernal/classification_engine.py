# -*- coding: utf-8 -*-
from algo.kernal.dataset import MyDataset
from algo.common.setting import local_config
from algo.common.logger import log

import os
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader


class ClassificationEngine(object):
    """图片分类引擎"""
    def __init__(self, image_name, model_path):
        """初始化参数"""
        self.image_name = image_name
        self.model_path = model_path

    def classifier(self, dataloader):
        """分类器"""
        log.info("加载分类模型resnet18.model......")
        model = torch.load(self.model_path, map_location='cpu')
        log.info("加载成功！")
        model.train(False)
        result = {}
        log.info("开始分类......")
        for count, data in enumerate(dataloader):
            inputs, labels = data
            outputs = model(Variable(inputs))
            _, predictions = torch.max(outputs.data, 1)
            if predictions.item() == 0:
                result[self.image_name] = 0
            else:
                result[self.image_name] = 1
        log.info("分类完毕！")
        return result


if __name__ == '__main__':
    parent_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    image_path = os.path.join(parent_path, local_config["image_path"])
    image_name = os.listdir(image_path)
    if '.DS_Store' in image_name:
        image_name.remove('.DS_Store')
    model_path = os.path.join(parent_path, local_config["model_path"])
    for name in image_name:
        datasets = MyDataset(image_path, name)
        print(datasets)
        dataloader = DataLoader(datasets, batch_size=1)
        engine = ClassificationEngine(name, model_path)
        classified_result = engine.classifier(dataloader)
        print(classified_result)
