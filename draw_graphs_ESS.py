
#%%
# reads accumulate_ess_sysid_essid.csv files and draws graphs
# so.park@lge.com
# 2018.11.11
import pandas as pd
import os
import datetime
import shutil


#%%
figsize_x = 19*2
figsize_y = 10*2
start_date = datetime.datetime(2016, 11, 1)
end_date = datetime.datetime(2018, 11, 1)
# system_id = ''
# ess_id = ''


#%%
def read_event_file():
    df_e = pd.read_csv(tables_path + 'tb_e_event_history.csv', parse_dates=['event_start_date',5,6], index_col = ['event_start_date'])
    return df_e


#%%
def read_file(system_id, ess_id):
    global filename
    filename = 'accumulate_' + 'ess_' + system_id + '_' + ess_id + '.csv'
    df = pd.read_csv(src_path + filename, parse_dates=['C.target_date'], index_col = ['C.target_date'])
    return df


#%%
def plot_all(df, df_event):
    import matplotlib.pyplot as plt
    
    fig = plt.figure(figsize=(figsize_x,figsize_y), tight_layout=True)
    fig.suptitle('ess_' + system_id + '_' + ess_id, fontsize=16)
    
    plot_soh_temp(df, df_event, fig, 331)
    plt.grid()
    
    plot_soc(df, fig, 332)
    plt.grid()
    
    plot_pv(df, fig, 333)
    plt.grid()
    plot_charge(df, fig, 338)
    plt.grid()
    
    plot_load(df, fig, 335)
    plt.grid()
    plot_grid_buy(df, fig, 339)
    plt.grid()
    plot_grid_sell(df, fig, 336)
    plt.grid()
    plot_pv_load_buy_sell_pv_sell_ratio(df, fig, 337)
    plt.grid()
    plot_temp(df, fig, 334)
    plt.grid()

    fig.savefig(graphs_path + 'ess_' + system_id + '_' + ess_id + ' graph.png')
    plt.close()


#%%
def plot_soh(df, fig, position):
    ax1 = fig.add_subplot(position)
    ax2 = ax1.twinx()
    
    ax1.plot(df.index, df['C.batt1_v'], color='m', label='Battery Voltage')
    ax1.set_yticks([150, 200, 250])
    ax1.set_ylim(bottom=100, top=400)
    ax1.legend(loc=2)
    
    ax2.plot(df.index, df['C.batt1_soh'], color='k', label='SOH')
    ax2.set_ylim(bottom=79, top=103)
    ax2.set_yticks([80, 85, 90, 95, 100])
    ax2.set_xlim(left=start_date, right=end_date)
    ax2.legend(loc=1)
#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' SOH')


#%%
def plot_grid_buy(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.grid_p_buy'].div(1000), color='orange', label='Grid Buy (kW)')

    ax1.set_ylim(bottom=0, top=7)
#     ax1.set_yticks([2,4,6])
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Grid Buy')


#%%
def plot_grid_sell(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.grid_p_sell'].div(1000), color='skyblue', label='Grid Sell (kW)')

    ax1.set_ylim(bottom=0, top=7)
#     ax1.set_yticks([2,4,6])
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Grid Sell')


#%%
def plot_charge(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['accu_chg_e'].div(1000), color='r', label='CHG Accumulated (kWh)')
    ax1.plot(df.index, df['accu_dis_e'].div(1000), color='b', label='DISCHG Accumulated (kWh)')
    ax1.set_yticks([1000,2000,3000,4000])
    ax1.set_ylim(bottom=0, top=4000)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)
#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Charge & Discharge')
   
#     df['CHG_RATE'] = df['M.DIS_A'].div(df['M.CHG_A']).mul(100, fill_value=0)
    ax2 = ax1.twinx()
    ax2.plot(df.index, df['chg_dis_ratio'], color='k', label='Discharge/Charge %')
    ax2.set_ylim(bottom=80, top=120)
#     ax2.set_ylim(bottom=0, top=100)
    ax2.legend(loc=1)


#%%
def plot_pv_sell_ratio(df, fig, position):

    ax1 = fig.add_subplot(position)
    
    ax1.plot(df.index, df['pv_sell_ratio'], color='k', label='PV-sell ratio(%)')
    ax1.set_ylim(bottom=0, top=100)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)


#%%
def bar_events(df, fig, position):

    ax1 = fig.add_subplot(position)
    
    ax1.bar(df.index, 1, width=0.8, color='brown', label='event')
    ax1.set_ylim(bottom=0, top=1)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)


#%%
def plot_pv_load_buy_sell_pv_sell_ratio(df, fig, position):

    ax1 = fig.add_subplot(position)
    ax2 = ax1.twinx()
    
    ax1.plot(df.index, df['accu_pv_e'].div(1000), color='r', label='PV (kWh)')
    ax1.plot(df.index, df['accu_load_e'].div(1000), color='c', label='Load (kWh)')
    ax1.plot(df.index, df['accu_buy_e'].div(1000), color='orange', label='Grid Buy (kWh)')
    ax1.plot(df.index, df['accu_sell_e'].div(1000), color='skyblue', label='Grid Sell (kWh)')
    ax1.set_ylim(bottom=0, top=15000)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)
   
    ax2.plot(df.index, df['pv_sell_ratio'], color='k', label='PV-sell ratio(%)')
    ax2.set_ylim(bottom=0, top=100)
    ax2.set_xlim(left=start_date, right=end_date)
    ax2.legend(loc=1)


#%%
def plot_soc(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.batt1_soc'], color='g', label='SOC')
    ax1.set_yticks([0, 25, 50, 75, 100])
    ax1.set_ylim(bottom=-10, top=120)
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Battery SOC')


#%%
def plot_load(df, fig, position):

    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['C.load_p'].div(1000), color='c', label='Load (kW)')
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=7)
    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Load Power')


#%%
def plot_pv(df, fig, position):
    
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.string1_p'].add(df['M.string2_p']).div(1000), color='r', label='PV (kW)')
#     ax1.set_yticks([2,4,6])
    ax1.set_ylim(bottom=0, top=7)

    ax1.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' PV power')


#%%
def plot_temp(df, fig, position):
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['M.batt1_tmp'], color='y', label='Battery Temperature')
    ax1.set_yticks([5, 10, 15, 20, 25, 30, 35, 40,45,50])
    ax1.set_ylim(bottom=0, top=50)
    ax1.set_xlim(left=start_date, right=end_date)
    ax1.legend(loc=2)

#     ax1.set_title('ess_' + system_id + '_' + ess_id + ' Battery Temperature')


#%%
def plot_soh_temp(df, df_event, fig, position):
    ax1 = fig.add_subplot(position)

    ax1.plot(df.index, df['C.batt1_soh'], color='k', label='SOH')    

    ax2 = ax1.twinx()
#     ax2.plot(df.index, df['M.batt1_tmp'], color='y', label='Temperature')
    if df_event.shape[0] > 0 :    
        ax2.bar(df_event.index, 15, color='r', label='event')
    
    ax2.set_yticks([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
    ax1.set_yticks([80, 85, 90, 95, 100])
    ax2.set_ylim(bottom=0, top=50)
    ax1.set_ylim(bottom=78, top=104)
    ax2.set_xlim(left=start_date, right=end_date)

    ax1.legend(loc=2)
    ax2.legend(loc=1)


#%%
src_path = '..\\new_result\\'   # where .csv files are
graphs_path = '..\\graphs\\'    # where graphs will be written to
tables_path = '..\\tables\\'
filename = ''
file_list = os.listdir(src_path)


#%%
# list of ESS with high DC ratio
# ess_list = [['476','435'],['809','744'],['740','683'],['392','361'],['801','596'],['396','362'],['563','466'],['120','254'],
#             ['408','373'],['1721','1569'],['388','356'],['400','367'],['442','402'],['516','484'],['1605','1654'],['958','867'],
#             ['264','258'],['452','344'],['478','326'],['470','427'],['614','553'],['508','465'],['705','639'],['262','249'],
#             ['304','291'],['866','788'],['355','336']]

# list of ESS with low DC ratio
# ess_list = [['899','822'],['972','887'],['466','359'],['1739','1580'],['682','692'],['1285','1211'],['1111','1032'],
#             ['375','351'],['1096','1015'],['968','882'],['1717','1572'],['1087','997'],['1129','1053'],['1226','1143'],['1335','1258'],
#             ['666','604'],['1545','1425'],['1489','1378'],['897','820']]

# # ess_list = [['476','435']]
            
# df_e = read_event_file()

# for i in range(len(ess_list)):
#     global system_id, ess_id
#     system_id, ess_id = ess_list[i]
#     df_event = df_e.loc[df_e['ess_id'] == int(ess_id)]
# #     df_event = df_temp.loc[df_temp['event_code'] != 'P215']
#     df = read_file(system_id, ess_id)
#     plot_all(df, df_event)
#     del df
#     del df_event
# #     del df_temp

    
# del df_e


#%%
# 폴더 내 모든 파일 그래프 그리기

df_e = read_event_file()

for i in range(len(file_list)):
    global system_id, ess_id
    
    if (i<514):
        continue

    system_id = file_list[i].split('_')[2]
    ess_id = file_list[i].split('_')[3].split('.')[0]
    
    print("processing [" + str(i) + "] " + system_id + "_" + ess_id + "\t" + str(datetime.datetime.now()))

    df_event = df_e.loc[df_e['ess_id'] == int(ess_id)]
    
    df = read_file(system_id, ess_id)
    plot_all(df, df_event)
    del df
    del df_event
    
del df_e


