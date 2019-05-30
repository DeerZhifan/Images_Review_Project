# -*- coding:utf-8 -*-
import torchvision.models as models


class Model(object):
    """加载PyTorch中的模型"""

    def vgg11(self):
        return models.vgg11_bn(pretrained=True)

    def vgg13(self):
        return models.vgg13_bn(pretrained=True)

    def vgg16(self):
        return models.vgg16_bn(pretrained=True)

    def vgg19(self):
        return models.vgg19_bn(pretrained=True)

    def resnet18(self):
        return models.resnet18(pretrained=True)

    def resnet34(self):
        return models.resnet34(pretrained=True)

    def resnet50(self):
        return models.resnet50(pretrained=True)


#if __name__ == '__main__':
    #model = Model()
    #vgg11 = model.vgg11()
