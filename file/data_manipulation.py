# -*- coding: utf-8 -*-
import json
import pandas as pd
# import re

# 讀取json檔
# C:\\Users\\吳金擇\\Desktop\\PTT-Analysis\\file\\rawdata.json
with open('rawdata.json', 'r', encoding="utf-8") as f:
    data = json.loads(f.read())

# 建立list用以儲存json所需欄位
all_list = []
for i in range(len(data)):
    all_list.append([data[i]['a_ID'], data[i]['b_作者'],
                     data[i]['c_標題'], data[i]['d_日期'],
                     data[i]['e_ip'], data[i]['h_推文總數']['all'],
                     data[i]['f_內文']])

# 以list建立datafram，以方便後續繪圖
buy2df = pd.DataFrame(all_list, columns=['id','author','title','date','ip','likes','content'])


# 建立年月週資料
buy2df['year'] = buy2df['date'].apply(lambda x: x[20:24])
buy2df['month'] = buy2df['date'].apply(lambda x: x[4:7])
buy2df['week'] = buy2df['date'].apply(lambda x: x[0:3])

# 排除無法使用資料(星期正常，就不再處理)
yearlist = ['2020','2019','2018','2017','2016',
            '2015','2014','2013','2012','2011','2010']
buy2df = buy2df[buy2df['year'].isin(yearlist)]
                
monlist = ['Jan','Feb','Mar','Apr','May',
           'Jun','Jul','Aug','Sep','Oct',
           'Nov','Dec']
buy2df = buy2df[buy2df['month'].isin(monlist)]


# 排除無法使用資料
df = buy2df[(buy2df.author!='no author')|
            (buy2df.content!='main_content error')]

# 去除作者欄位暱稱
df['author'] = df.author.str.split(" ", n=1, expand=True)


# ---------------------------
# 製作"商品分類"欄位
# ---------------------------
d = {'衣飾':['衣', '裙', '鞋', '包', '背心', '手套', '袋', '圍巾', '褲', '外套', '靴', '帽', '襪子', '衫', 'Tshirt', 'bra', '圍脖', '斗篷',
             '絲巾', '洋裝', '飾', '鍊', 'T恤', '帽t', '皮夾', '手環', '髮', '襪', '腰帶', '皮帶', '綁帶', '手帕', '戒指', '領巾', 'Gucci',
             '純棉', 'ASOS', 'asos', 'SHOPBOP', 'Shopbop', 'shopbop', '耳環', '分趾套', '玉如阿姨', '胸', '毛巾', '泳裝', '袖', '旗袍', '套裝', '童裝',
             '西裝', '女裝', '牛仔', '墨鏡', '針織', 'yourz', 'adidas', '西服', 'La Brisa Shoes', '肩帶'], 
     '彩妝保養':['霜', '美妝', '寶水', '眼影', '粉餅', '口紅', '腮紅', '眼線', '卸妝', '面膜', '保濕', '離子夾', '電棒捲', '電捲棒', '髮', '梳',
             'makeup', '睫毛', '護髮', '粉刺', '洗卸', '遮瑕', '保養', '絲瓜水', '噴霧', '指甲油', '化妝', 'DHC', 'ORBIS', '止汗膏',
             '露', '身體乳', '精油', '唇', '膏', 'sigma', 'Sigma', 'SIGMA', 'orbis', 'Orbis', '刷具', '雙眼皮', '杏仁酸', '彩妝', '香水', '荷芭油', '液',
             '痘痘', '蜜粉', '小三美日', '指緣油', '醒寤', '粉底', '膚', '康是美', '防護乳', '蘆薈', '打亮', '美白', '自拍', '美甲', 'Beautylish',
             '慕斯', '指甲', '芳療', '妝', 'goodness bad', '控油'],
     '食物':['茶', '食', '赫而司', '生乳捲', '包子' '饅頭', '火鍋', '料理', '可可', '奶', '蛋', '蔬菜', '葉黃素', '豬腳',
             '米', '麵', '禮盒', '氣泡水', '生鮮', '餅', '水餃', '錠', '海苔', '櫻桃', '布丁', '地瓜', '芒果', '酒', '維他命',
             '哈根達斯', '辣椒', '泡菜', '咖啡', '草莓', '菌', '魚', '餃', '檸檬塔', '膠囊', '堅果', '全家', '鳳梨', '吐司', '麻糬',
             '雞', '大福', '汁', '杏仁', '甜點', '貝果', '派', '泡芙', '烘焙', '果醬', '福義軒', '冰', '濃湯', 'iherb', '巧克力', '蘿蔔', '橄欖', '糖',
             '蔬果', '果乾', '飲', '豆腐', '優格', '檸檬', '蕉', '蠶豆', '舒芙蕾', '起司', '鳳', '薑', '亞尼克', '蕃茄', '菓子', '金皮油', '梅', '膳纖'],
     '電子周邊':['充電', '智慧', '線', '膜', '手機', '耳機', '麥克風', '鋼化膜', '相機', '鏡頭', '投影機', '玻璃貼', 'IPhone',
                 '廣角', '保護', 'DVD', '電腦', '行動電源', '電池', '平板', 'SIM卡', 'sim卡', '插座'],
     '生活五金':['口罩', '盒', '牙刷', '衛生棉', '墊', '收納', '架', '杯', '吸管', '錶', '枕', '燈', '餐具', '椅', '床', '吹風機',
                 '抹布', '掃把','棉花棒', '拖把', '吸塵器', '衛生紙', '櫃', '摺疊', '袋', '洗髮', '沐浴', '防曬', '眼鏡','無患子',
                 '傘', '蓮蓬頭', '被', '桶', '筷', '器', '機', '行李箱', '浴巾', '皂', '快煮壺', '夾腳拖', '罐', '行李', '水瓶',
                 '大創', '眼罩', '鍋', '噴油瓶', '腰靠', '去汙', '風扇', '除油', '蠟燭', '洗碗', '盤', '浴', '泡泡', '地毯', '瓶', '水壺',
                 '按摩', '迪卡儂', '簾', '螺絲', '水管', '除味', '紙巾', '洗面乳', '桌', '車', '盆', '保溫瓶', '掛勾', '丸龜製套', '疏通粉',
                 '塵蟎', '愛康', '毯', '便當', 'IKEA', '碗', '沙發', '鐘', '除濕', '棉條', '清潔', '霉', '黏土', '壁貼', '沙發', '耳塞', 'X-bike', '尿布', '臂套',
                 '放大鏡', '地板', '山姆伯伯', '抽屜', '手巾', '家用品', 'XBike'],
     '網路app':['netflix', 'youtube', '網路', '網', '任天堂', 'Microsoft', 'Spotify', '會員', 'spotify', 'Netflix', 'office', 
                'Office', '軟體', 'Apple Music', 'Apple music', 'Youtube', '系統', 'Youtube Premium', 'Photoshop', '貼圖'],
     '文物':['文具', '筆', '印章', '地圖', '手帳', '年曆', '桌曆', '月曆', '姓名貼', '積木', '娃娃', '玩偶', '膠帶', '明信片', '刀', 
             '書', '雜誌', '洗護', '日曆', '標籤', '紙', '桌遊', '公仔', '繪本', '手繪', '拼圖', '護照', '玩具', '種籽設計', '套卡', '章', '底片'
             ,'相簿', '計劃本', '油畫', '攝影', '相冊', 'DIY', '卡片', 'WOOD', '漫畫', '小說'],
     '寵物':['飼料', '貓', '狗', '寵物', '寵', '藝'],
     '票券':['券', '來回', '交通', '票', '優惠', '團報', '卷', '課', '飯店', '岩盤美浴', '方案', '溫泉', 'yoga', '師大', '療程']}
# 全改為小寫，以方便對照
df['title'] = df['title'].str.lower()
for i in d.keys():
    for j in range(len(d[i])):
        d[i][j] = d[i][j].lower()

# 建立關鍵字清單，並以長度做排序
keyword = []
for i in d.keys():
    for j in range(len(d[i])):
        keyword.append((i, d[i][j]))
keyword = sorted(keyword, key=lambda x: len(x[1]),reverse=True)

# 定義分類函數
def producttype(title):
    for i in range(len(keyword)):
            if title.find(keyword[i][1]) > 0:
                return keyword[i][0]
    return '其他'

# 將分類函數套用至df
df['product'] = df['title'].apply(lambda x: producttype(x))

# ---------------------------
# 製作"bank"欄位
# ---------------------------
b = {'郵局':['郵局', '中華郵政', '郵政'], 
     '台新':['台新', 'richart', 'TSBank', 'TSIB'],
     '中信':['中信', '中國信託', 'CTBC'],
     '臺銀':['台銀' '臺銀', '台灣銀行', '臺灣銀行'],
     '合庫':['合庫', '合作金庫'],
     '彰銀':['彰銀', '彰化銀行'],
     '臺灣企':['臺灣企'], '國泰':['國泰'], '土銀':['土銀'], '第一':['第一'],
     '華南':['華南'], '上海銀':['上海'], '富邦':['富邦'], '兆豐':['兆豐'],
     '匯豐':['匯豐'], '華泰':['華泰'], '陽信':['陽信'], '聯邦':['聯邦'],
     '玉山':['玉山'], '凱基':['凱基'], '星展':['星展'],
     }
# 全改為小寫，以方便對照
df['content'] = df['content'].str.lower()
for i in b.keys():
    for j in range(len(b[i])):
        b[i][j] = b[i][j].lower()

# 建立bank清單，並以長度做排序
bank = []
for i in b.keys():
    for j in range(len(b[i])):
        bank.append((i, b[i][j]))

# 定義銀行函數
def banktype(content):
    for i in range(len(bank)):
            if content.find(bank[i][1]) > 0:
                return bank[i][0]
    return '其他'

# 將分類函數套用至df
df['bank'] = df['content'].apply(lambda x: banktype(x))

df.to_csv(r'rawdata.csv', index=False)

         