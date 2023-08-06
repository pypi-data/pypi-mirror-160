import numpy as np
from wwprocess.PlotSchema import Schema

"""
将output目录下的一个试验对应的一个文件夹封装为一个对象
属性包含：
* 风洞试验、模态试验下
  * 各个测点的
    * 加速度和位移
      * 时程数据
      * 均方根、平均值
      * 谱 # TODO
方法包括：
1. 加载数据
2. 计算统计信息
3. 计算谱信息 # TODO
"""

class AET:  # AeroElasticTest

    descMap = {
        'ori': '原始截面',
        'rect': '方形截面',
        'C': 'C类风场',
        'uniform': '均匀风场',
        'rms': '均方根',
        'avg': '均值',
        'accel': '加速度',
        'disp': '位移'
    }

    def __init__(self,
                 shape,  # 形状 ori rect ..
                 windField='',  # 风场
                 angle='',  # 风向角
                 testRound='',  # 模态测试的第几次激励
                 expDir='', # 模态测试所采用的文件夹名
                 testType='wt',  # modal wt
                 noGlued=False,  # 是否粘住缝隙
                 thorough=False,  # 是否加密风速
                 ):
        # 空值
        self.dispMps = []  # 使用的位移测点
        self.accelMps = []  # 使用的加速度测点
        self.accelInAllWindSpeeds = {}  # 所有风向角的加速度数据
        self.dispInAllWindSpeeds = {}  # 所有风向角的位移数据
        self.dispRmsInAllWindSpeeds = {}  # 均方根
        self.accelRmsInAllWindSpeeds = {}  # 均方根
        self.dispAvgInAllWindSpeeds = {}  # 均方根
        self.accelAvgInAllWindSpeeds = {}  # 均方根
        self.accelDataModal = {}  # 模态测试的加速度数据，一层字典，键为测点号，值为时程
        self.dispDataModal = {}  # 模态测试的位移数据，一层字典，键为测点号，值为时程
        # 描述配置
        # 初始化的值
        self.shape = shape
        self.windField = windField
        self.testType = testType
        self.testRound = testRound
        self.expDir = expDir
        if noGlued:
            if thorough:
                self.angle = f'noGlued_thorough_{angle}'
            else:
                self.angle = f'noGlued_{angle}'
        else:
            if thorough:
                self.angle = f'thorough_{angle}'
            else:
                self.angle = angle

        # 是风洞试验是加载平均风速数据
        if testType == 'wt':
            meanFlowData = np.loadtxt(
                f'output/{shape}_windTunnelTest_{windField}_{self.angle}/meanFlow.txt')
            self.meanFlows = meanFlowData  # 平均风速数据
            self.windSpeedSeq = range(1, np.size(meanFlowData) + 1)

    def plotStat(
        self,
        sigType,  # accel disp
        statType,  # rms avg
        alignment,  # 单列或双列排布
        mps=[],  # 使用的测点

    ):
        # 计算数据，分别判断统计类型、传感器信号类型、是否自定义测点
        if statType == 'rms':
            if sigType == 'disp':
                if mps:
                    self.calcRmsInAllWindSpeeds('disp', mps)
                else:
                    self.calcRmsInAllWindSpeeds('disp')
            elif sigType == 'accel':
                if mps:
                    self.calcRmsInAllWindSpeeds('accel', mps)
                else:
                    self.calcRmsInAllWindSpeeds('accel')
        elif statType == 'avg':
            if sigType == 'disp':
                if mps:
                    self.calcAvgInAllWindSpeeds('disp', mps)
                else:
                    self.calcAvgInAllWindSpeeds('disp')
            elif sigType == 'accel':
                if mps:
                    self.calcAvgInAllWindSpeeds('accel', mps)
                else:
                    self.calcAvgInAllWindSpeeds('accel')
        # 绘图
        if alignment == 'single':
            plt = Schema('single')
        elif alignment == 'double':
            plt = Schema('double')
        fig, ax = plt.subplots()

        if sigType == 'disp':
            plotMps = self.dispMps
        elif sigType == 'accel':
            plotMps = self.accelMps

        for mp in plotMps:
            # 按风速变化整合数据
            wsSet = []
            for ws in self.windSpeedSeq:
                if statType == 'rms':
                    if sigType == 'disp':
                        wsSet.append(self.dispRmsInAllWindSpeeds[mp][ws])
                    elif sigType == 'accel':
                        wsSet.append(self.accelRmsInAllWindSpeeds[mp][ws])
                elif statType == 'avg':
                    if sigType == 'disp':
                        wsSet.append(self.dispAvgInAllWindSpeeds[mp][ws])
                    elif sigType == 'accel':
                        wsSet.append(self.accelAvgInAllWindSpeeds[mp][ws])

            ax.plot(self.meanFlows,
                    wsSet,
                    marker='s',
                    label=f'测点{mp}')

        ax.set_title(
            f'{self.descMap[self.shape]}-{self.descMap[self.windField]}{self.angle.replace("thorough_", "")}风向角{self.descMap[sigType]}{self.descMap[statType]}')
        ax.set_xlabel('风速（m/s）')
        if sigType == 'disp':
            ax.set_ylabel(f'位移{self.descMap[statType]}（m）')
        elif sigType == 'accel':
            ax.set_ylabel(f'加速度{self.descMap[statType]}（m/s$^2$）')
        ax.legend()
        return plt, ax

    # 计算所有风速的均方根，二级词典，一级为测点，二级为风速

    def calcRmsInAllWindSpeeds(self,
                               sigType,  # accel disp
                               mps=[],  # 使用的测点
                               ):
        # 加载数据
        if mps:
            self.loadDataInWindSpeeds(sigType, mps)
        else:
            self.loadDataInWindSpeeds(sigType)

        # 计算均方根
        sigTypeMap = {
            'accel': {
                'mps': self.accelMps,
                'dataSet': self.accelInAllWindSpeeds,
            },
            'disp': {
                'mps': self.dispMps,
                'dataSet': self.dispInAllWindSpeeds,
            }
        }
        rmsSet = {}
        for mp in sigTypeMap[sigType]['mps']:  # 对每一个测点算一条数据
            rmsSeq = {}
            for windspeedNum in self.windSpeedSeq:
                rmsSeq[windspeedNum] = (
                    np.std(sigTypeMap[sigType]['dataSet'][windspeedNum][mp]))
            rmsSet[mp] = rmsSeq
        if sigType == 'accel':
            self.accelRmsInAllWindSpeeds = rmsSet
        elif sigType == 'disp':
            self.dispRmsInAllWindSpeeds = rmsSet
        return rmsSet

    def calcAvgInAllWindSpeeds(self,
                               sigType,  # accel disp
                               mps=[],  # 使用的测点
                               ):
        # 加载数据
        if mps:
            self.loadDataInWindSpeeds(sigType, mps)
        else:
            self.loadDataInWindSpeeds(sigType)

        # 计算均方根
        sigTypeMap = {
            'accel': {
                'mps': self.accelMps,
                'dataSet': self.accelInAllWindSpeeds,
            },
            'disp': {
                'mps': self.dispMps,
                'dataSet': self.dispInAllWindSpeeds,
            }
        }
        avgSet = {}
        for mp in sigTypeMap[sigType]['mps']:  # 对每一个测点算一条数据
            avgSeq = {}
            for windspeedNum in self.windSpeedSeq:
                avgSeq[windspeedNum] = (
                    np.mean(sigTypeMap[sigType]['dataSet'][windspeedNum][mp]))
            avgSet[mp] = avgSeq
        if sigType == 'accel':
            self.accelAvgInAllWindSpeeds = avgSet
        elif sigType == 'disp':
            self.dispAvgInAllWindSpeeds = avgSet
        return avgSet

    # 加载全部风速的加速度或位移数据，返回2级字典，第一级为风速，第二季为测点，使用后更新xxxInAllWindSpeeds属性
    # 可传如使用的测点编号
    def loadDataInWindSpeeds(self,
                             sigType,  # accel disp
                             mps=[],  # 使用的测点
                             ):
        dataSet = {}
        if sigType == 'disp':
            for windspeedNum in self.windSpeedSeq:
                # 有传测点就使用传入的，否则使用全部
                if mps:
                    dataSet[windspeedNum] = self.loadDisp(windspeedNum, mps)
                else:
                    dataSet[windspeedNum] = self.loadDisp(windspeedNum)
            self.dispInAllWindSpeeds = dataSet
            return dataSet
        if sigType == 'accel':
            for windspeedNum in self.windSpeedSeq:
                if mps:
                    dataSet[windspeedNum] = self.loadAccel(windspeedNum, mps)
                else:
                    dataSet[windspeedNum] = self.loadAccel(windspeedNum)
            self.accelInAllWindSpeeds = dataSet
            return dataSet

            # 加载1个风速下的位移数据

    # 加载一个风速下指定测点的位移数据，返回字典，键为测点号（从0开始），值为np数组
    def loadDisp(self,
                 windspeed,  # 风速序号
                 mps=[1, 2],  # 使用的测点，从1开始
                 ):
        # 加载2个点的加速度传感器数据
        dataSet = {}
        dispDataMatrix = np.loadtxt(
            f'output/{self.shape}_windTunnelTest_{self.windField}_{self.angle}/timeSeq/disp.all{windspeed}.csv')
        for mp in mps:
            dataSet[mp] = dispDataMatrix[:, mp - 1] / (-100)
        # 添加测点数量属性
        self.dispMps = mps
        return dataSet

    # 加载一个风速下指定测点的加速度数据，返回字典，键为测点号（从0开始），值为np数组
    def loadAccel(self,
                  windspeed,  # 风速序号
                  mps=[1, 2, 3, 4, 5, 6, 7, 8, 9],  # 使用的测点，从1开始
                  ):
        # 加载9个点的加速度传感器数据
        dataSet = {}
        accelDataMatrix = np.loadtxt(
            f'output/{self.shape}_windTunnelTest_{self.windField}_{self.angle}/timeSeq/accel.all{windspeed}.csv')
        for mp in mps:
            if mp in [1, 4, 7]:  # 测点反向
                dataSet[mp] = accelDataMatrix[:, mp - 1] * (-1) * 10 * 9.8
            else:
                dataSet[mp] = accelDataMatrix[:, mp - 1] * 10 * 9.8
        # 添加测点数量属性
        self.accelMps = mps
        return dataSet

    # 加载模态测试数据
    def loadDispModal(self,
                      mps=[1, 2],  # 使用的测点，从1开始
                      ):
        # 加载9个点的加速度传感器数据
        dataSet = {}
        if self.expDir:
            dispDataMatrix = np.loadtxt(
                f'output/{self.expDir}/timeSeq/disp.all{self.testRound}.csv')
        else:
            dispDataMatrix = np.loadtxt(
                f'output/{self.shape}_modalTest/timeSeq/disp.all{self.testRound}.csv')
        for mp in mps:
            dataSet[mp] = dispDataMatrix[:, mp - 1] / (-100)
        # 添加测点数量属性
        self.dispMps = mps
        self.dispDataModal = dataSet
        return dataSet
    # 加载模态测试数据

    def loadAccelModal(self,
                       mps=[1, 2, 3, 4, 5, 6, 7, 8, 9],  # 使用的测点，从1开始
                       ):
        # 加载9个点的加速度传感器数据
        dataSet = {}
        if self.expDir:
            accelDataMatrix = np.loadtxt(
                f'output/{self.expDir}/timeSeq/accel.all{self.testRound}.csv')
        else:
            accelDataMatrix = np.loadtxt(
                f'output/{self.shape}_modalTest/timeSeq/accel.all{self.testRound}.csv')
        for mp in mps:
            if mp in [1, 4, 7]:  # 测点反向
                dataSet[mp] = accelDataMatrix[:, mp - 1] * (-1) * 10 * 9.8
            else:
                dataSet[mp] = accelDataMatrix[:, mp - 1] * 10 * 9.8
        # 添加测点数量属性
        self.accelMps = mps
        self.accelDataModal = dataSet
        return dataSet
