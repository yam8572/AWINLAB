# 	HW3-1 [模擬退火演算法(Simulated annealing, SA)](https://tzuchieh0931.medium.com/sa-metaheuristic-03-2632b2047d1f)
改善 爬山演算法 (Hill climbing, HC)，可能卡在 區域最佳解(Local optimum) 無法跳脫找到更佳的解 達到 全域最佳解(Global optimum)<br>
slove : 一定的機率接受較差的解，以此增加跳脫出區域最佳解的機會<br>

![](https://i.imgur.com/7qiA1m0.jpg)

# 1. 100bits 的 one-max 問題
## STEP 0 初始化迭代參數 及 退火環節參數
### (1)初始化迭代參數
```=python
# 100 bits
n = 100 

# 迭代次數(Iteration)
iteration = 1000

# 平均迭代1次 run 次數
run = 51
```

### (2)退火環節參數
初始溫度(T) 退火溫度 : current_temperature = 5.0<br>
讓初始允許機率達0.8 (較高機率接受差值)<br>

![](https://i.imgur.com/Pqllwqs.jpg)

退火係數(Rₜ) = 0.95 (降溫不要降太快故設0.95)<br>
退火係數(Rₜ)越小，降溫(T)越快，允許機率越快歸0，解收斂越快。<br>
    
## STEP 1 Initial : 產生初始解
隨機產生出一組合法解 : 依bits數隨機產生 0/1 長度的陣列 <br>
```=python
item_status = [ random.randint(0,1) for _ in range(bits數)] 
```

## STEP 2 Transition: 隨機 / 左右 移動 產生出其他解 (鄰近解)

### 找鄰近解方法:<br>

### (1)左右移動: 使解往左走+1 或往右走-1 <br>

ex. [ 0,0,0,1 ] 的左移+1鄰近解 : [ 0,0,1,0 ]<br>
ex. [ 0,0,0,1 ] 的右移-1鄰近解 : [ 0,0,0,0 ]<br>

### (2)隨機移動: 將隨機一位置 0換成 1 1換成 0 <br>
ex. [ 1,1,0,0 ] 的鄰近解 : [ 0,1,0,0 ] 、 [ 1,0,0,0 ] 、 [ 1,1,1,0 ] 、 [ 1,1,0,1 ]<br>


本程式採 **(2)隨機移動** 的方法找鄰近解<br>

## STEP 3 Evalution: 評估適應值(Objective value)大小
計算鄰近解的值 ( Value )<br>

```=python
    i = random.randint(0,n-1)

    # 多一個 1 
    if(neightbor_sol[i] == 0):

        neightbor_sol[i]=1
        neighbor_value += 1

    # 少一個 1 
    else: 
        neightbor_sol[i] = 0
        neighbor_value -= 1
```

## STEP 4 Determination: 
鄰近解的值 ( value )和現解的值 ( value )比較，<br>
鄰近解的值 ( value ) 較高，即更新現解成鄰近解 ;<br>
鄰近解的值 ( value ) 較低，則進入退火環節。<br>

```=python
# 鄰近解若優於或等於先前解則更新
if(currrent_value <= neighbor_value):

    current_sol = neightbor_sol
    currrent_value = neighbor_value

# 若差於先前解則進行退火環節
else:

    # 隨機值(r:0~1的浮點數)
    r = random.random()

    # Δf < 0 ，故找最大值為: 鄰近解 - 先前解
    Δf = (neighbor_value - currrent_value)
    accept_p = np.exp( (neighbor_value - currrent_value) / current_temperature )

    # 隨機值(r:0~1的浮點數) ≤ 允許機率則接受差值進行更新
    if(r <= accept_p):
        current_sol = neightbor_sol
        currrent_value = neighbor_value
```

### 退火環節:<br>
![](https://i.imgur.com/gkdtqoS.jpg)

隨機值( r:0 ~ 1的浮點數 ) ≤ 允許機率 則進行更新，接受較差的鄰近解獲利 ; <br>
隨機值( r:0 ~ 1的浮點數 ) > 允許機率 則維持現解。<br>

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

重複 STEP2 ~ STEP4 的步驟，直到迭代完 1000 次停止。<br>

## STEP 5 畫出 1000次 迭代( iteration ) run=51的平均收斂圖

![](https://i.imgur.com/oqFc4cT.jpg)



結論:<br>
在 iteration = 68 時收斂，<br>
找到最佳解 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]<br>
100 bits 個 1 ，最佳解值: 100<br>
