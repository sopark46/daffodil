
# coding: utf-8

# In[1]:


# reads accumulate_ess_sysid_essid.csv files and draws graphs
# so.park@lge.com
# 2019.11.11
import pandas as pd
import os
import datetime
import shutil


# In[2]:


figsize_x = 44*5
figsize_y = 12*2


# In[3]:


# start_date = datetime.datetime(2016, 9, 1)
year = 2018
month = 3
start_date = datetime.datetime(year, month, 1)
end_date = start_date + datetime.timedelta(30)
# system_id = ''
# ess_id = ''


# In[4]:


def read_file(system_id, ess_id):
    global filename
    filename = 'accumulate_' + 'ess_' + system_id + '_' + ess_id + '.csv'
    df = pd.read_csv(src_path + filename, parse_dates=['C.target_date'], index_col = ['C.target_date'])
    return df


# In[5]:


def read_event_file():
    df = pd.read_csv(tables_path + 'tb_e_event_history.csv', parse_dates=['event_start_date',5,6], index_col = ['event_start_date'])
    return df


# In[6]:


def plot_monthly(df, df_event, year, month):
    import matplotlib.pyplot as plt
    global start_date, end_date
    start_date = datetime.datetime(year, month, 1)
    end_date = start_date + datetime.timedelta(30) # 매월의 날수를 계산하기 귀찮아서 30으로 퉁침
    
    if end_date < df.index[0] or start_date > df.index[-1]:
        return
    
    fig = plt.figure(figsize=(figsize_x,figsize_y), tight_layout=True)
    fig.suptitle('ess_' + system_id + '_' + ess_id, fontsize=16)
    
    plot_load_pv(df, fig, 511)
    plt.grid()
    
    plot_grid_buy_sell_pv(df, fig, 512)
    plt.grid()   
    
    plot_soc_chg_dis_pv(df, fig, 513)
    plt.grid()
    
    plot_soh_event(df, df_event, fig, 514)
    plt.grid()
    
    plot_pv1_2(df, fig, 515)
    plt.grid()

    

    

#     plot_soh_temp(df, fig)
#     plot_pv_power(df, fig)
#     plot_temp_charge(df, fig)
#     plot_soc_charge(df, fig)

    fig.savefig(daily_path + 'ess_' + system_id + '_' + ess_id + '_' + str(year) + '_' + str(month) + '.png')
    plt.close()


# In[7]:


def plot_soh(df, fig, position):
    ax1 = fig.add_subplot(position)
    
    ax2 = ax1.twinx()
    ax1.plot(df.index, df['C.batt1_v'], color='m', label='Battery Voltage')
    ax1.set_yticks([150, 200, 250])
    ax1.set_ylim(bottom=100, top=400)
    ax1.legend(loc=2)
    
    ax2.plot(df.index, df['C.batt1_soh'], color='k', label='SOH')
    ax2.set_ylim(bottom=79, top=101)
    ax2.set_yticks([80, 85, 90, 95, 100])
    ax2.set_xlim(left=start_date, right=end_date)
    ax2.legend(loc=1)
#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' SOH')


# In[8]:


def plot_grid_buy_sell_pv(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.string1_p'].add(df['M.string2_p']).div(1000), color='grey', label='PV (kW)')
    ax1.plot(df.index, df['M.grid_p_buy'].div(1000), color='orange', label='Grid Buy (kW)')
    ax1.plot(df.index, df['M.grid_p_sell'].div(1000), color='skyblue', label='Grid Sell (kW)')

    ax1.set_ylim(bottom=0, top=6)
#     ax1.set_yticks([2,4,6])
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Grid Buy')


# In[9]:


def plot_grid_buy(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.grid_p_buy'].div(1000), color='r', label='Grid Buy (kW)')

    ax1.set_ylim(bottom=0, top=6)
#     ax1.set_yticks([2,4,6])
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Grid Buy')


# In[10]:


def plot_grid_sell(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.grid_p_sell'].div(1000), color='skyblue', label='Grid Sell (kW)')

    ax1.set_ylim(bottom=0, top=6)
#     ax1.set_yticks([2,4,6])
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Grid Sell')


# In[11]:


def plot_grid(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.grid_p_buy'].div(1000), color='r', label='Grid Buy')
    ax1.plot(df.index, df['M.grid_p_sell'].div(1000), color='skyblue', label='Grid Sell')

    ax1.set_ylim(bottom=0, top=2)
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Grid Buy & Sell')


# In[12]:


def plot_soh_event(df, df_event, fig, position):
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['C.batt1_soh'], color='k', label='SOH')    

    ax2 = ax1.twinx()
#     ax2.plot(df.index, df['M.batt1_tmp'], color='y', label='Temperature')
    
    if df_event.shape[0] > 0 :
        ax2.bar(df_event.index, 40, width=0.004, color='r', label='event')
    
    ax2.set_yticks([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax1.set_yticks([80, 85, 90, 95, 100])
    ax2.set_ylim(bottom=0, top=50)
    ax1.set_ylim(bottom=78, top=104)
    ax2.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)
    ax2.legend(loc=1)


# In[13]:


def plot_charge_a(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.CHG_A'].div(1000), color='r', label='CHG Accumulated (kWh)')
    ax1.plot(df.index, df['M.DIS_A'].div(1000), color='b', label='DISCHG Accumulated (kWh)')
    ax1.set_yticks([1000,2000,3000,4000])
    ax1.set_ylim(bottom=0, top=4000)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)
#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Charge & Discharge')
   
    df['CHG_RATE'] = df['M.DIS_A'].div(df['M.CHG_A']).mul(100, fill_value=0)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['CHG_RATE'], color='k', label='Discharge/Charge %')
    ax2.set_ylim(bottom=80, top=115)
#     ax2.set_ylim(bottom=0, top=100)
    ax2.legend(loc=1)


# In[14]:


def plot_charge(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.batt1_chg'].div(1000), color='r', label='CHG (kWh)')
    ax1.plot(df.index, df['M.batt1_dis'].div(1000), color='b', label='DISCHG (kWh)')
#     ax1.set_yticks([1, 2, 3, 4, 5, 6])
    ax1.set_ylim(bottom=0, top=1.5)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)
#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Charge & Discharge')


# In[15]:


def plot_soc_chg_dis_pv(df, fig, position):

    ax1 = fig.add_subplot(position)
    ax2 = ax1.twinx()

    ax1.plot(df.index, df['M.batt1_soc'], color='g', label='SOC')
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.set_ylim(bottom=-40, top=110)
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)
    
    ax2.plot(df.index, df['M.string1_e'].add(df['M.string2_e']).div(1000), color='grey', label='PV (kWh)')
    ax2.plot(df.index, df['M.batt1_chg'].div(1000), color='r', label='CHG (kWh)')
    ax2.plot(df.index, df['M.batt1_dis'].div(1000), color='b', label='DISCHG (kWh)')
#     ax1.set_yticks([1, 2, 3, 4, 5, 6])
    ax2.set_ylim(bottom=0, top=1.5)
    ax2.legend(loc=1)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Battery SOC')


# In[16]:


def plot_soc(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.batt1_soc'], color='g', label='SOC')
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.set_ylim(bottom=-20, top=120)
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Battery SOC')


# In[17]:


def plot_load_pv(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['C.load_p'].div(1000), color='c', label='Load (kW)')
    ax1.plot(df.index, df['M.string1_p'].add(df['M.string2_p']).div(1000), color='grey', label='PV (kW)')
    
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=6)
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Load Power')


# In[18]:


def plot_pv1_2(df, fig, position):
    
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.string1_p'].add(df['M.string2_p']).div(1000), color='r', label='PV1+PV2 (kW)')
    ax1.plot(df.index, df['M.string1_p'].div(1000), color='y', label='PV1 (kW)')
    ax1.plot(df.index, df['M.string2_p'].div(1000), color='m', label='PV2 (kW)')
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=6)

    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' PV power')


# In[19]:


def plot_pv1(df, fig, position):
    
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.string1_p'].div(1000), color='r', label='PV1 (kW)')
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=6)

    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' PV power')


# In[20]:


def plot_pv2(df, fig, position):
    
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.string2_p'].div(1000), color='r', label='PV2 (kW)')
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=6)

    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' PV power')


# In[21]:


def plot_pv(df, fig, position):
    
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.string1_p'].add(df['M.string2_p']).div(1000), color='r', label='PV (kW)')
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=6)

    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' PV power')


# In[22]:


def plot_temp(df, fig, position):
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.batt1_tmp'], color='y', label='Battery Temperature')
    ax1.set_yticks([5, 10, 15, 20, 25, 30, 35, 40])
    ax1.set_ylim(bottom=10, top=40)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Battery Temperature')


# In[23]:


src_path = '..\\new_result\\'   # where .csv files are
graphs_path = '..\\graphs\\'    # where graphs will be written to
tables_path = '..\\tables\\'
# daily_path = ''
filename = ''
file_list = os.listdir(src_path)


# In[24]:


# 리스트 내 모든 파일의 그래프 그리기
# list of high DC ratio
# ess_list = [['476','435'],['809','744'],['740','683'],['392','361'],['801','596'],['396','362'],['563','466'],['120','254'],
#             ['408','373'],['1721','1569'],['388','356'],['400','367'],['442','402'],['516','484'],['1605','1654'],['958','867'],
#             ['264','258'],['452','344'],['478','326'],['470','427'],['614','553'],['508','465'],['705','639'],['262','249'],
#             ['304','291'],['866','788'],['355','336']]

# list of low DC ratio
# ess_list = [['899','822'],['972','887'],['466','359'],['1739','1580'],['682','692'],['1285','1211'],['1111','1032'],
#             ['375','351'],['1096','1015'],['968','882'],['1717','1572'],['1087','997'],['1129','1053'],['1226','1143'],['1335','1258'],
#             ['666','604'],['1545','1425'],['1489','1378'],['897','820'], ['270','263'], ['1340','1269'],['1050','968'],['741','680']]

# df_e = read_event_file()

# print('drawing graphs to ' + graphs_path)

# for i in range(len(ess_list)):
#     global system_id, ess_id
#     global daily_path
    
#     system_id, ess_id = ess_list[i]

#     df = read_file(system_id, ess_id)
#     df_event = df_e.loc[df_e['ess_id'] == int(ess_id)]    
#     daily_path = graphs_path + system_id + '_' + ess_id + '\\'    
#     if os.path.isdir(daily_path) == False :
#         os.makedirs(daily_path)
        
#     print("processing ["+ str(i) + "] : " + system_id + "_" + ess_id + "\t" + str(datetime.datetime.now()))
#     plot_monthly(df, df_event, 2016, 11)
#     plot_monthly(df, df_event, 2016, 12)
#     for month in range (1, 13):
#         plot_monthly(df, df_event, 2017, month)
#     for month in range (1, 12):
#         plot_monthly(df, df_event, 2018, month)
        
#     del df
#     del df_event
    
# del df_e


# In[25]:


# 폴더 내 모든 파일의 그래프 그리기
df_e = read_event_file()

for i in range(len(file_list)):
    global system_id, ess_id
    global daily_path
    
    if (i<1006):
        continue

    system_id = file_list[i].split('_')[2]
    ess_id = file_list[i].split('_')[3].split('.')[0]
    df = read_file(system_id, ess_id)
    df_event = df_e.loc[df_e['ess_id'] == int(ess_id)]
    
    daily_path = graphs_path + system_id + '_' + ess_id + '\\'    
    if os.path.isdir(daily_path) == False :
        os.makedirs(daily_path)

    print("processing ["+ str(i) + "] : " + system_id + "_" + ess_id + "\t" + str(datetime.datetime.now()))    
    
    plot_monthly(df, df_event, 2016, 9)
    plot_monthly(df, df_event, 2016, 10)
    plot_monthly(df, df_event, 2016, 11)
    plot_monthly(df, df_event, 2016, 12)
    for month in range (1, 13):
        plot_monthly(df, df_event, 2017, month)
    for month in range (1, 12):
        plot_monthly(df, df_event, 2018, month)
        
    del df
    del df_event
    
del df_e

