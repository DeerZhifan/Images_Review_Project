# -*- coding:utf-8 -*-
import os
from PIL import Image
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader



class MyDataset(Dataset):
    """重载Dataset，便于创建数据集"""

    def __init__(self, root):
        """获取图片路径"""
        self.imgs =[os.path.join(root, imgName) for imgName in os.listdir(root)]

    def __getitem__(self, index):
        """为图片添加标签"""
        img_path = self.imgs[index]
        if 'val' in img_path.split('\\')[-1]:
            label = 0
        else:
            label = 1
        img = Image.open(img_path).convert('RGB')
        data = self.transform(img)
        return data, label

    def __len__(self):
        """数据集长度"""
        return len(self.imgs)

    def transform(self, img):
        """将图片转换为Tensor形式的矩阵"""
        transform = transforms.Compose([
                transforms.Resize([224, 224]),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.465, 0.406], [0.229, 0.224, 0.225])
            ])
        return transform(img)


if __name__ == '__main__':
    dataset_path = 'D:/work/large'
    datasets = {x: MyDataset(os.path.join(dataset_path, x)) for x in ['train', 'val', 'test']}
    dataloader = {x: DataLoader(datasets[x], batch_size=32, shuffle=True) for x in ['train', 'val', 'test']}
    datasetSize = {x: len(datasets[x]) for x in ['train', 'val', 'test']}
    '''
    sum = 0
    for i in range(20000):
        sum += datasets['test'][i][1]
    print(sum)'''