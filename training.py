# -*- coding:utf-8 -*-
from dataset import MyDataset
from settings import Settings
import os
import time
import copy
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader


class Training():
    """训练模型"""
    def __init__(self, dataloader, datasetSize, model, loss_function, optimizer, lr_scheduler, gpu, epoches):
        """设置初始参数"""
        self.dataloader = dataloader
        self.datasetSize = datasetSize
        self.model = model
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.gpu = gpu
        self.epoches = epoches

    def train(self):
        """训练模型"""
        since = time.time()
        best_model = self.model
        best_acc = 0
        for epoch in range(self.epoches):
            for phase in ['train', 'val']:
                if phase == 'train':
                    self.model.train(True)
                else:
                    self.model.train(False)
                running_loss = 0
                running_corrects = 0
                for _, data in enumerate(self.dataloader[phase]):
                    inputs, labels = data
                    if self.gpu:
                        inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                        self.model = self.model.cuda()
                    else:
                        inputs, labels = Variable(inputs), Variable(labels)
                    self.optimizer.zero_grad()
                    outputs = self.model(inputs)
                    _, predictions = torch.max(outputs.data, 1)
                    loss = self.loss_function(outputs, labels)
                    if phase == 'train':
                        loss.backward()
                        self.optimizer.step()

                    running_loss += float(loss.data)
                    running_corrects += torch.sum(predictions == labels.data).item()
                    # print(running_loss, running_corrects)
                epoch_loss = running_loss / self.datasetSize[phase]
                epoch_acc = running_corrects / self.datasetSize[phase]
                print('Epoch: {:} || {:} loss: {:.4f} || acc: {:4f}'.format(epoch, phase, epoch_loss, epoch_acc))
                if phase == 'val':
                    self.lr_scheduler.step(epoch_loss)
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model = copy.deepcopy(self.model)
        time_elapsed = time.time() - since
        m, s = divmod(time_elapsed, 60)
        h, m = divmod(m, 60)
        print('\nTraining complete in {:.0f}h {:.0f}m {:.0f}s'.format(h, m, s))
        print('\nBest val accuracy: {:.2f}%'.format(best_acc * 100))
        return best_model


if __name__ == '__main__':
    settings = Settings()
    dataset_path = settings.get_root()
    model_name = settings.get_modelname()
    model = settings.get_model()
    loss_function = settings.get_lossfunction()
    optimizer = settings.get_optimizer(model=model)
    gpu = settings.get_gpu()
    batch_size = settings.get_batchsize()
    lr_scheduler = settings.get_lrscheduler(model=model)
    epoches = settings.get_epoches()
    datasets = {x: MyDataset(os.path.join(dataset_path, x)) for x in ['train', 'val', 'test']}
    dataloader = {x: DataLoader(datasets[x], batch_size=batch_size, shuffle=True) for x in ['train', 'val', 'test']}
    datasetSize = {x: len(datasets[x]) for x in ['train', 'val', 'test']}
    train_engine = Training(dataloader, datasetSize, model, loss_function, optimizer, lr_scheduler, gpu, epoches)
    trained_model = train_engine.train()
    with open(model_name + '.model', 'wb') as f:
        torch.save(trained_model, f)
