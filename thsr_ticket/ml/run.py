import torch
import torch.nn as nn
from ml.Testmodel import CNN
from ml.datasets import CaptchaData
from torchvision.transforms import Compose, ToTensor
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import configs.model_config as model_config #模型設定參數py, 下面有code
 
#讀取本次模型的相關設定參數
conf=model_config.load_config()
conf_set=conf['conf_set']
conf_len=conf['conf_len']
conf_w=conf['conf_w']
conf_h=conf['conf_h']
alphabet=conf['alphabet']
conf_mdname=conf['conf_mdname']
 
 
def run(img):
    img_li = list()
    label_li = list()
    # print(img_list)
    # img = Image.open(imgpath)
    trans = ToTensor()
    img_tensor = trans(img)
    cnn = CNN()
    if torch.cuda.is_available():
        cnn = cnn.cuda()
        cnn.eval()
        cnn.load_state_dict(torch.load(conf_mdname))
    else:
        cnn.eval()
        model = torch.load(conf_mdname, map_location='cpu')
        cnn.load_state_dict(model)
    img_tensor = img_tensor.view(1, 3, conf_w, conf_h)
    output = cnn(img_tensor)
    output = output.view(-1, conf_set)
    output = nn.functional.softmax(output, dim=1)
    output = torch.argmax(output, dim=1)
    output = output.view(-1, conf_len)[0]
    label = ''.join([alphabet[i] for i in output.cpu().numpy()])
    print (label)
    return label
 
if __name__=="__main__":
    run()