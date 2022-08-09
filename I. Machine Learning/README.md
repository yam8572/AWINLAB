# I.	機器學習（Machine Learning）
## STEP1 讀csv檔
```=python
train_file_url= 'Mobile Price Classification/train.csv' # train檔案位置 
test_file_url= 'Mobile Price Classification/test.csv' # test檔案位置 
train_data = pd.read_csv(train_file_url); #讀訓練檔 
test_data = pd.read_csv(test_file_url); #讀測試檔 
```


## STEP2 刪除欄位
利用相關係數找出影響手機價位的屬性欄位 <br>
#找出影響價格範圍的屬性( 設相關係數 > 0.1 ) : battery_power 、 px_height 、 px_width 、 ram <br>
```=python
train_data.corr(method ='pearson')['price_range'] 
```
![](https://i.imgur.com/xypnUgq.png)

| Price_range   | 相關係數  |
| --------      | -------- | 
| ram           | 0.917046 | 
| battery_power | 0.200723 |
| px_height     | 0.148858 | 
| px_width      | 0.165818 | 

## STEP3 標準化 (待實驗何種情況標準化會提升準確率)
反而score準確率svm會差點0.01(0.961875>>0.9593)，但計算效能比較快 <br>

## STEP4 將訓練資料切分成訓練集和驗證集 (8:2切分)
```=python
X_train, X_valid, y_train, y_valid = train_test_split(X_train_data, Y_train_data, test_size = 0.2, random_state = 42)
```

## STEP5 使用4種機器學習模型 (各模型參數待了解)
訓練集準確率：XXX_model.score(X_train,y_train) <br>
驗證集準確率：XXX_model.score(X_valid,y_valid) <br>



| 學習模型                              | 訓練集準確率 | 驗證集準確率 |
| ------------------------------------ | -------- | -------- |
| 支援向量機(Support Vector Machine, SVM)| 0.959375 | 0.9675  |
| K-近鄰演算法(K-nearest neighbors, KNN) | 0.930625 | 0.915   |
| 決策樹(Decision Tree, DT)             | 1.0      | 0.86    |
| 隨機森林(Random Forest, RF)           | 1.0       | 0.935   |

## STEP6 預測測試集(Testing set)結果
### (a)	支援向量機(Support Vector Machine, SVM)
![](https://i.imgur.com/GOFzf93.png)
### (b)	K-近鄰演算法(K-nearest neighbors, KNN)
![](https://i.imgur.com/vQsmCZq.png)
### ( c )	決策樹(Decision Tree, DT)
![](https://i.imgur.com/I52lUXs.png)
### (d)	隨機森林(Random Forest, RF)
![](https://i.imgur.com/u7KRI82.png)

## STEP7 使用混淆矩陣(Confusion matrix)分析

![](https://i.imgur.com/UuKWXyi.jpg)

[圖片來源](https://www.ycc.idv.tw/confusion-matrix.html)

以驗證集分析 採 Weight avg

| 學習模型 | 準確率(Accuracy) | 精準度(Precision) | 召回率(Recall) | F1分數(F1-score)| 支持度(Support)                 |
| ------  | -------------- | ---------------  |-------------- | -------------- | ------------------------------- |
| SVM     | 0.97           | 0.97             | 0.97          | 0.97           | 0:錯2 / 1:錯0 / 2:錯7 / 3:錯4     |
| KNN     | 0.92           | 0.92             | 0.92          | 0.92           | 0:錯6 / 1:錯5 / 2:錯10 / 3:錯13   |
| DT      | 0.87           | 0.86             | 0.86          | 0.86           | 0:錯13 / 1:錯10 / 2:錯20 / 3:錯13 |
| RF      | 0.94           | 0.94             | 0.94          | 0.94           | 0:錯4 / 1:錯3 / 2:錯9 / 3:錯10    |

### 各指標含意 :
* Precision (PPV): <br>
  看的是在預測正向的情形下，實際的「精準度」是多少。<br>
* Recall (TPR):<br> 
  則是看在實際情形為正向的狀況下，預測「能召回多少」實際正向的答案。<br>
* F1-score: <br>
  Precision 和 Recall 間重要的比例用 F1-score 統合指標。<br>
* Accuracy : <br>
  True Positive 和 True Negative，把它加總起來除上所有情形個數，當數據大部分偏實際真或實際假時指標會失效 。<br>
  Accuracy 和 Precision 是接近的，accuracy 無失指標性。<br>
  
  各模型在 精準度(Precision)、召回率(Recall)、F1分數(F1-score) 皆相等。<br>

### 分析各模型在解決這個分類問題上的優劣 : <br>

| Price_range   | 相關係數  |
| --------      | -------- | 
| ram           | 0.917046 | 
| battery_power | 0.200723 |
| px_height     | 0.148858 | 
| px_width      | 0.165818 | 

* **支援向量機(Support Vector Machine, SVM) :**<br>
    適合處理多維度的資料，各性質與價格呈線性相關，故適合本題有多種性質影響價格區間。<br>
* **K-近鄰演算法(K-nearest neighbors, KNN) :** <br>
    找到距離最近的K個鄰居(K避免偶數出現平手狀況)→進行投票→決定類別<br>
    本題切分出的驗證集，價格區間樣本數算平均 ( 資料平衡 400筆中 0:105筆 / 1:91筆 / 2:92筆 / 3:112筆 ) ，故能得到不錯的精準值。<br>
* **決策樹(Decision Tree, DT) :** <br>
    ram 對於手機價格的影響力最大(相關係數高達0.9)，各若以性質 ram 去做子點區分，較能精準分出價格區間 ; <br>
    反之，若以其他性質 battery_power、 px_height 、px_width 去做子點區分，所得到的精準程度就較低，<br>
    故整體平均下來會拉低 Precision、Recall。<br>
    不適合過多性質，易造成 overfitting 之情形。<br>
* **隨機森林(Random Forest, RF)** : <br>
    隨機抽取各性質及樣本數，建構多棵決策樹，整體平均下來精準度高於DT。<br>
    在性質是隨機抽樣，及樣本資料也是隨機抽樣，可以有效規避避 overfitting 之情形。<br>
    適合處理多維度的資料。


**結論：**<br>
SVM學習模型 不管在 預測正向的正確率 ( Precision ) 及 實際正向下的正確率 ( Recall ) 都能高達9成。<br>
SVM學習模型在 Accuracy、Precision、Recall、F1-score 指標皆高於其他學習模型，故SVM學習模型在本範例較佳。<br>

### (a)	支援向量機(Support Vector Machine, SVM)
![](https://i.imgur.com/wJxfT66.png)

### (b)	K-近鄰演算法(K-nearest neighbors, KNN)
![](https://i.imgur.com/o6M7GYJ.png)

### ( c )	決策樹(Decision Tree, DT)
![](https://i.imgur.com/jjkQyjL.png)

### (d)	隨機森林(Random Forest, RF)
![](https://i.imgur.com/KAeO2ja.png)















