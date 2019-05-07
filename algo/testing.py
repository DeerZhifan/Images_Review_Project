# -*- coding:utf-8 -*-

from algo.settings import Settings
from algo.dataset import MyDataset
import os
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader


class Testing(object):
    """在测试集上评估模型"""
    def __init__(self, model):
        self.model = model
        self.model.train(False)

    def test(self, dataloader, gpu, model_name):
        """计算精度、查准率、查全率和F1值"""
        TP, FP, FN, TN = 0, 0, 0, 0
        for count, data in enumerate(dataloader['test']):
            inputs, labels = data
            if gpu:
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            else:
                inputs, labels = Variable(inputs), Variable(labels)

            outputs = self.model(inputs)
            _, predictions = torch.max(outputs.data, 1)
            TP += ((predictions == 1) & (labels == 1)).sum().item()
            FP += ((predictions == 1) & (labels == 0)).sum().item()
            FN += ((predictions == 0) & (labels == 1)).sum().item()
            TN += ((predictions == 0) & (labels == 0)).sum().item()
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        F1 = 2 * recall * precision / (precision + recall)
        accuracy = (TP + TN) / (TP + FP + FN + TN)
        print('Recall = {:.2f}% || Precision = {:.2f}% || F1 = {:.2f}'.format(recall*100, precision*100, F1))
        print('\n{:s} model accuracy on test dataset is {:.2f}%'.format(model_name, accuracy*100))


if __name__ == '__main__':
    settings = Settings()
    model_name = settings.get_modelname()
    model = torch.load(model_name + '.model')
    dataset_path = settings.get_root()
    gpu = settings.get_gpu()
    batch_size = settings.get_batchsize()
    datasets = {x: MyDataset(os.path.join(dataset_path, x)) for x in ['train', 'val', 'test']}
    dataloader = {x: DataLoader(datasets[x], batch_size=batch_size, shuffle=True) for x in ['train', 'val', 'test']}
    test_engine = Testing(model)
    test_engine.test(dataloader, gpu, model_name)
