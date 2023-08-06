import logging
import os
from typing import Any, Dict, List, Tuple, Union


def predict(
    user_model: Any,
    request: Union[prediction_pb2.SeldonMessage, List, Dict, bytes],
    seldon_metrics: SeldonMetrics,
) -> Union[prediction_pb2.SeldonMessage, List, Dict, bytes]:
    pass



'''
非会话模式计算接口,对应oneShot请求,可能存在并发调用

@param usrTag 句柄
#param params 功能参数
@param  reqData     写入数据实体
@param  respData    返回结果实体,内存由底层服务层申请维护,通过execFree()接口释放
@param psrIds 需要使用的个性化资源标识列表
@param psrCnt 需要使用的个性化资源个数

@return 接口错误码
    reqDat
    ret:错误码。无错误码时返回0
'''
def wrapperOnceExec(userWrapper: Any, params:{},reqData:[],respData:[],psrIds:[],psrCnt:int) -> int:
    print("hello world")
    print(usrTag)
    print(params)
    print(reqData)
    print(psrIds)
    print(psrCnt)
    return 100
