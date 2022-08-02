# I.	機器學習（Machine Learning）
## STEP1 讀csv檔
train_file_url= 'Mobile Price Classification/train.csv' # train檔案位置
test_file_url= 'Mobile Price Classification/test.csv' # test檔案位置


## STEP2 刪除欄位
利用相關係數找出影響手機價位的屬性欄位
#找出影響價格範圍的屬性(設相關係數 > 0.1 ) battery_power px_height px_width ram 
train_data.corr(method ='pearson')['price_range']

![](https://i.imgur.com/xypnUgq.png)

## STEP3 標準化 (待實驗何種情況標準化會提升準確率)
反而score準確率svm會差點0.01(0.961875>>0.9593)，但計算效能比較快

## STEP4 將訓練資料切分成訓練集和驗證集 (8:2切分)
X_train, X_valid, y_train, y_valid = train_test_split(X_train_data, Y_train_data, test_size = 0.2, random_state = 42)

## STEP5 使用4種機器學習模型 (各模型參數待了解)
訓練集準確率：XXX_model.score(X_train,y_train)
驗證集準確率：XXX_model.score(X_valid,y_valid)



| 學習模型| 訓練集準確率 | 驗證集準確率 |
| -------- | -------- | -------- |
| 支援向量機(Support Vector Machine, SVM)    | 0.959375     | 0.9675     |
| K-近鄰演算法(K-nearest neighbors, KNN) | 0.930625 | 0.915 |
| 決策樹(Decision Tree, DT)    | 1.0    | 0.86     |
| 隨機森林(Random Forest, RF)  | 1.0    | 0.935   |

# STEP6 預測測試集(Testing set)結果
### (a)	支援向量機(Support Vector Machine, SVM)
![](https://i.imgur.com/GOFzf93.png)
### (b)	K-近鄰演算法(K-nearest neighbors, KNN)
![](https://i.imgur.com/vQsmCZq.png)
### ( c )	決策樹(Decision Tree, DT)
![](https://i.imgur.com/I52lUXs.png)
### (d)	隨機森林(Random Forest, RF)
![](https://i.imgur.com/u7KRI82.png)

# STEP7 使用混淆矩陣(Confusion matrix)分析
以驗證集分析 採 Weight avg



| 學習模型 | 準確率(Accuracy) | 精準度(Precision) | 召回率(Recall) | F1分數(F1-score)| 支持度(Support) |
| -------- | -------- | -------- |-------- | -------- | -------- |
| SVM     | 0.97    | 0.97     |0.97    | 0.97     | 0:錯2/1:錯0/2:錯7/3:錯4|
| KNN     | 0.92     | 0.92     |0.92    | 0.92     | Text     |
| DT    | 0.87    | 0.86     | 0.86     | 0.86     | Text     |
| RF    | 0.94    | 0.94    | 0.94     | 0.94     | Text     |

結論：
SVM學習模型在本範例較佳。

### (a)	支援向量機(Support Vector Machine, SVM)
![](https://i.imgur.com/wJxfT66.png)

### (b)	K-近鄰演算法(K-nearest neighbors, KNN)
![](https://i.imgur.com/o6M7GYJ.png)

### ( c )	決策樹(Decision Tree, DT)
![](https://i.imgur.com/jjkQyjL.png)

### (d)	隨機森林(Random Forest, RF)
![](https://i.imgur.com/KAeO2ja.png)















