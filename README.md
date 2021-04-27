# 回報小幫手 使用手冊

統整Line群組內的回報內容，排序後顯示，並列出尚未回報人員

本服務提供給被失去4個月自由的117旅弟兄們使用。
方便協助放假在外，卻要負責統計回報人員名單的弟兄，可以快速完成統計

### 使用說明

- #### 加入回報小幫手 (本服務將於2021.04.28以後正式終止，可參考下方伺服器架設說明，自行將本服務部署在其他伺服器上使用)
掃描下方QR，將回報小幫手設為好友，並將小幫手加入群組內
<img src="https://imgur.com/NCV8xaF.jpg" style="float:left" /> 

- #### 輸入回報內容
回報小幫手加入群組後，會開始統計大家的回報內容，
請務必確保回報訊息內含有"學號姓名"四個字，以及正確的學號 => EX: 學號姓名:50090-王曉明(50090 or 090都算是正確的學號，都會視為是90號)  
任何群組內送出的訊息有包含 "學號姓名" 四個字，會被小幫手紀錄並擷取學號，
小幫手收到回報訊息以後會回復 [學號]-收到回報  
如欲更新回報內容，僅須再貼一次新的內容即可  
每天有兩個時段可回報，7:00-13:30以及14:00-22:00，這兩個時段結束後都會自動清空回報內容

| 正確回報範例                                                   |更新回報內容 | 錯誤回報範例(未輸入學號)                                       | 錯誤回報範例(文字開頭未包含"學號姓名")                         |
| -------------------------------------------------------------- | --- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| <img src="https://imgur.com/jfjAoWi.jpg" style="float:left" /> |  <img src="https://imgur.com/pwHkiyH.jpg" style="float:left" />   | <img src="https://imgur.com/iSfk9ar.jpg" style="float:left" /> | <img src="https://imgur.com/lcnvoJv.jpg" style="float:left" /> |

_*請注意，如果訊息格式正確，但不小心打到別人學號會覆蓋到別人資料。可重新輸入對方以及自己正確的學號以及訊息來更新內容。_ 


- #### 統整回報內容
輸入"統整回報"以後，小幫手會顯示目前回報狀況，如下圖  
<img src="https://imgur.com/K4H84JQ.jpg" style="float:left" />  

_*因本服務是用於統整後，方便負責統計的人貼於記事本，而記事本留言有字數上限，故本服務如偵測到統整內容超出字數上限會自動切成兩則訊息，讓負責統計的人不用手動切割統整內容。_

- #### 清空回報
如欲手動清空回報，可輸入"清空回報"，便會將小幫手統計的回報資料清除(不可恢復)  
<img src="https://imgur.com/FMB7VxN.jpg" style="float:left" />  

- #### 新增或取消退伍人員(Beta)
當班級內出現提早退伍(或是轉服其他單位志願役)的人員，可透過設定退伍人員，讓小幫手在進行統整回報時，自動忽略  
輸入"設定退伍人員:[學號[,學號...]]" ，及會將這些學號列入退伍人員名單  
如需將人員從退伍名單中移除，則輸入"取消退伍人員:[學號[,學號...]]"
| 設定退伍人員前  | 設定退伍人員完成後 | 取消退伍人員 |
| -------------------------------------------------------------- | -------------------------------------------------------------- | --- |
| <img src="https://imgur.com/RwStzZf.jpg" style="float:left" /> | <img src="https://imgur.com/MKkJoRi.jpg" style="float:left" /> |   <img src="https://imgur.com/UJmiVUw.jpg" style="float:left" />  |

- #### 恢復初始設定
如出現小幫手異常，可透過恢復初始設定，來重設小幫手
該操作會清空回報內容以及退伍人員名單
輸入"恢復初始設定"，即可重設小幫手(不可恢復)
<img src="https://imgur.com/AGxo4JQ.jpg" style="float:left" />

- #### 過年祝賀彩蛋
如果跟小幫手說"新年快樂"
他會回復你:)

### 伺服器架設說明

- #### 私人伺服
架設 Line 的後端伺服器可大致分為兩種方式: (1)架設私人伺服器或(2)架設商業雲端平台 (Heroku)
以下列舉兩種架設方式的優缺點  
|     | 私人伺服器 | 商業雲端平台 |
| --- | ---------- | ------------ |
| 優點 | 好Debug、方便管理資料庫、可快速更改設定 | 部署快速簡單、有免費方案 |
|缺點 | 架設複雜、成本高(機器、電力) | 不易Debug、會自動進入休眠模式 |


本服務目前是架設於私人伺服器，因此概略介紹大致部署流程  
- 建立 Provider  
到[Line Developer 官網](https://developers.line.biz/console/)用自己的Line帳號建立Provider，可參考網路[相關文章](https://github.com/yaoandy107/line-bot-tutorial#%E5%89%B5%E5%BB%BA-line-bot-%E9%A0%BB%E9%81%93)建立- 

- 為自己的伺服器IP位址申請Domain Name(網域名稱)  
看大家是否有自己的Domain Name或是還是學生的話，可以用[Github Education Pack](https://education.github.com/pack/offers) 在[NameCheap](https://www.namecheap.com/cart/addtocart.aspx?producttype=ssl&product=positivessl&action=purchase&period=1-YEAR&qty=1) 免費申請一個(一年)

- 獲得SSL憑證
為自己的Domain Name申請SSL憑證  
其中Line要求的SSL憑證需要由有認證的機構發出(無法使用python自行產生)，同樣也可以到[NameCheap](https://www.namecheap.com/cart/addtocart.aspx?producttype=ssl&product=positivessl&action=purchase&period=1-YEAR&qty=1) 免費申請一個(一年)

- 設定Token 以及 Secret
新增一個檔案取名為token.yml，並將LINE的Token以及secret新增在裡面，格式如下  
```
millitary_report_helper: 
  token: [YOUR LINE TOKEN]
  secret: [YOUR LINE Secret]
```

- 將自己申請的Domain Name 與 Line 綁訂
將自己的Domain Name填入自己新增的LINE Provider 的webook URL，如下  
https://imgur.com/OckfG3h

接著將程式啟動後就完成了
另外也可參考網路[相關文章](https://github.com/yaoandy107/line-bot-tutorial)，利用Heroku將服務部署在雲端上

