import meteva
import numpy as np
import datetime
import copy
import time
import pandas as pd
import os


def get_score_method_with_mid(method):
    hfmc_list = [
        meteva.method.ts,meteva.method.bias,meteva.method.ets,meteva.method.mr,meteva.method.far,
        meteva.method.r,meteva.method.hss_yesorno,meteva.method.pofd,meteva.method.pod,
        meteva.method.dts,meteva.method.orss,meteva.method.pc,meteva.method.roc,meteva.method.sr,
        meteva.method.hk_yesorno,meteva.method.odds_ratio,meteva.method.ob_fo_hr,meteva.method.ob_fo_hc
    ]
    hfmc_of_sum_rain_list = [meteva.method.pc_of_sun_rain]
    tase_list = [meteva.method.me, meteva.method.mae, meteva.method.mse, meteva.method.rmse]
    tc_list = [meteva.method.correct_rate,meteva.method.wrong_rate]
    tmmsss_list = [meteva.method.residual_error, meteva.method.residual_error_rate,meteva.method.corr]
    method_mid = None
    method_name = method.__name__
    if method in hfmc_of_sum_rain_list:
        method_mid = getattr(meteva.method, method_name + "_hfmc")
    elif method in hfmc_list:
        method_mid  = getattr(meteva.method, method_name +"_hfmc")
    elif method in tase_list:
        method_mid = getattr(meteva.method, method_name + "_tase")
    elif method in tc_list:
        method_mid = getattr(meteva.method, method_name + "_tc")
    elif method in tmmsss_list:
        method_mid = getattr(meteva.method, method_name + "_tmmsss")
    return method_mid


def get_middle_method(method):
    hfmc_list = [
        meteva.method.ts,meteva.method.bias,meteva.method.ets,meteva.method.mr,meteva.method.far,
        meteva.method.r,meteva.method.hss_yesorno,meteva.method.pofd,meteva.method.pod,
        meteva.method.dts,meteva.method.orss,meteva.method.pc,meteva.method.roc,meteva.method.sr,
        meteva.method.hk_yesorno,meteva.method.odds_ratio,meteva.method.ob_fo_hr,meteva.method.ob_fo_hc
    ]
    hfmc_of_sum_rain_list = [meteva.method.pc_of_sun_rain]
    tase_list = [meteva.method.me, meteva.method.mae, meteva.method.mse, meteva.method.rmse]
    tc_list = [meteva.method.correct_rate,meteva.method.wrong_rate]
    tmmsss_list = [meteva.method.residual_error, meteva.method.residual_error_rate,meteva.method.corr]
    method_mid = None
    method_name = method.__name__
    if method in hfmc_of_sum_rain_list:
        method_mid = meteva.method.hfmc_of_sun_rain
    elif method in hfmc_list:
        method_mid  = meteva.method.hfmc
    elif method in tase_list:
        method_mid = meteva.method.tase
    elif method in tc_list:
        method_mid = meteva.method.tc_count
    elif method in tmmsss_list:
        method_mid = meteva.method.tmmsss
    return method_mid

def get_middle_columns(method):
    if method == meteva.method.hfmc_of_sun_rain:
        return ["Hsr","Fsr","Msr","Csr"]
    elif method == meteva.method.hfmc:
        return ["H","F","M","C"]
    elif method == meteva.method.tase:
        return ["T", "E", "A", "S"]
    elif method == meteva.method.tc_count:
        return ["T", "C"]
    elif method == meteva.method.tmmsss:
        return  ["T", "MX","MY","SX","SY","SXY"]
    else:
        print("暂无支持")
        pass


def middle_df(sta_all,method,grade_list = None,compare = None,gid = None):
    '''

    :param sta_all:
    :param method:
    :param grade_list:
    :param compare:
    :param gid:
    :return:
    '''

    mid_columns = get_middle_columns(method)
    method_args = {}
    if grade_list is not None:
        method_args["grade_list"] = grade_list
    if compare is not None:
        method_args["compare"] = compare
    grade_exp = None
    names_exp = None
    group_name = None
    if gid is not None:
        group_name = gid.columns[1]
        groups = gid[group_name]
        groups = groups.drop_duplicates(keep = "first")
        names = groups.values
        gll = []
        for i in range(len(names)):
            ids = gid.loc[gid[group_name] == names[i]].values[:, 0]
            gll.append(ids.tolist())

        method_args["g"] = "id"
        method_args["gll"] = gll
        if grade_list is not None:
            grade_exp, names_exp = np.meshgrid(grade_list, names)
            grade_exp = grade_exp.flatten().tolist()
            names_exp = names_exp.flatten().tolist()
        else:
            names_exp = names
    else:
        if grade_list is not None:
            grade_exp = grade_list
        else:
            pass

    sta_list = meteva.base.split(sta_all)
    df_list = []
    for sta in sta_list:
        not_all_iv = [True]
        if method.__name__.find("_uv") >= 0 or method.__name__.find("distance") >= 0:
            col_step = 2
            valid_index = [0, 1]
        else:
            col_step = 1
            valid_index = [0]

        len_ = len(sta.columns)
        for nv in range(6 + col_step, len_, col_step):
            not_all_iv1 = np.any(sta.iloc[:, nv].values != meteva.base.IV)
            not_all_iv.append(not_all_iv1)
            if not_all_iv1:
                valid_index.append(nv - 6)
                if col_step == 2: valid_index.append(nv - 5)
        sta = meteva.base.in_member_list(sta, member_list=valid_index, name_or_index="index")
        sta1 = meteva.base.not_IV(sta)
        data_names = meteva.base.get_stadata_names(sta1)
        for m in range(1, len(data_names)):
            sta2 = meteva.base.sele_by_para(sta1, member=[data_names[0], data_names[m]])
            mid_array, _ = meteva.product.score(sta2, method,**method_args)

            index_names = ["time","dtime","model"]
            dict1 = {"time":sta2["time"].values[0],"dtime":  sta2["dtime"].values[0],"model": data_names[m]}
            if names_exp is not None:
                index_names.append(group_name)
                dict1[group_name] = names_exp
            if grade_exp is not None:
                index_names.append("grade")
                dict1["grade"] = grade_exp

            if method == meteva.method.tc_count:
                if grade_list is None:
                    dat1 = mid_array[..., 0]
                else:
                    dat1 = np.repeat([mid_array[..., 0]],len(grade_list))
                dict1[mid_columns[0]] = dat1.flatten()
                dict1[mid_columns[1]] = mid_array[..., 1:].flatten()
            else:
                for c in range(len(mid_columns)):
                    dict1[mid_columns[c]] = mid_array[...,c].flatten()

            #print(dict1)
            hfmc_df = pd.DataFrame(dict1)
            df_list.append(hfmc_df)
    df_all = pd.concat(df_list, axis=0)
    return df_all


def middle_xr(sta_all,method,grade_list = None,compare = None,gid = None):
    '''

    :param sta_all:
    :param method:
    :param grade_list:
    :param compare:
    :param gid:
    :return:
    '''
    mid_columns = get_middle_columns(method)
    df_all = middle_df(sta_all,method,grade_list,compare = compare,gid = gid)
    all_columns = df_all.columns
    index_columns = []
    for name in all_columns:
        if name not in mid_columns:
            index_columns.append(name)
    index =[]
    for i in range(len(index_columns)):
        index.append(df_all[index_columns[i]].values)
    df_new = pd.DataFrame(df_all[mid_columns].values,index = index,columns = mid_columns)
    df_new.index.names = index_columns
    mid_xr = df_new.to_xarray()
    return mid_xr



if __name__ =="__main__":
    path = r"H:\test_data\input\mps\rain24.h5"
    sta_all = pd.read_hdf(path)
    print(sta_all)
    path = r"H:\test_data\input\mps\station_id_province_name.dat"
    id_province = pd.read_csv(path, sep="\\s+", header=None, usecols=[3, 4])
    id_province.columns = ["id", "province"]
    df_all = middle_xr(sta_all,meteva.method.hfmc,grade_list=[0.1,10,25,50,100,250],gid=id_province)
    print(df_all)


