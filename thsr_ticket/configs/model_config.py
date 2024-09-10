import json
import pathlib
 
 
def load_config():
    #建立可能出現的驗證碼字元集
    source = [str(i) for i in range(0, 10)]
    #source += [chr(i) for i in range(97, 97+26)] #高鐵驗證碼只有大寫區分，故可以去掉小寫英文
    source += [chr(i) for i in range (65,65+26)]
    alphabet = ''.join(source)
    #幾碼驗證碼
    conf_len=4
    #輸出模型檔名
    conf_mdname='thsr_ticket/ml/checkpoints/model_thsrc.pth'
    #圖片寬
    conf_w=48
    #圖片高
    conf_h=140
    ##########
    conf_set=len(alphabet)
    mconfig={}
    mconfig={'conf_set':conf_set,'alphabet':alphabet,'conf_len':conf_len, 'conf_mdname':conf_mdname,'conf_w':conf_w,'conf_h':conf_h}
    return mconfig