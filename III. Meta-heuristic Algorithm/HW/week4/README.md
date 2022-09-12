# 	HW4 [禁忌搜尋演算法(Tabu Search)](https://tzuchieh0931.medium.com/ts-metaheuristic-04-c71c8ac1d57f)
參考資料:
https://github.com/james093131/Tabu-Search-for-0-1-knapsack/blob/master/normal.hpp
## 題目:
請使用禁忌搜尋法(Tabu search)與SA方法解決100 bits one-max problem <br>
(deception problem自由解答)<br>
※本次作業請畫出51 run、1000 iteration的結果平均收斂圖，並一併附於壓縮檔中，另程式流程及結果請使用.txt檔說明，包含找到的最佳解為何，平均最佳解為何，並嘗試分析其原因。<br>

# 100bits 的 one-max 問題
## STEP 0 初始化迭代參數
### (1)初始化迭代參數
```=python
# 100 bits
n = 100 

# 迭代次數(Iteration)
iteration = 1000

# 平均迭代1次 run 次數
run = 51

# 禁忌搜尋列表 列表size設=7
tabu_list = []
tabu_size = 7
```
    
## STEP 1 Initial : 產生初始解
隨機產生出一組合法解 : 依bits數隨機產生 0/1 長度的陣列 <br>
```=python
rand_sol = [ random.randint(0,1) for _ in range(bits數)] 
```

## STEP 2 Transition: 隨機移動 產生出鄰近解
隨機移動: 將隨機一位置 0換成 1 1換成 0 <br>
ex. [ 1,1,0,0 ] 的可能鄰近解 : [ 0,1,0,0 ] 、 [ 1,0,0,0 ] 、 [ 1,1,1,0 ] 、 [ 1,1,0,1 ] <br>
```=python
i = random.randint(0,n-1)

# 多一個 1 
if(neightbor_sol[i] == 0):

    neightbor_sol[i] = 1

# 少一個 1 
else: 
    neightbor_sol[i] = 0
```

若鄰近解已在 tabu_list 中則重新進 STEP2 Transition 找新鄰近解，<br>
直到找到不在 tabu_list 中的解，並將其加入 tabu list 尾端。 <br>

### 檢查是否在 tabu_list 中: <br>
```=python
if(sol in tabu_list):
	return False
else:
	return True
```

### 將新鄰近解加入 tabu list 中: <br>
tabu list 未滿，新鄰近解直接加進 tabu list 尾端；<br>
tabu list 滿，刪除 tabu list 中第一個解，再將新鄰近解加進 tabu list 尾端<br>

```=python
def recordTabuList(sol):
    
    # tabu list 未滿 --> 直接加進尾端
    if(len(tabu_list) < tabu_size):
        tabu_list.append(sol)
        
    # tabu list 滿 --> 刪第一個再加進尾端
    else:
        tabu_list.pop(0)
        tabu_list.append(sol)
```

## STEP 3 Evalution: 評估適應值(Objective value)大小
計算採隨機移動鄰近解的值 ( Value )<br>
```=python
def Evaluation(sol):
    val = sol.count(1)
    return val
```

## STEP 4 Determination: 
鄰近解的值 ( value )和現解的值 ( value )比較，<br>
鄰近解的值 ( value ) 較高，即更新現解成鄰近解 ;<br>
```=python
def Determination(current_sol, current_val, new_sol, new_val):
    # 新解值較好 --> 接受新解
    if(new_val > current_val):
        current_sol, current_val = new_sol, new_val
    return current_sol, current_val
```

重複 STEP2 ~ STEP4 ( TED ) 的步驟，直到跑完 51run 各迭代完 1000 次停止。<br>

## STEP 5 畫出 跑完 51run 各迭代完 1000 次 的平均收斂圖
每次迭代都紀錄入解和解值，<br>
並用 rand_best_val, rand_best_val 分別記錄最佳解及最佳解值。<br>
```=python
# 紀錄採隨機移動每次的值
temp_history.append(rand_currrent_val)
# 紀錄採隨機移動最佳解及最佳值
if(rand_currrent_val > rand_best_val):
    rand_best_val = rand_currrent_val
    rand_best_sol = rand_current_sol
```
最後用每次的紀錄採平均畫出平均收斂圖
```=python
# 畫採隨機移動的平均收斂圖
plotIteration(rand_avg_val, iteration)
```
![](https://i.imgur.com/smap4D5.jpg)


結論:<br>
找到最佳解 10 bits 個 1 : [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]<br>
最佳解值: 100<br>
最佳平均解值: 100<br>
