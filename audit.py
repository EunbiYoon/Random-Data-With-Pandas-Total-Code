import io
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import figure
import calendar
import pandas as pd
import io
import os
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta
import openpyxl
from random import*
import string
import pandas

def gmes():
    #아이템 만들기
    Item=["Tub Side Air Vent Bellows Tightened Check",
            "Drain Hose Damaged Check","Drain Hose Tightened Check",
            "Energy Label Version Check","Friction Damper Pins Seated Check",
            "Tub Side Gasket Tightened Check","Cabinet Cover Side Gasket Tightened Check",
            "Inlet Valve Harness Connected Check","Inner Drum Weld Thickness Check",
            "Outer Tub Weld Thickness Check","PCB Version Check",
            "Pressure Switch Tube Tightened Check","Rotor Bolt Tightened Check",
            "Suspension Springs Tightened Check"]
    
    GMES_data=pandas.DataFrame(columns=["Item"])

    for i in range(14):
        GMES_data.at[i,"Item"]=Item[i]
        

    #측정값 스펙  넣기
    for i in range(14):
        if i<7:
            if i%3==0:
                for j in range(5): # 스펙도 무작위로 추출
                    GMES_data.at[i,j]=randint(110,200) # 측정 갑, lower spec 까지 무작위 선출
                GMES_data.at[i,5]=randint(100,150) # lower Spec
                GMES_data.at[i,6]=GMES_data.at[i,5]+randint(0,200) # Upper Spec
            else:
                for j in range(6):
                    GMES_data.at[i,j]=round(uniform(1,2),2) # 측정 갑, lower spec 까지 무작위 선출
                GMES_data.at[i,6]=round(GMES_data.at[i,5]+uniform(0,1),2) # Upper Spec
        elif i<10:
            if i%2==0:
                for j in range(6): # 스펙도 무작위로 추출
                    GMES_data.at[i,j]=randint(400,410)
                GMES_data.at[i,6]=GMES_data.at[i,5]+randint(0,100) # Upper Spec
            else:
                for j in range(5):
                    GMES_data.at[i,j]=round(uniform(-0.5,0.5),2)
                GMES_data.at[i,5]=round(uniform(-1,0),2)
                GMES_data.at[i,6]=round(GMES_data.at[i,5]+uniform(0.5,2),2) # Upper Spec
        else:
            for j in range(6):
                GMES_data.at[i,j]=randint(200,300)
            GMES_data.at[i,6]=GMES_data.at[i,5]+randint(0,100) # Upper Spec

            
    # 데이터 평균 구하기

    import pandas as pd
    average_data=pd.DataFrame()
    for i in range(14):
        k=0
        for j in range(5):
            k=GMES_data.at[i,j]+k
        average_data.at["d",i]=round(k/5,2)
    
    #각 데이터 판단하기
    for i in range(14):
        for j in range(5):
            ins=float(GMES_data.at[i,j])
            lower_spec=float(GMES_data.at[i,5])
            upper_spec=float(GMES_data.at[i,6])
            if ins>=lower_spec and ins<=upper_spec:
                GMES_data.at[i,j+7]="OK"
            else:
                GMES_data.at[i,j+7]="NG"

            
    #Judge 모두 합치고 모두 OK이어야 OK이다.
    for i in range(14):
        k=''
        for j in range(5):
            k=GMES_data.at[i,j+7]+k
            j=j+1
        if k=='OKOKOKOKOK':
            GMES_data.at[i,'final']="OK"
        else:
            GMES_data.at[i,'final']="NG"

    # 정수는 정수 만들어주기
    for i in range(14):
        if i<7:
            if i%3==0:
                for j in range(7): # 스펙도 정수로 변환
                    GMES_data.at[i,j]=str(int(GMES_data.at[i,j]))
        elif i<10:
            if i%2==0:
                for j in range(7): 
                    GMES_data.at[i,j]=str(int(GMES_data.at[i,j]))
        else:
            for j in range(7):
                GMES_data.at[i,j]=str(int(GMES_data.at[i,j]))


    # 필요 없는 데이터 지우기
    GMES_data=GMES_data.drop([7,8,9,10,11],axis=1)

    # data col,row 이름 바꾸기
    Col=['Item','Measure# 1','Measure #2','Measure #3','Measure #4','Measure #5','Lower_Spec','Upper_Spec',"Judgement"]
    GMES_data.columns=Col
    Row=range(1,15)
    GMES_data.index=Row

    ############################# bw, dl data
    # bw_data, dl_data 만들기
    bw_data=pd.DataFrame()
    dl_data=pd.DataFrame()
    for i in range(5):
        for j in range(5):
            bw_data.at[i,j]=int(randint(62,125))
    for i in range(20):
        for j in range(5):
            dl_data.at[i,j]=round(uniform(3.6,5.9),2)
            dl_data.at[20-i,j]=round(uniform(4.0,5.0),2) #좀더 다양한 데이터 만들기

    # bw_data, dl_data col
    from datetime import date
    today=date.today()
    col_name=pd.DataFrame()
    for i in range(5):
        k= today - relativedelta(days=4-i)
        col_name.at["d",i]=k.strftime('%m/%d') # columns

    bw_data.columns=col_name.loc['d']
    dl_data.columns=col_name.loc['d']


    ############## plot의 요소들을 하나로 묶기
    fig, axes = plt.subplots(2,2)
    fig.set_size_inches(11,6)

    #################################################################### Balance Weight #########################################################3
    ############## 1x1 chart
    # Box Plot
    BW_Box=axes[0,0].boxplot(bw_data)

    # reference line
    axes[0,0].hlines(xmin=0, xmax=6.5, y=70,color='r', linestyles='--')
    axes[0,0].hlines(xmin=0, xmax=6.5, y=120,color='r', linestyles='--')
    axes[0,0].annotate('70', xy=(6.5, 69),ha='right', va='top',color='red',fontsize=9)
    axes[0,0].annotate('120', xy=(6.5, 119),ha='right', va='top',color='red',fontsize=9)

    # 꾸미기
    axes[0,0].set_title('Balance Weight Bolt Torque',fontsize=10)
    axes[0,0].set_xticklabels(bw_data.columns, fontsize=9)
    axes[0,0].set_ylim(60,130,10)
    axes[0,0].set_xlabel('Date',fontsize=9,color='gray')
    axes[0,0].set_ylabel('kgf*cm',fontsize=9,color='gray')

    ############# 2x1 Table
    bw_max=round(bw_data.max(),2)
    bw_min=round(bw_data.min(),2)
    bw_mean=round(bw_data.sum()/30,2)
    bw_table=pd.DataFrame([bw_max,bw_min,bw_mean])
    bw_table.index=["Maximum","Minimum","Mean"]

    axes[1,0].set_axis_off()
    cell_text=bw_table.values
    row_labels=["Maximum","Minimum","Average"]
    row_colours=["#B9EBD6","#B9EBD6","#B9EBD6"]
    import numpy as np
    col_colours=np.full(5,"#B9EBD6")

    BW_TABLE=axes[1,0].table(cellText=bw_table.values, rowLabels=row_labels, colLabels=bw_data.columns, loc='center', rowColours=row_colours, colColours=col_colours, cellLoc='center')
    BW_TABLE.auto_set_font_size(False)
    BW_TABLE.set_fontsize(9)
    BW_TABLE.auto_set_column_width(col=list(range(len(bw_table.columns))))
    axes[1,0].set_title('Balance Weight Bolt Torque Result',x=0.35,y=0.7,fontsize=10)

    #################################################################### Door Latch #########################################################3
    ############## 1x2 chart
    # Box Plot
    axes[0,1].boxplot(dl_data)

    # reference line 변수 설정
    axes[0,1].hlines(xmin=0, xmax=6.5, y=3.8,color='r', linestyles='--')
    axes[0,1].hlines(xmin=0, xmax=6.5, y=5.8,color='r', linestyles='--')
    axes[0,1].annotate('3.8', xy=(6.5, 3.78),ha='right', va='top',color='red',fontsize=9)
    axes[0,1].annotate('5.8', xy=(6.5, 5.78),ha='right', va='top',color='red',fontsize=9)

    axes[0,1].set_title('Door Latch Gap',fontsize=10)
    axes[0,1].set_xticklabels(dl_data.columns,fontsize=9)
    axes[0,1].set_ylim(3.5,6,0.5)
    axes[0,1].set_xlabel('Date',fontsize=9,color='gray')
    axes[0,1].set_ylabel('mm',fontsize=9,color='gray')

    ############# 2x2 Table
    dl_max=round(dl_data.max(),2)
    dl_min=round(dl_data.min(),2)
    dl_mean=round(dl_data.sum()/20,2)
    dl_table=pd.DataFrame([dl_max,dl_min,dl_mean])
    dl_table.index=["Maximum","Minimum","Average"]

    axes[1,1].set_axis_off()
    cell_text=dl_table.values
    row_labels=["Maximum","Minimum","Average"]
    row_colours=["#B9EBD6","#B9EBD6","#B9EBD6"]
    col_colours=np.full(6,"#B9EBD6")
    DL_TABLE=axes[1,1].table(cellText=dl_table.values, rowLabels=row_labels, colLabels=dl_data.columns ,loc='center', rowColours=row_colours, colColours=col_colours, cellLoc='center')
    DL_TABLE.auto_set_font_size(False)
    DL_TABLE.set_fontsize(9)
    DL_TABLE.auto_set_column_width(col=list(range(len(dl_table.columns))))
    axes[1,1].set_title('Door Latch Gap Result',x=0.35,y=0.7,fontsize=10)


    #그래프 간격 띄우기
    plt.tight_layout()

    # save fig
    plt.savefig('static/Line Audit1.png')

    ######################################################### GMES table 결과 도출 #####################################################
    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(11,3.4)
    ax.set_axis_off()

    col_colours=['#FBEEB0','#CED6FE','#CED6FE','#CED6FE','#CED6FE','#CED6FE','#C5EFE8','#C5EFE8','#FCD9E0']
    data_table=ax.table(cellText=GMES_data.values,rowLabels=GMES_data.index,colLabels=GMES_data.columns, loc='center',colLoc='center',rowLoc='left',cellLoc='left',colColours=col_colours)
    data_table.set_fontsize(9)
    data_table.auto_set_column_width(col=list(range(len(GMES_data.columns))))

    today=date.today()
    today=today.strftime('%m/%d')
    ax.set_title('Front Loader Line Audit Result ('+today+")",x=0.5, y=1.05,fontsize=10)


    #그래프 간격 띄우기
    plt.tight_layout()

    # save fig
    plt.savefig('static/Line Audit2.png')


