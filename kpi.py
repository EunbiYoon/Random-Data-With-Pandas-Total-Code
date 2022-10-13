import pandas as pd
import numpy as np
import xlrd
from datetime import date,timedelta
import datetime
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
from email.mime.image import MIMEImage
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import figure
import calendar
from datetime import datetime
import pandas as pd
import pandas as pd
import numpy as np
import xlrd
from datetime import date
import io
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import figure
from datetime import date,timedelta
import datetime
from dateutil.relativedelta import relativedelta
import openpyxl
from random import*
import string


########### New Services 만들기 ##############
# 파일 불러오기
def kpi_graph():
   ## random dataframe 생성
   fsvc_target=randint(1300,1600)
   fsvc_Ctarget=fsvc_target*0.8
   fsales_target=randint(50000,70000)

   tsvc_target=randint(1500,1700)
   tsvc_Ctarget=tsvc_target*0.8
   tsales_target=randint(50000,70000)


   #3 Months Sales, SVC 마지막 날 dataframe 만들기
   today=date.today()
   YearNdate=pd.DataFrame(columns=["Month","Ndate"])
   for i in range(3):
      condition=int(today.strftime('%m'))-i
      if condition<=0:
         condition = condition+12 #12 -> 1월 넘어가는 구간
      YearNdate.at[i,"Month"]=condition

   #lunar year
   today=date.today()
   lunaryear=int(today.strftime('%y'))%4

   # 달의 마지막날 추출
   for i in range(3):
      condition=YearNdate.at[i,"Month"]
      a=0
      if condition==1 or condition==3 or condition==5 or condition==7 or condition==8 or condition==10 or condition==12:
         a=31
      elif condition==4 or condition==6 or condition==9 or condition==11:
         a=30
      elif condition==2:
         today=date.today()-datetime.timedelta(weeks=i*4)
         lunaryear=int(today.strftime('%y'))%4
         if lunaryear==0:
               a=29
         else:
               a=28
      else:
         print("Year End Month Error")
      YearNdate.at[i,"Ndate"]=a

   # Recent 3 Months SVC Sales data
   T3MSalesData=pd.DataFrame()
   F3MSalesData=pd.DataFrame()
   T3MSVCData=pd.DataFrame()
   F3MSVCData=pd.DataFrame()

   today=date.today()
   remove_day1=int(today.strftime('%d'))
   for i in range(3):
      if i==0 or i==1:
         for j in range(YearNdate.at[i,"Ndate"]):
               F3MSalesData.at[j,i]=randint(0,2200)
               F3MSVCData.at[j,i]=randint(0,80)
               T3MSalesData.at[j,i]=randint(0,2700)
               T3MSVCData.at[j,i]=randint(0,90)
      else:
         for j in range(remove_day1): #오늘도 실시간으로 업데이트 되는 상황
               F3MSalesData.at[j,i]=randint(0,2200)
               F3MSVCData.at[j,i]=randint(0,80)
               T3MSalesData.at[j,i]=randint(0,2700)
               T3MSVCData.at[j,i]=randint(0,90)
      


   # 누적 서비스 데이터 만들기 전에 그래프 옆의 테이블 위해 3Month Sum 구하기
   FSVCR3=F3MSVCData.sum()
   TSVCR3=T3MSVCData.sum()
   FSalesR3=F3MSalesData.sum()
   TSalesR3=T3MSalesData.sum()

   # 누적 서비스 데이터 만들기
   F3MSVCData=F3MSVCData.cumsum()
   T3MSVCData=T3MSVCData.cumsum()
   F3MSalesData=F3MSalesData.cumsum()
   T3MSalesData=T3MSalesData.cumsum()


   # 이번달의 SVC Sales 총합 만들기
   FSVC_Result=int(F3MSVCData.at[remove_day1-1,len(F3MSVCData.columns)-1]) #index 0부터 시작하니깐
   TSVC_Result=int(T3MSVCData.at[remove_day1-1,len(T3MSVCData.columns)-1])
   FSales_Result=int(F3MSalesData.at[remove_day1-1,len(F3MSalesData.columns)-1])
   TSales_Result=int(T3MSalesData.at[remove_day1-1,len(T3MSalesData.columns)-1])

   # 9months 랜덤 데이터 만들기
   FYear=pd.DataFrame()
   TYear=pd.DataFrame()
   for i in range(9):
      FYear.at[i,"SVC"]=randint(700,1600)
      FYear.at[i,"Sales"]=randint(28000,45000)
      TYear.at[i,"SVC"]=randint(900,1800)
      TYear.at[i,"Sales"]=randint(33000,50000)

   # Recent 3 months data 가져와서 넣기
   for i in range(3):  
      FYear.at[i+9,"SVC"]=FSVCR3[i]
      FYear.at[i+9,"Sales"]=FSalesR3[i]
      TYear.at[i+9,"SVC"]=TSVCR3[i]
      TYear.at[i+9,"Sales"]=TSalesR3[i]


   ########## 아래는 복사 붙여 넣기
   # start & end month date, pass & total business day
   # 매달 1일에는 마지막 달 마지막 날이 추출되는 조건 추가
   today=date.today()
   k=today.strftime('%d')
   if k=='01':
      print("first day of month")
      exp=today-relativedelta(days=1)
      startM0=exp.replace(day=1)
      pass_businessday=len(pd.bdate_range(startM0,exp))#이미 1뺐으니깐 더이상 뺄 필요 없음
      endM0=today-relativedelta(days=1)
      total_businessday=len(pd.bdate_range(startM0,endM0))
      today=today-relativedelta(days=1)
      
   else:
      print("not the first day of month")
      exp=today
      startM0=exp.replace(day=1)
      pass_businessday=len(pd.bdate_range(startM0,today))-1#어제 기준으로 보기때문에 1 빼기
      endM0=startM0+relativedelta(months=1)-relativedelta(days=1)
      total_businessday=len(pd.bdate_range(startM0,endM0))

   # FL TL Expected SVC data 추출
   FSVC_Exp=int(round(FSVC_Result*total_businessday/pass_businessday,0))
   TSVC_Exp=int(round(TSVC_Result*total_businessday/pass_businessday,0))
   FSales_Exp=int(round(FSales_Result*total_businessday/pass_businessday,0))
   TSales_Exp=int(round(TSales_Result*total_businessday/pass_businessday,0))


   # Target trend 만들기
   end_date=endM0.strftime('%d')
   end_date=int(end_date)

   FL_SVC_Target_Trend=np.arange(start = fsvc_target/end_date, stop = fsvc_target+fsvc_target/end_date, step = fsvc_target/end_date)
   FL_SVC_Target_Trend=FL_SVC_Target_Trend.astype(int)

   FL_SVC_CTarget_Trend=np.arange(start = fsvc_Ctarget/end_date, stop = fsvc_Ctarget, step = fsvc_Ctarget/end_date)
   FL_SVC_CTarget_Trend=FL_SVC_CTarget_Trend.astype(int)

   FL_Sales_Target_Trend=np.arange(start = fsales_target/end_date, stop = fsales_target+fsales_target/end_date, step = fsales_target/end_date)
   FL_Sales_Target_Trend=FL_Sales_Target_Trend.astype(int)

   TL_SVC_Target_Trend=np.arange(start = tsvc_target/end_date, stop = tsvc_target+tsvc_target/end_date, step = tsvc_target/end_date)
   TL_SVC_Target_Trend=TL_SVC_Target_Trend.astype(int)

   TL_SVC_CTarget_Trend=np.arange(start = tsvc_Ctarget/end_date, stop = tsvc_Ctarget, step = tsvc_Ctarget/end_date)
   TL_SVC_CTarget_Trend=TL_SVC_CTarget_Trend.astype(int)

   TL_Sales_Target_Trend=np.arange(start = tsales_target/end_date, stop = tsales_target+tsales_target/end_date, step = tsales_target/end_date)
   TL_Sales_Target_Trend=TL_Sales_Target_Trend.astype(int)


   # Target data 추출
   today=date.today()
   yesterday=int(today.strftime('%d'))-1

   FSVC_Target= int(round(fsvc_target*yesterday/end_date,0))  
   FSVC_CTarget= int(round(fsvc_Ctarget*yesterday/end_date,0))
   FSales_Target=int(round(fsales_target*yesterday/end_date,0))

   TSVC_Target=int(round(tsvc_target*yesterday/end_date,0))
   TSVC_CTarget=int(round(tsvc_Ctarget*yesterday/end_date,0))
   TSales_Target=int(round(tsales_target*yesterday/end_date,0))


   ####  STATUS ####
   # FL SVC Status data 추출
   FSVC_Diff=int(round(FSVC_Result-FSVC_Target,0))
   FSVC_DPer=int(round(FSVC_Diff*100/FSVC_Target,0))

   if FSVC_Result-FSVC_Target>=0:
      FSVC_Status="Base: "+str(FSVC_Diff)+"EA ("+str(FSVC_DPer)+"%↑)"+" Challenge: "+str(FSVC_Diff)+"EA ("+str(FSVC_DPer)+"%↑)"
   elif FSVC_Result-FSVC_Target<0:
      FSVC_Status=str(FSVC_Diff)+"EA ("+str(FSVC_DPer)+"%↓)"
   else:
      print("Error")

   # FL SVC C Status data 추출
   FSVC_CDiff=int(round(FSVC_Result-FSVC_CTarget,0))
   FSVC_CDPer=int(round(FSVC_CDiff*100/FSVC_CTarget,0))

   if FSVC_Result-FSVC_CTarget>=0:
      FSVC_CStatus=str(FSVC_CDiff)+"EA ("+str(FSVC_CDPer)+"%↑)"
   elif FSVC_Result-FSVC_CTarget<0:
      FSVC_CStatus=str(FSVC_CDiff)+"EA ("+str(FSVC_CDPer)+"%↓)"
   else:
      print("Error")

   # FL Sales Status data 추출
   FSales_Diff=int(round(FSales_Result-FSales_Target,0))
   FSales_DPer=int(round(FSales_Diff*100/FSales_Target,0))
   if FSales_Diff >= 0:
      FSales_Status=str(FSales_Diff)+"EA ("+str(FSales_DPer)+"%↑)"
   elif FSales_Diff < 0:
      FSales_Status=str(FSales_Diff)+"EA ("+str(FSales_DPer)+"%↓)"
   else:
      print("Error")

   # TL SVC Status data 추출
   TSVC_Diff=int(round(TSVC_Result-TSVC_Target,0))
   TSVC_DPer=int(round(TSVC_Diff*100/TSVC_Target,0))
   if TSVC_Result-TSVC_Target>=0:
      TSVC_Status=str(TSVC_Diff)+"EA ("+str(TSVC_DPer)+"%↑)"
   elif TSVC_Result-TSVC_Target<0:
      TSVC_Status=str(TSVC_Diff)+"EA ("+str(TSVC_DPer)+"%↓)"
   else:
      print("Error")

   # TL SVC C Status data 추출
   TSVC_CDiff=int(round(TSVC_Result-TSVC_CTarget,0))
   TSVC_CDPer=int(round(TSVC_CDiff*100/TSVC_CTarget,0))
   if TSVC_Result-TSVC_CTarget>=0:
      TSVC_CStatus=str(TSVC_CDiff)+"EA ("+str(TSVC_CDPer)+"%↑)"
   elif TSVC_Result-TSVC_CTarget<0:
      TSVC_CStatus=str(TSVC_CDiff)+"EA ("+str(TSVC_CDPer)+"%↓)"
   else:
      print("Error")

   # TL Sales Status data 추출
   TSales_Diff=int(round(TSales_Result-TSales_Target,0))
   TSales_DPer=int(round(TSales_Diff*100/TSales_Target,0))
   if TSales_Result-TSales_Target>=0:
      TSales_Status=str(TSales_Diff)+"EA ("+str(TSales_DPer)+"%↑)"
   elif TSales_Result-TSales_Target<0:
      TSales_Status=str(TSales_Diff)+"EA ("+str(TSales_DPer)+"%↓)"
   else:
      print("Error")


   ################################################################################ 테이블 ################################################
   ############## plot의 요소들을 하나로 묶기
   fig, ax = plt.subplots()
   fig.set_size_inches(9, 1)
   ax.set_axis_off()

   # SVC 생성
   table_vals=[[FSVC_Target,FSVC_CTarget,FSVC_Result,FSVC_Status,FSVC_CStatus,FSVC_Exp],[TSVC_Target, TSVC_CTarget,TSVC_Result, TSVC_Status, TSVC_CStatus,TSVC_Exp]]
   col_labels=['Base Target',"Challenge Target",'Result','Base T.Status','Challenge T.Status',"Expected Closing"]
   row_labels=["Front Loader","Top Loader"]
   SVC_table=ax.table(cellText=table_vals, rowLabels=row_labels, colLabels=col_labels, loc='center', cellLoc='center')
   SVC_table.auto_set_font_size(False)
   SVC_table.set_fontsize(10)
   SVC_table.auto_set_column_width(col=list(range(len(col_labels)-1)))

   #그림 저장
   plt.tight_layout()
   plt.savefig('static/fig1.png')

   ############## plot의 요소들을 하나로 묶기
   fig, ax = plt.subplots()
   fig.set_size_inches(6.5, 1)
   ax.set_axis_off()

   # Sales 생성
   table_vals=[[FSales_Target,FSales_Result,FSales_Status,FSales_Exp],[TSales_Target,TSales_Result, TSales_Status, TSales_Exp]]
   col_labels=['Target','Result','Status',"Expected Closing"]
   row_labels=["Front Loader","Top Loader"]
   SVC_table=ax.table(cellText=table_vals, rowLabels=row_labels, colLabels=col_labels, loc='center', cellLoc='center')
   SVC_table.auto_set_font_size(False)
   SVC_table.set_fontsize(10)
   SVC_table.auto_set_column_width(col=list(range(len(col_labels)-1)))

   #그림 저장
   plt.tight_layout()
   plt.savefig('static/fig2.png')


   ##############################################그래프 만들기##########################################################3
   ############## plot의 요소들을 하나로 묶기
   fig, ax = plt.subplots(2,2)
   fig = plt.figure(constrained_layout = True, figsize=(11,8))
   gs = fig.add_gridspec(8,11)
   ax[0,0] = fig.add_subplot(gs[0:4,0:8])
   ax[0,1] = fig.add_subplot(gs[0:4,9:11])
   ax[1,0] = fig.add_subplot(gs[4:9,0:8])
   ax[1,1] = fig.add_subplot(gs[4:9,9:11])

   ############# FL 그래프 그리기
   # column 이름 정하기
   Data0M=today.strftime('%Y-%m')
   date0M_name=today.strftime('%y.%m')

   date1M_name=today-relativedelta(months=1)
   Data1M=date1M_name.strftime('%Y-%m')
   date1M_name=date1M_name.strftime('%y.%m')

   date2M_name=today-relativedelta(months=2)
   Data2M=date2M_name.strftime('%Y-%m')
   date2M_name=date2M_name.strftime('%y.%m')

   # color 리스트
   ax[0,0].plot(F3MSVCData[len(F3MSVCData.columns)-3],linestyle='-', linewidth=1.0,color='#CBCFC9',label='FL_SVC_'+date2M_name) # SVC
   ax[0,0].plot(F3MSVCData[len(F3MSVCData.columns)-2],linestyle='-', linewidth=1.0,color='black',label='FL_SVC_'+date1M_name) # SVC
   ax[0,0].plot(F3MSVCData[len(F3MSVCData.columns)-1], linestyle='-', marker='o', linewidth=2.0,color='red',label='FL_SVC_'+date0M_name) # SVC

   ax[0,0].plot(FL_SVC_Target_Trend,linestyle='-', linewidth=1.0,color='green',label="'"+date0M_name+' Base Target') # SVC # Twinx 만들기 위함
   ax[0,0].plot(FL_SVC_CTarget_Trend,linestyle='--', linewidth=1.0,color='green',label="'"+date0M_name+' Challenge Target') # SVC # Twinx 만들기 위함
   ax[0,0].set_ylabel('SVC',color='gray')

   #twinx로 sale 데이터
   ax00T = ax[0,0].twinx()
   ax00T.set_ylabel('Sales',color='gray')
   F3MSalesData.columns=['FL_Sales_'+date2M_name,'FL_Sales_'+date1M_name,'FL_Sales_'+date0M_name]
   F3MSalesData[['FL_Sales_'+date2M_name,'FL_Sales_'+date1M_name,'FL_Sales_'+date0M_name]].plot(kind='bar',color=['#C0B8CD','#B8DAFD','#F3BA0A'],ax=ax00T)


   #FL 그래프 UI
   ax00T.set_title("Front Loader Service & Sales Status",fontsize=13)
   ax[0,0].set_xlabel("Date",color='gray')
   ax[0,0].set_xticks(np.arange(0,31,step=1))
   ax[0,0].set_xticklabels(range(1,32))
   ax[0,0].set_xlim(-.5,30.5)
   ax[0,0].set_ylim(0,1600)
   ax00T.set_ylim(0,140000)

   #legend
   ax[0,0].legend(loc='upper left')
   ax00T.legend(loc='upper left',bbox_to_anchor=(0.3,1))


   ############# TL 그래프 그리기
   # column 이름 정하기 -> front loader 사용하기
   # color 리스트
   ax[1,0].plot(T3MSVCData[len(T3MSVCData.columns)-3],linestyle='-', linewidth=1.0,color='#CBCFC9',label='TL_SVC_'+date2M_name) # SVC
   ax[1,0].plot(T3MSVCData[len(T3MSVCData.columns)-2],linestyle='-', linewidth=1.0,color='black',label='TL_SVC_'+date1M_name) # SVC
   ax[1,0].plot(T3MSVCData[len(T3MSVCData.columns)-1], linestyle='-', marker='o', linewidth=2.0,color='red',label='TL_SVC_'+date0M_name) # SVC

   ax[1,0].plot(TL_SVC_Target_Trend,linestyle='-', linewidth=1.0,color='green',label="'"+date0M_name+' Base Target') # SVC # Twinx 만들기 위함
   ax[1,0].plot(TL_SVC_CTarget_Trend,linestyle='--', linewidth=1.0,color='green',label="'"+date0M_name+' Challenge Target') # SVC # Twinx 만들기 위함
   ax[1,0].set_ylabel('SVC',color='gray')

   #twinx로 sale 데이터
   ax10T = ax[1,0].twinx()
   ax10T.set_ylabel('Sales',color='gray')
   T3MSalesData.columns=['TL_Sales_'+date2M_name,'TL_Sales_'+date1M_name,'TL_Sales_'+date0M_name]
   T3MSalesData[['TL_Sales_'+date2M_name,'TL_Sales_'+date1M_name,'TL_Sales_'+date0M_name]].plot(kind='bar',color=['#C0B8CD','#B8DAFD','#F3BA0A'],ax=ax10T)

   #TL 그래프 UI
   ax10T.set_title("Top Loader Service & Sales Status",fontsize=13)
   ax[1,0].set_xlabel("Date",color='gray')
   ax[1,0].set_xticks(np.arange(0,31,step=1))
   ax[1,0].set_xticklabels(range(1,32))
   ax[1,0].set_xlim(-.5,30.5)
   ax[1,0].set_ylim(0,1800)
   ax10T.set_ylim(0,140000)

   #legend
   ax[1,0].legend(loc='upper left')
   ax10T.legend(loc='upper left',bbox_to_anchor=(0.3,1))


   ############# 그래프 옆의 테이블  그리기
   ############# FL 그래프 그리기
   # row 이름 정하기
   Data0M=today.strftime('%Y-%m')
   row_label=pd.DataFrame()
   for i in range(12):
      name=today-relativedelta(months=11-i)
      row_label.at[i,"Month"]=name.strftime("'%y.%m")
   row_label=row_label["Month"].values.tolist()

   FYear.index=row_label
   TYear.index=row_label

   # FL 테이블 생성
   ax[0,1].set_axis_off()
   row_colours=np.full(len(row_labels),'#D5DEDE')
   col_colours=['#FAC69E','#FAC69E']
   FL_table=ax[0,1].table(cellText=FYear.values.astype(int),rowLabels=FYear.index,colLabels=FYear.columns,rowColours=np.full(12,'#D5DEDE'),colColours=col_colours,loc='center',cellLoc='center')
   FL_table.auto_set_font_size(False)
   FL_table.set_fontsize(9)
   FL_table.auto_set_column_width(col=list(range(len(FYear.columns))))

   #rowColours=row_colours, colColours=col_colours
   # TL 테이블 생성
   ax[1,1].set_axis_off()
   TL_table=ax[1,1].table(cellText=TYear.values.astype(int),rowLabels=TYear.index,colLabels=TYear.columns,rowColours=np.full(12,'#D5DEDE'),colColours=col_colours,loc='center',cellLoc='center')
   TL_table.auto_set_font_size(False)
   TL_table.set_fontsize(9)
   TL_table.auto_set_column_width(col=list(range(len(TYear.columns))))
   #fontweight='bold'


   #그래프 간격 띄우기
   plt.tight_layout()
   plt.savefig('static/fig3.png')
   

