# III. [超啟發式演算法（Meta-heuristic Algorithm）](https://tzuchieh0931.medium.com/introduction-metaheuristic-01-e2a598123c6f)
超啟發式演算法不會將解遍歷所以可以節省大量的時間成本；如果遇到解空間很大的問題，可以以較為快速的方式找到一個可接受的結果（有可能解空間大到無法遍歷），像是01背包問題、旅行銷售員問題（TSP）、排程問題、函數最佳化、甚至是深度學習的超參數調整都可以使用超啟發式演算法的方式來解決。<br>

## (1)	動態規劃(Dynamic programming)
把原問題分解為相對簡單的子問題的方式求解複雜問題的方法，<br>
將子問題的答案記錄下來，當下一回來用到前一回合答案時就直接查表，<br>
也可以說是一種用空間換取時間的解題方式。<br>

## STEP 0 讀 txt 檔 初始化 0/1 Knapsack 參數
```=python
file = open('p07_p.txt', 'r')
    for line in file.readlines():
        p.append(int(line))
    file.close
```
![](https://i.imgur.com/BDu9Vb6.jpg)

## STEP 1 建表 answer table
利用 array : dp 紀錄每個子問題的解，取得最佳解
```
# answer table array
dp = np.array([[0 for _ in range(背包限重容量+1)] for _ in range(物品數+1)])
```

![](https://i.imgur.com/cbbklyz.jpg)
![](https://i.imgur.com/WcoVOKU.jpg)


## STEP 2 回推拿取那些物品
![](https://i.imgur.com/iD5UJe4.jpg)
![](https://i.imgur.com/W0XNUDJ.jpg)

另起一個 s[ ] 數組，s[i]=0表示不拿，s[i]=1表示拿 <br>
dp[i][c]為最優值，如果dp[i][c]=dp[i-1][c] , 說明有沒有第i件物品都一樣，則s[i]=0 ; 否則 s[i]=1。<br>
當s[i]=0時，由s[i-1][c]繼續構造最優解；<br>
當s[i]=1時，則由s[i-1][c-w[i]]繼續構造最優解。<br>



## STEP 3 印出並匯出 answer table 成 csv 檔
```
solution_table.to_csv('solution_table.csv')
```
![](https://i.imgur.com/htHnZI7.jpg)

## (2)	[爬山演算法(Hill climbing, HC)](https://tzuchieh0931.medium.com/hc-metaheuristic-02-a071980b37e6)

## STEP 0 讀 txt 檔 初始化 0/1 Knapsack 參數
```=python
file = open('p07_p.txt', 'r') 
    for line in file.readlines(): 
        p.append(int(line)) 
    file.close 
```   
![](https://i.imgur.com/BDu9Vb6.jpg)

## STEP 1 Initial:
隨機產生出一組合法解 : 依物品數隨機產生 0/1 長度的陣列 <br>
物品 不拿: 0 拿: 1 <br>
```=python
item_status = [ random.randint(0,1) for _ in range(物品數)] 
```

需檢查隨機拿或不拿的 0 / 1 陣列組合 總重 < Capacity <br>

## STEP 2 Transition: 隨機 / 左右 移動 

找鄰近解方法:<br>

### (1)隨機移動: 將隨機一位置 0換成 1 1換成 0 <br>
ex. [ 1,1,0,0 ] 的鄰近解 : [ 0,1,0,0 ] 、 [ 1,0,0,0 ] 、 [ 1,1,1,0 ] 、 [ 1,1,0,1 ]<br>
即隨機找一物品，若原本在背包則從背包中拿出，若原本不在背包則放進背包<br>

### (2)左右移動: 將隨機任兩不同值位置 0、1對調<br>
ex. [ 1,1,0,0 ] 的鄰近解 : [ 0,1,1,0 ] 、 [ 0,1,0,1 ] 、 [ 1,0,1,0 ] 、 [ 1,0,0,1 ]<br>
即隨機找兩物品，一個已在背包中，一個不在背包中，將原本不在背包的放入背包，同時將放回原本在背包的物品。<br>

程式採 **(2)左右移動** 的方法找鄰近解<br>
過程需檢查是否符合 合法解 ( 總重 < Capacity )，若不符合則 while 迴圈取新鄰近解。<br>

## STEP 3 Evalution: 評估適應值(Fitness value)大小
計算鄰近解的獲利 ( Profit )<br>

## STEP 4 Determination: 
鄰近解的獲利 ( Profit )和現解的獲利 ( Profit )比較，<br>
鄰近解的獲利 ( Profit ) 較高，即更新現解成鄰近解 ;<br>
鄰近解的獲利 ( Profit ) 較低，則維持現解。<br>

重複 STEP2 ~ STEP4 的步驟，直到迭代完 500 次停止。<br>

## STEP 5 畫出 500次 迭代( iteration )的收斂圖
![](https://i.imgur.com/ayyBqTG.jpg)



## (3)	[模擬退火演算法(Simulated annealing, SA)](https://tzuchieh0931.medium.com/sa-metaheuristic-03-2632b2047d1f)
改善 爬山演算法 (Hill climbing, HC)，可能卡在 區域最佳解(Local optimum) 無法跳脫找到更佳的解 達到 全域最佳解(Global optimum)<br>
slove : 一定的機率接受較差的解，以此增加跳脫出區域最佳解的機會<br>

![](https://i.imgur.com/08wlRqQ.jpg)

## STEP 0 讀 txt 檔 初始化 0/1 Knapsack 參數 及 退火環節參數
### (1)初始化 0/1 Knapsack 參數
```=python
file = open('p07_p.txt', 'r') 
    for line in file.readlines(): 
        p.append(int(line)) 
    file.close 
```
![](https://i.imgur.com/BDu9Vb6.jpg)

### (2)退火環節參數
初始溫度(T) 退火溫度 : current_temperature = 200.0<br>
讓初始允許機率達0.8 (較高機率接受差值)<br>

![](https://i.imgur.com/0xp1E6Y.jpg)

退火係數(Rₜ) = 0.95 (降溫不要降太快故設0.95)<br>
退火係數(Rₜ)越小，降溫(T)越快，允許機率越快歸0，解收斂越快。<br>
    
## STEP 1 Initial:
隨機產生出一組合法解 : 依物品數隨機產生 0/1 長度的陣列 <br>
物品 不拿: 0 拿: 1 <br>
```=python
item_status = [ random.randint(0,1) for _ in range(物品數)] 
```
需檢查隨機拿或不拿的 0 / 1 陣列組合 總重 < Capacity <br>

## STEP 2 Transition: 隨機 / 左右 移動 

找鄰近解方法:<br>

### (1)隨機移動: 將隨機一位置 0換成 1 1換成 0 <br>
ex. [ 1,1,0,0 ] 的鄰近解 : [ 0,1,0,0 ] 、 [ 1,0,0,0 ] 、 [ 1,1,1,0 ] 、 [ 1,1,0,1 ]<br>
即隨機找一物品，若原本在背包則從背包中拿出，若原本不在背包則放進背包<br>

### (2)左右移動: 將隨機任兩不同值位置 0、1對調<br>
ex. [ 1,1,0,0 ] 的鄰近解 : [ 0,1,1,0 ] 、 [ 0,1,0,1 ] 、 [ 1,0,1,0 ] 、 [ 1,0,0,1 ]<br>
即隨機找兩物品，一個已在背包中，一個不在背包中，將原本不在背包的放入背包，同時將放回原本在背包的物品。<br>

程式採 **(2)左右移動** 的方法找鄰近解<br>
過程需檢查是否符合 合法解 ( 總重 < Capacity )，若不符合則 while 迴圈取新鄰近解。<br>

## STEP 3 Evalution: 評估適應值(Fitness value)大小
計算鄰近解的獲利 ( Profit )<br>

## STEP 4 Determination: 
鄰近解的獲利 ( Profit )和現解的獲利 ( Profit )比較，<br>
鄰近解的獲利 ( Profit ) 較高，即更新現解成鄰近解 ;<br>
鄰近解的獲利 ( Profit ) 較低，則進入退火環節。<br>

### 退火環節:<br>
![](https://i.imgur.com/gkdtqoS.jpg)

隨機值(r:0~1的浮點數) ≤ 允許機率 則進行更新，接受較差的鄰近解獲利 ; <br>
隨機值(r:0~1的浮點數) > 允許機率 則維持現解。<br>

### 允許機率: 
![](https://i.imgur.com/hUFg4za.jpg)
```=python
np.exp( (neighbor_profit - currrent_profit) / current_temperature )
```
差值(Δf)需 < 0 ，故為(鄰近解 - 現解)


e的指數若是一個很小的負值，計算後的值會較接近1，允許機率較高，接受差值可能性高；<br>
e的指數若是一個很大的負值，計算後的值會較接近0，允許機率較低，接受差值可能性低。<br>


### 比較大的機率接受更新方法: (即讓e的指數是一個很小的負值)<br>
(1) 差值(Δf)較小 (鄰近解 - 現解)<br>
(2) 初始退火溫度不要太小 <br>
(3) 退火係數不要太小，每輪降溫才不會太快<br>

### 降溫 ↓ 
不論是否更新進下一輪迭代前須降溫 ↓  ( 允許機率 ↓ )<br>
```=python
current_temperature = current_temperature * Rₜ ( 退火係數 )
```

重複 STEP2 ~ STEP4 的步驟，直到迭代完 500 次停止。<br>

## STEP 5 畫出 500次 迭代( iteration )的收斂圖

![](https://i.imgur.com/o2LPXIe.jpg)

結論:<br>
雖然模擬退火演算法在0/1背包問題的實驗結果爬山演算法差異不大，但在更複雜問題上(解的分布有多個高低起伏)，模擬退火演算法是能夠有更好效果的。<br>
