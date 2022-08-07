#coding:gbk
import random
import math
import matplotlib.pyplot as plt
global m,C;    # m个物品 ,背包容量C
global time,balance;    #  time 迭代次数, balance  平衡次数
global best,T,af;   #best 记录全局最优  T 温度  af退火率

m=15; T=200.0; af =0.95;
time =500;  balance = 200; 
best_way=[0]*m;   now_way=[0]*m  #  best_way 记录全局最优解方案   now_way 记录当前解方案  
weight=[];
profits=[];
picture=[];

def cop(a,b,le):     #复制函数 把b数组的值赋值a数组
    for i in range(le):
        a[i]=b[i]
def calc(x):  #计算背包价值
    global C,wsum;
    vsum=0;wsum=0;
    for i in range(m):
        vsum +=x[i]*profits[i];  wsum += x[i]*weight[i];    
    return  vsum;
def produce():  #初始产生随机解
    while (1>0):
        for k in range(m):
            if(random.random() < 0.5):  now_way[k]=1;
            else: now_way[k]=0;
        calc(now_way)
        if(wsum <C): break;
    global best;
    best=calc(now_way);
    cop(best_way,now_way,m);

def init():   #初始化函数
    global C,best,T;    
    file = open('p07_c.txt', 'r')
    C = int(file.read())
    #print(C)
    file.close()
    
    file = open('p07_w.txt', 'r')
    for line in file.readlines():        
        weight.append(int(line))
        #print(weight)
    file.close

    file = open('p07_p.txt', 'r')
    for line in file.readlines():        
        profits.append(int(line))
        #print(weight)
    file.close

    best=-1;
    produce()    #产生初始解
def get(x):      #随机将背包中已经存在的物品取出
    while(1>0):
        ob = random.randint(0,m-1);
        if(x[ob]==1): x[ob]=0;break;
def put(x):      #随机放入背包中不存在的物品
    while(1>0):
        ob = random.randint(0,m-1);
        if(x[ob]==0): x[ob]=1;break;       
def slove():  #迭代函数
    global best,T,balance;
    test=[0]*m;
    now = 0;   #当前背包价值
    for i in range(balance):
        now = calc(now_way);
        cop(test,now_way,m);
        ob = random.randint(0,m-1); #随机选取某个物品
        if(test[ob]==1): put(test);test[ob]=0;  #在背包中则将其拿出，并加入其它物品
        else:   #不在背包中则直接加入或替换掉已在背包中的物品
            if(random.random()<0.5):test[ob]=1; 
            else : get(test); test[ob]=1;
        temp= calc(test);
        if(wsum>C):continue;    # 非法解则跳过
        if(temp > best):
            best=temp;
            cop(best_way,test,m);     #更新全局最优
            
        
        if(temp > now):
            cop(now_way,test,m);       #直接接受新解
            
            
        else:
            g = 1.0*(temp-now)/T;
            if(random.random() < math.exp(g)):   #概率接受劣解
                cop(now_way,test,m);
        
                
#*****************************主函数**********************        
init();
isGood = 0;
for i in range(time):      
    slove();
    T = T*af;    #温度下降
    picture.append(best)
if(isGood == 0):   print('优解:',best,'迭代次数',time);
print('方案为：',best_way);               #打印方案
plt.plot(picture)
plt.title('SA')
plt.show()
