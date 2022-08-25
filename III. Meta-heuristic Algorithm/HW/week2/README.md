# 	HW2 [爬山演算法(Hill climbing, HC)](https://tzuchieh0931.medium.com/hc-metaheuristic-02-a071980b37e6)

# 1. 100bits 的 one-max 問題
## STEP 0 初始化迭代參數
### (1)初始化迭代參數
```=python
# 100 bits
n = 100 

# 迭代次數(Iteration)
iteration = 1000

# 平均迭代1次 run 次數
run = 51
```
    
## STEP 1 Initial : 產生初始解
隨機產生出一組合法解 : 依bits數隨機產生 0/1 長度的陣列 <br>
```=python
item_status = [ random.randint(0,1) for _ in range(bits數)] 
```

## STEP 2 Transition: 左右 / 隨機 移動 產生出其他解 (鄰近解)

### 找鄰近解方法:<br>

### (1)左右移動: 使解往左走+1 或往右走-1 <br>

ex. [ 0,0,0,1 ] 的左移+1鄰近解 : [ 0,0,1,0 ]<br>
ex. [ 0,0,0,1 ] 的右移-1鄰近解 : [ 0,0,0,0 ]<br>

### (2)隨機移動: 將隨機一位置 0換成 1 1換成 0 <br>
ex. [ 1,1,0,0 ] 的鄰近解 : [ 0,1,0,0 ] 、 [ 1,0,0,0 ] 、 [ 1,1,1,0 ] 、 [ 1,1,0,1 ]<br>


## STEP 3 Evalution: 評估適應值(Objective value)大小
計算鄰近解的值 ( Value )<br>

採 **(1)左右移動** 的方法找鄰近解<br>
```=python
# 左移 +1
for i in range(n-1,-1,-1):
    if(neightbor_sol[i] == 0):
        neightbor_sol[i] = 1
        neighbor_value += 1
        break
    else:
        neightbor_sol[i] = 0
        neighbor_value -= 1
```


採 **(2)隨機移動** 的方法找鄰近解<br>
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

```=python
# 鄰近解若優於或等於先前解則更新
if(currrent_value <= neighbor_value):

    current_sol = neightbor_sol
    currrent_value = neighbor_value
```

重複 STEP2 ~ STEP4 ( TED ) 的步驟，直到跑完 51run 各迭代完 1000 次停止。<br>

## STEP 5 畫出 跑完 51run 各迭代完 1000 次 的平均收斂圖

採 **(1)左右移動** 的方法
![](https://i.imgur.com/hosdAtS.jpg)

採 **(2)隨機移動** 的方法
![](https://i.imgur.com/AH3FShP.jpg)

結論:<br>

* 採 **(1)左右移動** 的方法會陷入區域最佳解，<br>
因隨機產生 0/1 初始解，0/1出現各占50%，<br>
故初始解會落在中間值(長度一半)的位置，<br>
例如: <br>
[0,0,1,1] 左移+1 [0,1,0,0]<br>
[0,0,1,1] 右移-1 [0,0,1,0]<br>
皆沒有較好故維持不更新，故卡在一半的位置，無法往上獲得更好的解。<br>

* 採 **(2)隨機移動** 的方法會可找到全域最佳解，<br>
因隨機產生 0/1 初始解，0/1出現各占50%，<br>
因隨機移動是將解中的 bit 做0/1對調，<br>
有一半的機率可以將0換成1往上找到更好的解。<br>
