
class XDict:
    """对标准Dict的扩展"""

    def __init__(self, dct):
        """
        * dct: {Dict} ---- 封装dict
        """
        self.data = dct 

    @staticmethod
    def fromArray(arr, *keyFuncs):
        """从数组arr中，按照keyFuncs计算的关键字列表来 构建Dict
        * arr: {List} ---- 数组
        * keyFuncs: {(T)=>B} ---- 构建关键字
        """

        res = {}    # 结果Dict
        level = len(keyFuncs)   # 关键字层级
        for ele in arr:
            dct = res   # 临时变量，用于迭代本次元素时递进关键字
            for i in range(level):  # 遍历每一层关键字
                func = keyFuncs[i]
                key = func(ele) # 获取关键字
                if i == level-1:    # 最后一层
                    dct[key] = ele  # 追加或者更新叶子信息
                else:
                    if not key in dct:    # 第一次引用该关键字，创建Dict变量
                        dct[key] = {}
                    dct = dct[key]  # 递进到下一个关键字层次

        return res
