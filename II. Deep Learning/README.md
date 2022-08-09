# II. 深度學習（Deep Learning）
## STEP 1 找適合的圖片壓縮大小 
(圖片不會太糊的最小值) 
結論：設 IMG_SIZE = 100 <br>

![](https://i.imgur.com/YjTCHCN.jpg)


## STEP 2 匯入圖檔 並 壓縮處理
(1)圖片轉灰階(二維)
```=python
img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)
```
![](https://i.imgur.com/iTV8hAd.png)

**以灰階處理考量 :** 
每種花不只一種的顏色，不同種類的花也會有相同顏色，且葉子背景皆為綠色。


(1)圖片壓縮成 100px*100px
```=python
img_resize_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE)) 
```

(3)像素 normalize 成 0~1 間
```=python
img_resize_array = img_resize_array / 255 
```

## STEP 3 轉換資料維度以符合 Network

(1) 將 flower image 轉換成 (資料數, IMG_SIZE * IMG_SIZE)
```=python
X_arr = np.array(X).reshape(4317, IMG_SIZE * IMG_SIZE).astype('float32')
```

(2) 將 flower label 轉換成數值 (資料數, 5)

daisy-------> 1:[1. 0. 0. 0. 0.] 
dandelion---> 2:[0. 1. 0. 0. 0.] 
rose--------> 3:[0. 0. 1. 0. 0.] 
sunflower---> 4:[0. 0. 0. 1. 0.] 
tulip-------> 5:[0. 0. 0. 0. 1.]

## STEP 4 Train Network 
### ( Define Network >> Compile Network >> Fit Network )
#### Define Network : 建立簡單的線性執行的模型 
```
Adam_model = Sequential()
# Add Input layer, 隱藏層(hidden layer) 有 256個輸出變數
Adam_model.add(Dense(units=256, input_dim=10000, kernel_initializer='normal', activation='relu')) 
# Add output layer
Adam_model.add(Dense(units=5, kernel_initializer='normal', activation='softmax'))
```
#### Compile Network : 選擇損失函數、優化方法及成效衡量方式
```
Adam_model.compile( optimizer = Adam(learning_rate=0.0001),
                           loss = 'categorical_crossentropy',  
                           metrics = ['accuracy'] ) 
Adam_model.summary()
```
![](https://i.imgur.com/gQcULGx.jpg)

 #### Fit Network : 訓練模型
 ```
 # Train the model 批次 = 40 訓練週期 = 16
Adam_hostory = Adam_model.fit(
                    x = X_arr, 
                    y = y_arr,
                    validation_data = (x_test, y_test),
                    epochs = epochsNum, 
                    batch_size = batch_sizeNum, 
                    shuffle = True, 
                    verbose = 2)
```



![](https://i.imgur.com/hhWHqUt.jpg)

Common ways to improve a deep model:
• Adding layers
• Increase the number of hidden units
• Change the activation functions
• Change the learning rate
• Change the optimization function
• Fitting on more data [ 調整 批量大小(batch_size) ]
• Fitting for longer [ 調整 訓練週期(epochs) ]

### 以調整 優化器(optimizer) 、訓練週期(epochs)、批量大小(batch_size) 優化訓練模型

7 種優化器 (optimizer) : Adam、SGD、RMSprop、Adagrad、Adadelta、Adamax、Nadam <br>


### Case 1 當設 訓練週期(epochs)=20, 批量大小(batch_size)=32

| optimizer    | Adam   | SGD    | RMSprop | Adagrad | Adadelta | Adamax | Nadam  |
| ------------ | ------ | ------ | ------- | ------- | -------- | ------ | ------ |
| accuracy     | 0.6511 | 0.5550 | 0.4918  | 0.6120  | 0.5066   | 0.5453 | 0.4756 |
| val_accuracy | 0.6678 | 0.5972 | 0.5312  | 0.5637  | 0.5382   | 0.5718 | 0.4479 |

### Case 2 當設 訓練週期(epochs)=20, 批量大小(batch_size)=16

| optimizer    | Adam     | SGD      | RMSprop  | Adagrad  | Adadelta | Adamax   | Nadam    |
| ------------ | -------- | -------- | -------- | -------- | -------- | -------- | -------- |
| accuracy     | 0.6588 ↑ | 0.6516 ↑ | 0.4786 ↓ | 0.6671 ↑ | 0.5226 ↑ | 0.5548 ↑ | 0.4387 ↓ |
| val_accuracy | 0.6991 ↑ | 0.7118 ↑ | 0.5243 ↓ | 0.6250 ↑ | 0.5995 ↑ | 0.6215 ↑ | 0.3831 ↓ |

#### 結論: Case 1 VS Case 2 <br>
批量大小(batch_size) = 16 優於 =32 : Adam、SGD、Adagrad、Adadelta、Adamax<br>
批量大小(batch_size) = 16 差於 =32 : RMSprop、Nadam<br>
整體以 批量大小(batch_size) = 16 在 Adam、Adagrad 較佳<br>

### Case 3 當設 訓練週期(epochs)=30, 批量大小(batch_size)=16

| optimizer    | Adam    | SGD     | RMSprop | Adagrad | Adadelta | Adamax  | Nadam   |
| ------------ | ------  | ------  | ------- | ------- | -------- | ------  | ------  |
| accuracy     | 0.8145 ↑| 0.7855 ↑| 0.5874 ↑| 0.7992 ↑| 0.6403 ↑ | 0.6959 ↑| 0.6273 ↑|
| val_accuracy | 0.8565 ↑| 0.8044 ↑| 0.5301 ↑| 0.8565 ↑| 0.6227 ↑ | 0.6968 ↑| 0.6655 ↑|

#### 結論: Case 1 VS Case 3 <br>
訓練週期(epochs)=30 優於 =20 : Adam、SGD、RMSprop、Adagrad、Adadelta、Adamax、Nadam <br>
整體皆在 訓練週期(epochs)=30 下為佳
尤其在 Adam、SGD、Adagrad 顯著成長，Adam 為最佳 <br>

#### 盡量提高最優化各模型
| optimizer    | Adam       | SGD    | RMSprop | Adagrad | Adadelta | Adamax | Nadam  |
| ------------ | ------     | ------ | ------- | ------- | -------- | ------ | ------ |
| batch_size   | 16         | 16     | 48      | 16      | 16       | 16     | 48     |
| epochs       | 40         | 40     | 25      | 40      | 40       | 40     | 25     |
| accuracy     | **0.8918** | 0.8670 | 0.5247  | 0.8941  | 0.7528   | 0.8258 | 0.5147 |
| val_accuracy | 0.9248     | 0.9282 | 0.5012  | 0.8796  | 0.7905   | 0.8287 | 0.4954 |

#### 最終結論：<br>
選擇 optimizer = Adam，<br>
因 accuracy、val_accuracy 高於其他 optimizer (val_accuracy 能達 9成準確率)<br>
且 Adam 整體在折線下較穩定，折線的波動不會太大 (較沒有訓練中 val_accuracy 大幅度的上升或下降)<br>
透過測試得知 在 epochs=40 batch_size=16 的參數下 Adam 訓練較佳，<br>
故 STEP 5~7 用 optimizer=Adam epochs=40 batch_size=16 做評估。<br>

### 用 optimizer=Adam epochs=40 batch_size=16 下的訓練結果圖
![](https://i.imgur.com/gKO2tcN.jpg)
![](https://i.imgur.com/kIQla09.jpg)




## STEP 5 Evaluate Network 
### 用 optimizer=Adam epochs=40 batch_size=16 做評估

val_accuracy of testing data = 92.5%

## STEP 6 Make Predictions
### 出測試集隨機十筆預測後的結果和正解進行比較
![](https://i.imgur.com/Yxx86bu.jpg)


10張裡 預測正確:9張 預測正確:1張


## STEP 7 以混淆矩陣衡量模型的好壞

![](https://i.imgur.com/SF12CsA.jpg)


precision = 94% 和 recall = 92% 數值接近 val_accuracy = 92.5% ，accuracy 無失指標性。
precision = 94% > recall = 92% 在預測正向的精準率微佳於實際正向的精準率。

**困惑**<br>
訓練資料原本分類錯誤，預測也錯誤，<br>
不會因為訓練完挑出原本錯誤的分類。<br>

如下圖應為菊花(daisy)，但訓練資料歸在玫瑰(rose)資料夾
![](https://i.imgur.com/G2i49f9.png)
![](https://i.imgur.com/aUG3xrc.jpg)








