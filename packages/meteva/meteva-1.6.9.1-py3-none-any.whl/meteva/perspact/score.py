import meteva
import numpy as np
import collections

# 实现任意纬度分类的函数
def score_pd(df, method, s = None,g=None,gll_dict = None,plot = None,**kwargs):
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
    #
    # hfmc_list = [
    #     meteva.method.ts,meteva.method.bias,meteva.method.ets,meteva.method.mr,meteva.method.far,
    #     meteva.method.r,meteva.method.hss_yesorno,meteva.method.pofd,meteva.method.pod,
    #     meteva.method.dts,meteva.method.orss,meteva.method.pc,meteva.method.roc,meteva.method.sr,
    #     meteva.method.hk_yesorno,meteva.method.odds_ratio,meteva.method.ob_fo_hr,meteva.method.ob_fo_hc,
    #     meteva.method.pc_of_sun_rain
    # ]
    #
    # tase_list = [meteva.method.me, meteva.method.mae, meteva.method.mse, meteva.method.rmse]
    # tc_list = [meteva.method.wrong_rate]
    tmmsss_list = [meteva.method.residual_error, meteva.method.residual_error_rate,meteva.method.corr]
    #
    #
    # method_mid = None
    # column_list = None

    # if method in hfmc_list:
    #     column_list = ["H","F","M","C"]
    #     method_mid  = getattr(meteva.method, method_name +"_hfmc")
    # elif method in tase_list:
    #     column_list = ["T", "E", "A", "S"]
    #     method_mid = getattr(meteva.method, method_name + "_tase")
    # elif method in tc_list:
    #     column_list = ["T", "C"]
    #     method_mid = getattr(meteva.method, method_name + "_tc")
    # elif method in tmmsss_list:
    #     column_list = ["T", "MX","MY","SX","SY","SXY"]
    #     method_mid = getattr(meteva.method, method_name + "_tmmsss")
    column_df = df.columns
    if not set(column_list) <= set(column_df):
        print("input pandas.DataFrame must contains columns in list of "+ str(column_list) + " for mem." + method_name + " caculation")
        return None,None

    if s is not None:
        if g is not None:
            if g == "last_range" or g == "last_step":
                s["drop_last"] = False
            else:
                s["drop_last"] = True
    df1 = meteva.base.sele_by_dict(df0, s)

    if g is None:
        g = [g]
        gll_dict = None
        gll0 = None
    else:
        if isinstance(g,str):
            g = [g]

        if gll_dict is None:
            gll_dict = {}
            for gg in range(len(g)):
                gll_dict[g[gg]] = None

        for gg in range(len(g)):
            if g[gg] not in gll_dict.keys() or   gll_dict[g[gg]] is None:
                _,gll = meteva.base.group(df1,g = g[gg])
                gll_dict[g[gg]] = gll
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
                for i in range(1, tmmsss_array.shape[0]):
                    mid_array = meteva.method.tmmsss_merge(mid_array, tmmsss_array[i, :])
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
            score_array,_ = score_pd(df1_list[i], method,g = g_left, gll_dict = gll_dict,plot = None)
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



def score_xr(ds,method,s = None,g = None,gll_dict = None,plot = None,**kwargs):


    hfmc_list = [
        meteva.method.ts,meteva.method.bias,meteva.method.ets,meteva.method.mr,meteva.method.far,
        meteva.method.r,meteva.method.hss_yesorno,meteva.method.pofd,meteva.method.pod,
        meteva.method.dts,meteva.method.orss,meteva.method.pc,meteva.method.roc,meteva.method.sr,
        meteva.method.hk_yesorno,meteva.method.odds_ratio,meteva.method.ob_fo_hr,meteva.method.ob_fo_hc,
        meteva.method.pc_of_sun_rain
    ]

    tase_list = [meteva.method.me, meteva.method.mae, meteva.method.mse, meteva.method.rmse]
    tc_list = [meteva.method.wrong_rate]
    tmmsss_list = [meteva.method.residual_error, meteva.method.residual_error_rate,meteva.method.corr]


    method_mid = None
    column_list = None
    method_name = method.__name__
    if method in hfmc_list:
        column_list = ["H","F","M","C"]
        method_mid  = getattr(meteva.method, method_name +"_hfmc")
    elif method in tase_list:
        column_list = ["T", "E", "A", "S"]
        method_mid = getattr(meteva.method, method_name + "_tase")
    elif method in tc_list:
        column_list = ["T", "C"]
        method_mid = getattr(meteva.method, method_name + "_tc")
    elif method in tmmsss_list:
        column_list = ["T", "MX","MY","SX","SY","SXY"]
        method_mid = getattr(meteva.method, method_name + "_tmmsss")




    pass