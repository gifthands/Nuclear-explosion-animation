from matplotlib.pyplot import *;from numpy import *
import re;from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap;from pylab import mpl
mpl.rcParams['font.sans-serif']= ['SimHei']
data=open('转化文件.txt','r').readlines()    #提取
for i in range(len(data)):
    data[i]=data[i].split()      #分割
    #下方为正则表达式索引
years=[];months=[];times=[];lons=[];lats=[];KTs=[]
for i in range(len(data)):
    year=re.search(r'\d\d\d\d',str(data[i]))
    if(year==None):
        continue
    else:
        year=year.group(0)
    if(1949<=int(year)<=1990):
        month=re.search(r'[A-Z]{3}',str(data[i]))
        if(month==None):
            continue
        else:
            month=month.group(0)
            time=re.search(r'\d\d:\d\d',str(data[i]))
            if(time==None):
                continue
            else:
                time=time.group(0)
                lon=re.search(r'[-|\d]\d{1,4}.\d{5}',str(data[i]))
                if(lon==None):
                    continue
                else:
                    lon=lon.group(0)
                    lat=re.search(r'[-|\d]\d{0,4}.\d{5}',str(data[i]))
                    if(lat==None):
                        continue
                    else:
                        lat=lat.group(0)
                        data[i]=data[i].reverse
                        KT=re.search(r'\d{1,4}.\d{1,6}',str(data[i]))
                        if(KT==None):
                            continue
                        else:
                            KT=KT.group(0)
                            years.append(year)
                            months.append(month)
                            times.append(time)
                            lons.append(lon)
                            lats.append(lat)
                            KTs.append(KT)
##数据清洗完毕,制作动画
#fig= plt.figure(figsize = [12, 6])
#ax = plt.subplot(111)
## 创建地图：
#map = Basemap(projection='robin', lon_0=0, resolution='c')    #设定了投影方法，球形的地球表面投影到平面地图
## 绘制地图（元素）：
#map.drawcoastlines(linewidth=0.25)  #绘制海岸线
#map.drawcountries(linewidth=0.25)   #绘制国界线
#map.drawmapboundary(fill_color=(0.8, 0.95, 1.0))  #画出地图边界，并填充背景（海洋，陆地在此之上）
#map.fillcontinents(color=(1,0.9,0.7),lake_color=(0.8, 0.95, 1.0),zorder=0) #填充大陆（注意zorder=0代表先画，即在底层）
#scat=map.scatter(0,0,s=0,marker='o',color='r')
#ax.set_xlabel(u'全球核爆实验（红色当量大于800）',fontsize=16)
#ax.set_title('')
#pointlimit=20
#points = np.zeros(4*pointlimit, dtype=float).reshape(pointlimit, 4) 
#maxsize = 300   # 点大小的最大值，累加超过后从头开始
#sizestep = 30   # 点大小一次增加的值
## 颜色的缓冲区：
#colors = [[0,0,1,1], [1,0,0,1]] # 两种颜色，前一种表示800及以下，后一种表示800以上
#pointcolors = np.zeros(8*pointlimit, dtype=float).reshape(pointlimit, 2, 4) #edgecolor, facecolor
#N=len(years)-1
## 动画更新函数：
#def update(frame):
#    recordindex = frame%N   # 计算整体数据集中当前处理行数的下标值，处理完之后从头开始
#    pointindex = frame%pointlimit # 计算缓存可见点的下标值，满了后从头开始
#    # 所有点的大小均增加一个步长sizeStep
#    points[:, 3] = [((size+sizestep)%maxsize if size>0 else 0) for size in points[:, 3]]
#
#    # 将整体数据集中当前处理数据放入缓存（points）
#    # 将经纬度投影为地图上的点（map）
#    points[pointindex, 0], points[pointindex, 1] = map(lons[recordindex], lats[recordindex])
#    points[pointindex, 2] = KTs[recordindex]  # 核爆当量
#    points[pointindex, 3] = 20  # 点大小初始化
#    pointcolors[pointindex, 0, :] = (colors[0] if points[pointindex, 2] < 5.5 else colors[1]) # edgecolor
#    pointcolors[pointindex, 1, :] = pointcolors[pointindex, 0, :]*(1,1,1,0.25) # facecolor    
#
#    # 修改散点图的点大小、位置、颜色：
#    scat.set(sizes=points[:, 3], offsets=zip(points[:, 0],points[:, 1]))
#    scat.set(edgecolor=pointcolors[:, 0, :], facecolor=pointcolors[:, 1, :])   # 修改标题以显示动态时间（当前地震发生时间）：
#    ax.set_title(years[recordindex]+''+months[recordindex]+''+times[recordindex])
#animation = FuncAnimation(fig, update, interval=100)  # 更新频率单位是千分之一秒    
#plt.show()




                            
    
