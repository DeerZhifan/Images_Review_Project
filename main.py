# -*- coding: utf-8 -*-
from dataset import MyDataset
import torch
from PIL import Image
from torchvision import transforms
from torch.autograd import Variable
from torch.utils.data import DataLoader


class Main():
    """图片审核程序主入口"""
    def __init__(self, img_path, img_name, model_name):
        """初始化参数"""
        self.img = Image.open(img_path + '/' + img_name).convert('RGB')
        self.img_name = img_name
        self.model_name = model_name

    def isAutoParts(self, dataloader):
        """是否配件配件"""
        model = torch.load(self.model_name + '.model', map_location='cpu')
        for count, data in enumerate(dataloader):
            inputs, labels = data
            print(inputs.shape)
            outputs = model(Variable(inputs))
            _, predictions = torch.max(outputs.data, 1)
            print(predictions)
            if predictions.item() == 0:
                print("{:} is not a autoparts".format(self.img_name))
            else:
                print("{:} is a autoparts".format(self.img_name))

    def transform(self, img):
        """将图片转换为Tensor形式的矩阵"""
        transform = transforms.Compose([
                transforms.Resize([224, 224]),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.465, 0.406], [0.229, 0.224, 0.225])
            ])
        return transform(img)


if __name__ == '__main__':
    img_path = '/users/vita/desktop/tes'
    img_name = 'test5.jpeg'
    model_name = 'resnet18'
    datasets = MyDataset(img_path)
    dataloader = DataLoader(datasets, batch_size=1, shuffle=True)
    engine = Main(img_path, img_name, model_name)
    engine.isAutoParts(dataloader)
