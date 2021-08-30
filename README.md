# Azure_linebot 發票辨識系統  
透過Azure表格辨識系統訓練不管是傳統發票還是電子發票只要拍下照片都能輕鬆兌獎  
## 專案流程:  
![image](https://user-images.githubusercontent.com/58453878/131366269-06585144-eae6-4690-abb0-0570642cc62a.png)

## 專案製作流程
1. 透過爬蟲先將財政部每個月兌獎資訊爬取下來,並存入mongodb,
選擇Mongodb原因則是因為每期特別號數量不同,並撰寫讀取API  //程式碼參考:model/selectdb.py , //爬蟲: ./ETL_etax.py
2. 利用Azure 表單辨識訓練器訓練模型,使能成功辨識發票訓練完成透過金鑰連結
3. 撰寫兌獎邏輯 //程式碼參考:model/receipt.py
4. 撰寫linebot api //程式碼參考: ./Linebot.py

## 實際執行畫面
![image](https://user-images.githubusercontent.com/58453878/131368389-5aff464d-af4f-4d53-bbf8-ee94ac45b32f.png)
