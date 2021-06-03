import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif']= ['SimHei']
import urllib.request as req
from mpl_toolkits.basemap import Basemap
from  matplotlib.animation import FuncAnimation
import re
data=open('转化文件.txt','r').readlines()    #提取
for i in range(len(data)):
    data[i]=data[i].split()      #分割
years=[];months=[];days=[];times=[];lons=[];lats=[];KTs=[]
#清洗如下
monthDict={'JAN':'1','FEB':'2','MAR':'3','APR':'4','MAY':'5','JUN':'6','JUL':'7','AUG':'8','SEP':'9','OCT':'10','NOV':'11','DEC':'12'}
for i in range(len(data)):
    year=re.search(r'(19\d\d)|(200\d)',str(data[i]))
    if(year==None):
        continue
    else:
        year=year.group(0)
    if(1949<=int(year)<=2009):
        month=re.search(r'[A-Z]{3}',str(data[i]))
        if(month==None):
            continue
        else:
            month=month.group()
        if(month not in monthDict):
            continue
        else:
            x=data[i].index(month)
            month=monthDict[month]
        try:
            int(data[i][x+1])
        except(ValueError):
            print('ValueError')
            continue
        else:
            day=data[i][x+1]
        if(':' in str(data[i][x+2])):
            time=data[i][x+2]
        else:
            continue
        lat=re.search(r'(-|\d)\d{0,3}\.\d{5}',str(data[i]))
        if(lat==None):
            continue
        else:
            lat=lat.group()
            y=data[i].index(lat)
            if('.' not in data[i][y+1]):
                continue
            else:
                lon=data[i][y+1]
                List=data[i].copy()
                List.reverse()
                while(List!=[]):
                    z=re.search(r'[a-zA-Z-,*?<>:]',str(List[0]))
                    if(z!=None):
                        del(List[0])
                    else:
                        break
                KT=List[0]
                if(KT==None):
                    continue
                else:
                    years.append(year)
                    months.append(month)
                    days.append(day)
                    times.append(time)
                    lons.append(lon)
                    lats.append(lat)
                    KTs.append(KT)
#数据清洗完毕,制作动画
fig= plt.figure(figsize = [12, 6])
ax = plt.subplot(111)
# 创建地图：
map = Basemap(projection='robin', lon_0=0, resolution='c')    #设定了投影方法，球形的地球表面投影到平面地图
# 绘制地图（元素）：
map.drawcoastlines(linewidth=0.25)  #绘制海岸线
map.drawcountries(linewidth=0.25)   #绘制国界线
map.drawmapboundary(fill_color=(0.8, 0.95, 1.0))  #画出地图边界，并填充背景（海洋，陆地在此之上）
map.fillcontinents(color=(1,0.9,0.7),lake_color=(0.8, 0.95, 1.0),zorder=0) #填充大陆（注意zorder=0代表先画，即在底层）

scat = map.scatter(0, 0, s = 0, marker='o', color='r')  # 初始点位置设为原点，大小取0（即不可见）
ax.set_xlabel(u"1949-1990年核爆炸实验（核爆当量：绿色表示小于100KT，蓝色表示100-1000KT，红色表示大于1000KT）", fontsize=16)
ax.set_title('')

pointlimit = 20  # 图中同时最大允许显示的核试验，相当于缓存的可见点数
# 经度、纬度、核爆当量、点大小的缓冲区：
points = np.zeros(4*pointlimit, dtype=float).reshape(pointlimit, 4) 
maxsize = 240   # 点大小的最大值，累加超过后从头开始
sizestep = 30   # 点大小一次增加的值
# 颜色的缓冲区：
colors = [[0,1,0,1],[0,0,1,1], [1,0,0,1]] # 两种颜色，前一种表示核爆当量100及以下，后一种表示核爆当量100到1000,最后的表示1000以上
pointcolors = np.zeros(8*pointlimit, dtype=float).reshape(pointlimit, 2, 4) #edgecolor, facecolor
N=len(years)
# 动画更新函数：
def update(frame):
    recordindex = frame%N   # 计算整体数据集中当前处理行数的下标值，处理完之后从头开始
    pointindex = frame%pointlimit # 计算缓存可见点的下标值，满了后从头开始
    # 所有点的大小均增加一个步长sizeStep
    points[:, 3] = [((size+sizestep)%maxsize if size>0 else 0) for size in points[:, 3]]

    # 将整体数据集中当前处理数据放入缓存（points）
    # 将经纬度投影为地图上的点（map）
    points[pointindex, 0], points[pointindex, 1] = map(lons[recordindex], lats[recordindex])
    points[pointindex, 2] = KTs[recordindex]  # 核爆当量
    points[pointindex, 3] = 20  # 点大小初始化
    if(points[pointindex, 2]< 100):
        pointcolors[pointindex, 0, :] = colors[0]
    elif(points[pointindex, 2]<=1000):
        pointcolors[pointindex, 0, :] = colors[1]
    else:
        pointcolors[pointindex, 0, :] = colors[2]               #edgecolor
    pointcolors[pointindex, 1, :] = pointcolors[pointindex, 0, :]*(1,1,1,0.25) # facecolor    

    # 修改散点图的点大小、位置、颜色：
    scat.set(sizes=points[:, 3], offsets=[(points[i, 0],points[i, 1]) for i in range(pointlimit)])
    scat.set(edgecolor=pointcolors[:, 0, :], facecolor=pointcolors[:, 1, :])

    # 修改标题以显示动态时间（当前核爆炸发生时间）：
    ax.set_title(years[recordindex]+'-'+months[recordindex]+'-'+days[recordindex]+' '+times[recordindex])

ani = FuncAnimation(fig, update, interval=10)  # 更新时间为100个千分之一秒
plt.show()




                            
    
