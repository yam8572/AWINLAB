# HW5 [蟻群演算法 (Ant Colony Optimization)](https://medium.com/qiubingcheng/%E4%BB%A5python%E5%AF%A6%E4%BD%9C%E8%9F%BB%E7%BE%A4%E6%9C%80%E4%BD%B3%E5%8C%96%E6%BC%94%E7%AE%97%E6%B3%95-ant-colony-optimization-aco-%E4%B8%A6%E8%A7%A3%E6%B1%BAtsp%E5%95%8F%E9%A1%8C-%E4%B8%8A-b8c1a345c5a1)

參考資料:
https://github.com/james093131/ACO/blob/master/main.cpp

[ant colony optimization](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4129846)

[An ant colony optimization method for generalized TSP problem](https://www.sciencedirect.com/science/article/pii/S1002007108002736)

[畫路徑圖](https://github.com/p208p2002/tsp-eil51-solutions/blob/master/eil51-GA.ipynb)

## 題目:
HW5作業：<br>
請使用蟻群演算法 (Ant Colony Optimization) 解決銷售員走訪問題 (Travelling Salesman Problem)，題目指定為 eil51：<br>http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/eil51.tsp

※本次作業請畫出51 run、1000 iteration的結果平均收斂圖，並一併附於壓縮檔中，另程式流程及結果請使用.txt檔說明，包含找到的最佳解為何，平均最佳解為何，並嘗試分析其原因。<br>

## 流程演算法:
![](https://i.imgur.com/4c9hxaN.png)
![](https://i.imgur.com/OgP68FQ.png)
![](https://i.imgur.com/MPK05TV.png)

## STEP 0 初始化迭代參數 及 螞蟻演算法相關參數
### (1)初始化迭代參數
平均迭代1次 run 次數<br>
run = 51<br>
迭代次數(Iteration)<br>
iteration = 1000<br>

### (2)螞蟻演算法相關參數
螞蟻數<br>
ants = 51<br>

讀取ei151.txt抓各點[X Y] 座標<br>
coordinate = readFile()<br>
```=python=
xy = []
    
    file = open('ei151.txt', 'r')
    r = file.read()
    
    # 每行依序讀
    read_line = r.split('\n')               
    for i in range(len(read_line)):
        # 每行再以空格切割資料
        read_element = read_line[i].split()
        # 第一個 element 當 key 第二、三個當 value
        xy.append([int(read_element[1]),int(read_element[2])])

    file.close()
    
    return np.array(xy,dtype=np.int8)

```

拜訪點總數<br>
city_num = len(coordinate) <br>

建 點數 * 點數的多為陣列 存放各點間的距離倒數表<br>
distance_table = [[0 for _ in range(city_num)] for _ in range(city_num)]<br>

費洛蒙初值設一個極小值<br>
initial_pher = 0.000167<br>
初始化費洛蒙表<br>
pheromone_table = [[initial_pher for _ in range(city_num)] for _ in range(city_num)]<br>

通常 beta > alpha<br>
alpha = 0 表費洛蒙次方設 0 值為1 >> 表下個地點去哪的機率全受距離影響<br>
alpha = 2.6<br>
beta = 0 表距離次方設 0 值為1 >> 表下個地點去哪的機率全受費洛蒙影響<br>
beta = 6.7<br>

constant 定值<br>
Q = 0.9<br>
費洛蒙消退比<br>
p_decline = 0.9<br>

### 一隻螞蟻就是表示一個解，建構每一個解流程：
![](https://i.imgur.com/jDc1Xkf.png)

**Transition**

STEP1 隨機挑選起始點。<br>
STEP2 計算候選點清單的合適度。依照能見度<br>(visibility)及費洛蒙(pheromone)計算合適度。<br>
STEP3 使用輪盤法挑選本次欲踏訪點。<br>
STEP4 更新候選點清單。其實就是移除本階段踏訪的縣市。<br>
STEP5 重複上述1–4動作，直到所有點踏訪完畢。<br>

**Evaluation**
評估每個螞蟻各自解的目標值(Objective value)大小: 行徑總距離。<br>

**Determination**
儲存最佳解<br>
```python=
# 儲存單一 iteration 下 ants找到的最佳解 
if (distance < ants_bestdistance):
    ants_bestdistance = distance
    ants_bestpath = current_path
# 紀錄單一 run 下 1000iteration 的最佳解 
if (ants_bestdistance < iter_bestdistance):
    # 儲存最佳解
    iter_bestdistance = ants_bestdistance
    iter_bestpath = ants_bestpath
```

**更新費洛蒙：**
費洛蒙會隨時間蒸散，並增加新解螞蟻產生的費洛蒙<br>
![](https://i.imgur.com/yzv3Iki.png)

費洛蒙蒸散 = 原費洛蒙 x 蒸發率<br>
新增費洛蒙值 = Q(定值) / 路徑總長<br>
```python=
# 更新費洛蒙:費洛蒙會隨時間蒸散
def pheromoneUpdate(pheromone_table, distance, path):
    # (公式 8.2~8.4)
    # 公式 8.2 i 到 j 更新的費洛蒙數量 Q / totalDistance
    pheromoneAmount = Q / distance
    # 公式 8.4 前半 費洛蒙蒸散
    pher_table = np.array(pheromone_table,dtype=float)
    pher_table *= p_decline 
    
    # Add pheromone to the path of the ants
    # 加總螞蟻所經路徑費洛蒙總數 公式 8.3
    for i in range(len(path)):
        for j in range(city_num):
            city1 = path[j]
            city2 = path[j+1] if j < city_num-1 else path[0]
            # 公式 8.4 後半 加上公式 8.3 即本次螞蟻新增的費洛蒙值
            pheromone_table[city1][city2] += pheromoneAmount
            pheromone_table[city2][city1] += pheromoneAmount

            if pheromone_table[city1][city2] < initial_pher :
                pheromone_table[city1][city2] = initial_pher
                pheromone_table[city2][city1] = initial_pher
    
    # pheromone_table = (1-p_decline) * pheromone_table + p_decline * (Q/dis)
    return pher_table
```

**平均收斂圖結果:**<br>
![](https://i.imgur.com/2qIwPbT.png)

最佳解: <br>
[46 11 45 50 26  0 31 10 37 15 49  8 48  4 36 43 14 44 32 38  9 29 33 20
 28  1 21  2 19 34 35 27 30 25  7 47 22  6 42 23 13 24 12 40 18 39 41 16
  3 17  5]
最佳值:  457.2444075965325 <br>
最佳平均解值 455.92493481931376 <br>

**路徑圖:**<br>
![](https://i.imgur.com/uX5DKrv.png)

### 目標正解: 431
![](https://i.imgur.com/2WVjvLu.png)
![](https://i.imgur.com/OmJCYST.png)

