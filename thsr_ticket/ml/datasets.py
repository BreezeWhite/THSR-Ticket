from PIL import Image
from torchvision import transforms
import torch
from torch.utils.data import Dataset
import os
import pandas as pd
import configs.model_config as model_config
 
 
conf=model_config.load_config()
conf_set=conf['conf_set']
conf_len=conf['conf_len']
alphabet=conf['alphabet']
 
def img_loader(img_path):
    img = Image.open(img_path)
    resize2 = transforms.Resize([48, 140])
    img = resize2(img)
    img.save(img_path)
    return img.convert('RGB')
 
def make_dataset(data_path, alphabet, num_class, num_char):
    # img = os.listdir(data_path)
    # key=lambda x: int(x.split('.')[0])
    # img.sort(key=lambda x: int(x.split('.')[0]))
    # #print(img)
    # df = pd.read_csv("./label.csv")
    # #print (df)
    # 上面我註解起來，是適用 PIC+label.csv的方式來讀取data, 但高鐵本篇範例我沒有做csv，所以採用下面方式讀取data
    img = os.listdir(data_path)
    info_list_id = [x for x in img ]
    info_list_label = [x.split('_')[1].split('.')[0]  for x in img ]
    #檢查label
    #print (info_list_label)
    for k in info_list_label:
        if len(k)!=num_char:
            print (k)
            info_list_label=info_list_label.remove(k)
    df=pd.DataFrame(
    {'ID': info_list_id,
     'label': info_list_label,
    })
    samples = []
    k=0
    for imgname in img:
        imgpath = os.path.join(data_path, imgname)
        label = df['label'][k]
        k+=1
        target = []
        for char in label:
            vec = [0] * num_class
            vec[alphabet.find(char)] = 1
            target += vec
        samples.append((imgpath, target))
    return samples
 
 
class CaptchaData(Dataset):
    #num_char分别表示字符的總量和一張圖片中的字符數量，分别為62和4。
    def __init__(self, data_path, num_class=conf_set, num_char=conf_len,
                 transform=None, target_transform=None, alphabet=alphabet):#62,4
        super(Dataset, self).__init__()
        self.data_path = data_path
        self.num_class = num_class
        self.num_char = num_char
        self.transform = transform
        self.target_transform = target_transform
        self.alphabet = alphabet
        self.samples = make_dataset(self.data_path, self.alphabet,
                                    self.num_class, self.num_char)
     
    def __len__(self):
        return len(self.samples)
     
    def __getitem__(self, index):
        img_path, target = self.samples[index]
        img = img_loader(img_path)
        if self.transform is not None:
            img = self.transform(img)
        if self.target_transform is not None:
            target = self.target_transform(target)
        return img, torch.Tensor(target)