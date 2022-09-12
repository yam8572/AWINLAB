# HW6 [粒子群最佳化(Particle swarm optimiaztion)](https://tzuchieh0931.medium.com/%E7%B2%92%E5%AD%90%E7%BE%A4%E6%9C%80%E4%BD%B3%E5%8C%96-pso-13e702657f7d)

參考資料:
[以Python實作粒子群演算法(Particle Swarm Optimization, PSO)](https://medium.com/qiubingcheng/%E4%BB%A5python%E5%AF%A6%E4%BD%9C%E7%B2%92%E5%AD%90%E7%BE%A4%E6%BC%94%E7%AE%97%E6%B3%95-particle-swarm-optimization-pso-f0d0404c443b)

## 題目:
HW6作業：<br>
請使用粒子群最佳化(Particle swarm optimiaztion)解決Ackley function <br>

※本次作業請畫出51 run、1000 iteration的結果平均收斂圖，並一併附於壓縮檔中，另程式流程及結果請使用.txt檔說明，包含找到的最佳解為何，平均最佳解為何，並嘗試分析其原因。<br>

## STEP 0 初始化迭代參數 及 粒子群最佳化相關參數 及 Ackley function
### (1)初始化迭代參數
平均迭代1次 run 次數<br>
run = 51<br>
迭代次數(Iteration)<br>
iteration = 1000<br>

### (2)粒子群最佳化相關參數
![](https://i.imgur.com/KINZiR6.png)
![](https://i.imgur.com/8vg2dsP.png)


初始方向向量設 0<br>
v = 0 <br>
w = 0.729844 <br>
c1 = c2 = 1.496180 <br>
r1 = r2 = 0~1 間隨機數 <br>

### (3)Ackley function參數
Ackley function:<br>
![](https://i.imgur.com/TyYor69.png)
![](https://i.imgur.com/vwi24Nz.png)

a = 20, b = 0.2 and c = 2π<br>

## STEP 1 粒子的位置進行隨機初始化
在上下界的範圍內隨機產生位置<br>
```python=
for d in range(self.dimension):
    rand_pos = self.lower_bounds[d]+random.random()*(self.upper_bounds[d]-self.lower_bounds[d])
    solution.append(rand_pos)
```
將所有粒子進行 evaluation 代入Ackley function算出其適應值，並且將目前的位置及適應值設為各粒子的歷史最佳位置及適應值，最後找出全部粒子中最佳的位置及適應值即完成初始化步驟<br>

計算適應值:<br>
```python=
# Evaluation
# objective function
def Ackley_objective_value(x, y):
    return -a * exp(-b * sqrt((x**2 + y**2) / dim)) - exp((cos(c * x) + cos(c * y)) / dim) + e + a
```
找出全部粒子中最佳的位置及適應值:<br>
```python=
#update invidual best solution
self.individual_best_solution.append(solution)
objective_val = self.Ackley_objective_value(self.solutions[i][0],self.solutions[i][1])
self.individual_best_objective_value.append(objective_val)

#record the smallest objective val
if(objective_val < min_val):
    min_index = i
    min_val = objective_val
    
# udpate so far the best solution 初始化最佳 globalBest(初始粒子值最小的)
self.global_best_solution = self.solutions[min_index].copy()
self.global_best_objective_value = min_val
```

## STEP 2 Transition 更新粒子位置及慣性方向
![](https://i.imgur.com/KINZiR6.png)
![](https://i.imgur.com/8vg2dsP.png)
![](https://i.imgur.com/eDqILGu.png)

```python=
# Transition
def move_to_new_positions(self):
    for i,solution in enumerate(self.solutions):
        # personalBest影響權重
        alpha = self.c1 * random.random()
        # globalBest影響權重
        beta = self.c2 * random.random()
        for d in range(self.dimension):
            # 新慣性 = 原慣性 + 權重 * (個人最佳 - 原位置 ) + 權重 * (全域最佳 - 原位置 ) 
            v = w * self.v + alpha * (self.individual_best_solution[i][d]-self.solutions[i][d])+\
                beta * (self.global_best_solution[d]-self.solutions[i][d])
            # 新位置 = 原位置 + 新慣性
            self.solutions[i][d] += v
            # 超過邊界拉回在邊界上
            self.solutions[i][d] = min(self.solutions[i][d],self.upper_bounds[d])
            self.solutions[i][d] = max(self.solutions[i][d],self.lower_bounds[d])
```
## STEP 3 Evaluation
無條件接受新產生的解，即使新的解比原先解差也會接受。<br>
故只需把所有粒子送入評估函數(Ackley function)進行評估得到新的適應值。<br>

## STEP 4 Determination: 
若新的適應值較小即更新全局最佳解。<br>
```python=
def update_best_solution(self):
    for i,solution in enumerate(self.solutions):
        # Evaluation
        obj_val = self.Ackley_objective_value(self.solutions[i][0],self.solutions[i][1])
        # Determination
        # 更新 personal best
        if(obj_val < self.individual_best_objective_value[i]):
            self.individual_best_solution[i] = solution
            self.individual_best_objective_value[i] = obj_val
            # 更新 global best
            if(obj_val < self.global_best_objective_value):
                self.global_best_solution = solution
                self.global_best_objective_value = obj_val
```

重複 STEP2 ~ STEP4 ( TED ) 的步驟，直到跑完 51run 各迭代完 1000 次停止。<br>

## STEP 5 畫出 跑完 51run 各迭代完 1000 次 的平均收斂圖
每次迭代都紀錄入解和解值，<br>
並用 best_sol, best_val 分別記錄最佳解及最佳解值。<br>
```=python
# 紀錄每次 iteration 最佳解值
iteration_history.append(particals.global_best_objective_value)

if (particals.global_best_objective_value < best_val):
    # 儲存最佳解
    best_val = particals.global_best_objective_value
    best_sol = particals.global_best_solution
```
最後用每次的紀錄採平均畫出平均收斂圖
```=python
# 畫採的平均收斂圖
plotIteration(avg_val, iteration)
```
![](https://i.imgur.com/mY2h6FO.png)

結果:<br>
最佳解:  [1.2312433486973203e-07, 2.728598631673808e-07]<br>
最佳值:  8.467000007783554e-07<br>
最佳平均解值 8.467000007783554e-07<br>
