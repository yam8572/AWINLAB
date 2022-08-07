#coding:gbk
import random
import math
import matplotlib.pyplot as plt
global m,C;    # m����Ʒ ,��������C
global time,balance;    #  time ��������, balance  ƽ�����
global best,T,af;   #best ��¼ȫ������  T �¶�  af�˻���

m=15; T=200.0; af =0.95;
time =500;  balance = 200; 
best_way=[0]*m;   now_way=[0]*m  #  best_way ��¼ȫ�����Žⷽ��   now_way ��¼��ǰ�ⷽ��  
weight=[];
profits=[];
picture=[];

def cop(a,b,le):     #���ƺ��� ��b�����ֵ��ֵa����
    for i in range(le):
        a[i]=b[i]
def calc(x):  #���㱳����ֵ
    global C,wsum;
    vsum=0;wsum=0;
    for i in range(m):
        vsum +=x[i]*profits[i];  wsum += x[i]*weight[i];    
    return  vsum;
def produce():  #��ʼ���������
    while (1>0):
        for k in range(m):
            if(random.random() < 0.5):  now_way[k]=1;
            else: now_way[k]=0;
        calc(now_way)
        if(wsum <C): break;
    global best;
    best=calc(now_way);
    cop(best_way,now_way,m);

def init():   #��ʼ������
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
    produce()    #������ʼ��
def get(x):      #������������Ѿ����ڵ���Ʒȡ��
    while(1>0):
        ob = random.randint(0,m-1);
        if(x[ob]==1): x[ob]=0;break;
def put(x):      #������뱳���в����ڵ���Ʒ
    while(1>0):
        ob = random.randint(0,m-1);
        if(x[ob]==0): x[ob]=1;break;       
def slove():  #��������
    global best,T,balance;
    test=[0]*m;
    now = 0;   #��ǰ������ֵ
    for i in range(balance):
        now = calc(now_way);
        cop(test,now_way,m);
        ob = random.randint(0,m-1); #���ѡȡĳ����Ʒ
        if(test[ob]==1): put(test);test[ob]=0;  #�ڱ����������ó���������������Ʒ
        else:   #���ڱ�������ֱ�Ӽ�����滻�����ڱ����е���Ʒ
            if(random.random()<0.5):test[ob]=1; 
            else : get(test); test[ob]=1;
        temp= calc(test);
        if(wsum>C):continue;    # �Ƿ���������
        if(temp > best):
            best=temp;
            cop(best_way,test,m);     #����ȫ������
            
        
        if(temp > now):
            cop(now_way,test,m);       #ֱ�ӽ����½�
            
            
        else:
            g = 1.0*(temp-now)/T;
            if(random.random() < math.exp(g)):   #���ʽ����ӽ�
                cop(now_way,test,m);
        
                
#*****************************������**********************        
init();
isGood = 0;
for i in range(time):      
    slove();
    T = T*af;    #�¶��½�
    picture.append(best)
if(isGood == 0):   print('�Ž�:',best,'��������',time);
print('����Ϊ��',best_way);               #��ӡ����
plt.plot(picture)
plt.title('SA')
plt.show()
