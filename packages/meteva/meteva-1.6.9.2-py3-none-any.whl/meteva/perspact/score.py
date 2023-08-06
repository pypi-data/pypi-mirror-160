import meteva
import numpy as np
import pandas as pd
import xarray as xr
import datetime
import collections

# 实现任意纬度分类的函数
def score_df(df, method, s = None,g=None,gll_dict = None,plot = None,**kwargs):
    '''

    :param df:
    :param method:
    :param g:
    :return:
    '''
    method_name = method.__name__
    method_mid = meteva.perspact.get_middle_method(method)
    column_list = meteva.perspact.get_middle_columns(method_mid)
    score_method_with_mid = meteva.perspact.get_score_method_with_mid(method)
    df0 = meteva.base.sta_data(df)

    column_df = df.columns
    if not set(column_list) <= set(column_df):
        print("input pandas.DataFrame must contains columns in list of "+ str(column_list) + " for mem." + method_name + " caculation")
        return None,None

    df1 = meteva.base.sele_by_dict(df0, s)

    if g is None:
        g = [g]
        gll_dict = None
        gll0 = None
    else:

        #将g转成列表形式
        if isinstance(g,str):
            g = [g]

        #gll_dict 初始化包含所有分类维度
        if gll_dict is None:
            gll_dict = {}
            for gg in range(len(g)):
                gll_dict[g[gg]] = None

        #对每个维度的分类方式进行赋值
        for gg in range(len(g)):
            if g[gg] not in gll_dict.keys() or  gll_dict[g[gg]] is None:
                if g[gg].find("time")>=0:
                    _,gll = meteva.base.group(df1,g = g[gg])
                else:
                    #为了保持原有排序，不用group函数
                    groups = df1[g[gg]]
                    groups = groups.drop_duplicates(keep="first")
                    gll = groups.values
                gll_dict[g[gg]] = gll

        # 将分组方式统一成单层列表，或者两层列表
        gll_dict1 = {}
        for gg in range(len(g)):
            list_list = gll_dict[g[gg]]
            has_list = False
            for list1 in list_list:
                if  isinstance(list1,list):
                    has_list = True
            if has_list:
                list_list1 = []
                for list1 in list_list:
                    if isinstance(list1, list):
                        list_list1.append(list1)
                    else:
                        list_list1.append([list1])
            else:
                list_list1 = list_list
            gll_dict1[g[gg]] = list_list1
        gll_dict = gll_dict1

        #取出第一个分类维度的分类方式备用
        gll0 = gll_dict[g[0]]

    g0 = g[0]
    df1_list, gll = meteva.base.group(df1, g=g0, gll=gll0)
    if len(g) == 1:
        score_list = []
        gll_i_dict ={}
        score1 = None
        for i in range(len(df1_list)):
            if method_mid == meteva.method.tmmsss:
                tmmsss_array = df1_list[i][column_list].values
                mid_array = tmmsss_array[0, :]
                for j in range(1, tmmsss_array.shape[0]):
                    mid_array = meteva.method.tmmsss_merge(mid_array, tmmsss_array[j, :])
            else:
                mid_list = []
                for column in column_list:
                    mid = np.sum(df1_list[i][column])
                    mid_list.append(mid)
                mid_array = np.array(mid_list)
            score1 = score_method_with_mid(mid_array)
            score_list.append(score1)
            gll_str = str(gll[i])
            gll_i_dict[gll_str] = i

        if gll0 is None:
            score_list_with_iv = score_list
        else:
            score_list_with_iv = []
            for j in range(len(gll0)):
                gll_str = str(gll0[j])
                if gll_str in gll_i_dict.keys():
                    score2 = score_list[gll_i_dict[gll_str]]
                else:
                    score2 = score1 * 0 + meteva.base.IV
                score_list_with_iv.append(score2)

        score_array = np.array(score_list_with_iv)

        if plot is not None:meteva.base.plot_tools.plot_bar(plot,score_array,name_list_dict=gll_dict,**kwargs)

        return  score_array,gll_dict
    else:
        if len(g) == 2:
            g_left = g[1]
        else:
            g_left = g[1:]

        gll_i_dict ={}
        score_all_list = []
        score_array = None
        for i in range(len(gll)):
            score_array,_ = score_df(df1_list[i], method,g = g_left, gll_dict = gll_dict,plot = None)
            score_all_list.append(score_array)
            gll_str = str(gll[i])
            gll_i_dict[gll_str] = i

        score_list_with_iv = []
        for j in range(len(gll0)):
            gll_str = str(gll0[j])
            if gll_str in gll_i_dict.keys():
                score2 = score_all_list[gll_i_dict[gll_str]]
            else:
                score2 = score_array * 0 + meteva.base.IV
            score_list_with_iv.append(score2)
        score_all_array = np.array(score_list_with_iv)

        if plot is not None:meteva.base.plot_tools.plot_bar(plot,score_all_array,name_list_dict=gll_dict,**kwargs)

        return score_all_array,gll_dict

def sele_by_dict(ds0,s):
    if s is None:
        return ds0
    else:
        ob_keys =[]
        not_ob_keys = []
        for key in s.keys():
            if key.find("ob_")>=0:
                ob_keys.append(key)
            else:
                not_ob_keys.append(key)

        #收集非观测时间相关的时间选取参数
        s_not_ob = {}
        #收集和dtime维度相关的选取参数
        dtime_s = ds0.dtime.values
        for key in not_ob_keys:
            list0 = s[key]
            if not isinstance(list0, list):
                list0 = [list0]
            if key =="dtime":
                dtime_s = list(set(dtime_s) & set(list0))
                if len(dtime_s) ==0:
                    return None
                dtime_s.sort()
                not_ob_keys.remove(key)
            elif key =="dtime_range":
                list1 = []
                for value in dtime_s:
                    if value>=s[key][0] and value<= s[key][1]:
                        list1.append(value)
                if len(list1) == 0:
                    return None
                else:
                    list1.sort()
                    dtime_s = list1
                not_ob_keys.remove(key)
        s_not_ob["dtime"] = dtime_s

        #收集和time维度相关的选取参数
        time_s = ds0.time.values
        for key in not_ob_keys:
            list0 = s[key]
            if not isinstance(list0, list):
                list0 = [list0]
            if key =="time":
                values_s1 = []
                for value in list0:
                    values_s1.append(meteva.base.all_type_time_to_time64(value))
                fo_times = pd.Series(0, index=time_s)
                time_s = time_s[fo_times.index.isin(values_s1)]
                if len(dtime_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="year":
                fo_times = pd.Series(0, index=time_s)
                time_s = time_s[fo_times.index.year.isin(list0)]
                if len(dtime_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="month":
                fo_times = pd.Series(0, index=time_s)
                time_s = time_s[fo_times.index.month.isin(list0)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="xun":
                fo_times = pd.Series(0, index=time_s)
                mons = fo_times.index.month.astype(np.int16)
                days = fo_times.index.day.astype(np.int16)
                xuns = np.ceil(days / 10).values.astype(np.int16)
                xuns[xuns > 3] = 3
                xuns += (mons - 1) * 3
                xuns = pd.Series(xuns)
                time_s = time_s[xuns.isin(list0)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="hou":
                fo_times = pd.Series(0, index=time_s)
                mons = fo_times.index.month.astype(np.int16)
                days = fo_times.index.day.astype(np.int16)
                hous = np.ceil(days / 5).values.astype(np.int16)
                hous[hous > 6] = 6
                hous += (mons - 1) * 6
                hous = pd.Series(hous)
                time_s = time_s[hous.isin(list0)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="day":
                days_list = []
                time0 = datetime.datetime(1900, 1, 1, 0, 0)
                seconds = 3600 * 24
                for day0 in list0:
                    day0 = meteva.base.tool.time_tools.all_type_time_to_datetime(day0)
                    day = int((day0 - time0).total_seconds() // seconds)
                    days_list.append(day)
                days = (time_s - meteva.base.all_type_time_to_time64(time0)) // np.timedelta64(1, "D")
                days = pd.Series(days)
                time_s = time_s[days.isin(days_list)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="dayofyear":
                fo_times = pd.Series(0, index=time_s)
                time_s = time_s[fo_times.index.dayofyear.isin(list0)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="hour":
                fo_times = pd.Series(0, index=time_s)
                time_s = time_s[fo_times.index.hour.isin(list0)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="minute":
                fo_times = pd.Series(0, index=time_s)
                time_s = time_s[fo_times.index.minute.isin(list0)]
                if len(time_s) == 0:
                    return None
                not_ob_keys.remove(key)
            elif key =="time_range":
                start_time = meteva.base.all_type_time_to_time64(list0[0])
                end_time = meteva.base.all_type_time_to_time64(list0[1])
                list1 = []
                for value in time_s:
                    if value>=start_time and value<= end_time:
                        list1.append(value)
                if len(list1) == 0:
                    return None
                else:
                    dtime_s = np.array(list1)
                not_ob_keys.remove(key)

        #根据观测时间参和可用时效确定实际可用的起报时间
        if len(ob_keys)>0:
            time_exp,dtime_exp = np.meshgrid(time_s,dtime_s)
            time_exp = time_exp.flattlen()
            dtime_exp = dtime_exp.flatten()
            dtimes = dtime_exp * np.timedelta64(1, 'h')
            obtimes = time_exp + dtime_exp

            for key in ob_keys:
                list0 = s[key]
                if not isinstance(list0, list):
                    list0 = [list0]
                if key =="ob_time":
                    values_s1 = []
                    for value in list0:
                        values_s1.append(meteva.base.all_type_time_to_time64(value))
                    fo_times = pd.Series(0, index=time_s)
                    time_s = time_s[fo_times.index.isin(values_s1)]
                    if len(dtime_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_year":
                    fo_times = pd.Series(0, index=time_s)
                    time_s = time_s[fo_times.index.year.isin(list0)]
                    if len(dtime_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_month":
                    fo_times = pd.Series(0, index=time_s)
                    time_s = time_s[fo_times.index.month.isin(list0)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_xun":
                    fo_times = pd.Series(0, index=time_s)
                    mons = fo_times.index.month.astype(np.int16)
                    days = fo_times.index.day.astype(np.int16)
                    xuns = np.ceil(days / 10).values.astype(np.int16)
                    xuns[xuns > 3] = 3
                    xuns += (mons - 1) * 3
                    xuns = pd.Series(xuns)
                    time_s = time_s[xuns.isin(list0)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_hou":
                    fo_times = pd.Series(0, index=time_s)
                    mons = fo_times.index.month.astype(np.int16)
                    days = fo_times.index.day.astype(np.int16)
                    hous = np.ceil(days / 5).values.astype(np.int16)
                    hous[hous > 6] = 6
                    hous += (mons - 1) * 6
                    hous = pd.Series(hous)
                    time_s = time_s[hous.isin(list0)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_day":
                    days_list = []
                    time0 = datetime.datetime(1900, 1, 1, 0, 0)
                    seconds = 3600 * 24
                    for day0 in list0:
                        day0 = meteva.base.tool.time_tools.all_type_time_to_datetime(day0)
                        day = int((day0 - time0).total_seconds() // seconds)
                        days_list.append(day)
                    days = (time_s - meteva.base.all_type_time_to_time64(time0)) // np.timedelta64(1, "D")
                    days = pd.Series(days)
                    time_s = time_s[days.isin(days_list)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_dayofyear":
                    fo_times = pd.Series(0, index=time_s)
                    time_s = time_s[fo_times.index.dayofyear.isin(list0)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_hour":
                    fo_times = pd.Series(0, index=time_s)
                    time_s = time_s[fo_times.index.hour.isin(list0)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_minute":
                    fo_times = pd.Series(0, index=time_s)
                    time_s = time_s[fo_times.index.minute.isin(list0)]
                    if len(time_s) == 0:
                        return None
                    not_ob_keys.remove(key)
                elif key =="ob_time_range":
                    start_time = meteva.base.all_type_time_to_time64(list0[0])
                    end_time = meteva.base.all_type_time_to_time64(list0[1])
                    list1 = []
                    for value in time_s:
                        if value>=start_time and value<= end_time:
                            list1.append(value)
                    if len(list1) == 0:
                        return None
                    else:
                        dtime_s = np.array(list1)
                    not_ob_keys.remove(key)



        s_not_ob["time"] = time_s

        #收集其它维度相关的参数
        for key in not_ob_keys:
            list0 = s[key]
            if not isinstance(list0, list):
                list0 = [list0]
            s_not_ob[key] =list0

        ds1 = ds0.sel(s_not_ob)



        return ds1

def score_xr(ds,method,s = None,g = None,gll_dict = None,plot = None,**kwargs):

    method_name = method.__name__
    method_mid = meteva.perspact.get_middle_method(method)
    value_list = meteva.perspact.get_middle_columns(method_mid)
    score_method_with_mid = meteva.perspact.get_score_method_with_mid(method)

    for value in value_list:
        if not value in ds:

            print("input xarray.DataSet must contains columns in list of " + str(
            value_list) + " for mem." + method_name + " caculation")
            return None, None


    ds1 = sele_by_dict(ds, s)
    print(ds1)
    if g is None:
        g = [g]
        gll_dict = None
        gll0 = None
    else:

        # 将g转成列表形式
        if isinstance(g, str):
            g = [g]

        # gll_dict 初始化包含所有分类维度
        if gll_dict is None:
            gll_dict = {}
            for gg in range(len(g)):
                gll_dict[g[gg]] = None

        # 对每个维度的分类方式进行赋值
        for gg in range(len(g)):
            if g[gg] not in gll_dict.keys() or gll_dict[g[gg]] is None:
                if g[gg].find("time") >= 0:
                    _, gll = meteva.base.group(ds1, g=g[gg])
                else:
                    # 为了保持原有排序，不用group函数
                    groups = ds1[g[gg]]
                    groups = groups.drop_duplicates(keep="first")
                    gll = groups.values
                gll_dict[g[gg]] = gll

        # 将分组方式统一成单层列表，或者两层列表
        gll_dict1 = {}
        for gg in range(len(g)):
            list_list = gll_dict[g[gg]]
            has_list = False
            for list1 in list_list:
                if isinstance(list1, list):
                    has_list = True
            if has_list:
                list_list1 = []
                for list1 in list_list:
                    if isinstance(list1, list):
                        list_list1.append(list1)
                    else:
                        list_list1.append([list1])
            else:
                list_list1 = list_list
            gll_dict1[g[gg]] = list_list1
        gll_dict = gll_dict1

        # 取出第一个分类维度的分类方式备用
        gll0 = gll_dict[g[0]]

    g0 = g[0]

    return None
if __name__ =="__main__":

    path = r"H:\test_data\input\meb\BSEP_NMC_RFFC_GOWFS_EME_AGLB_L88_P9_20220728000014412.txt"
    sta = meteva.base.read_stadata_from_sevp(path,meteva.base.sevp_element_id.温度)
    print(sta)

    # path = r"H:\test_data\input\mps\rain24.h5"
    # sta_all = pd.read_hdf(path)
    # path = r"H:\test_data\input\mps\station_id_province_name.dat"
    # id_province = pd.read_csv(path, sep="\\s+", header=None, usecols=[3, 4])
    # id_province.columns = ["id", "province"]
    # ds_all = meteva.perspact.middle_ds(sta_all,meteva.method.hfmc,grade_list=[0.1,10,25,50,100,250],gid=id_province)
    # ds_all.to_netcdf(r"H:\test_data\input\mps\hfmc_xr.nc")
    # ds_all = xr.open_dataset(r"H:\test_data\input\mps\hfmc_xr.nc")
    # result = sele_by_dict(ds_all,s = {"ob_time":["2022071508"]})
    # print(result)
    #


