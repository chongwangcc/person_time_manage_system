#!/usr/bin/python2
# -*- coding: utf-8 -*
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
print(matplotlib.matplotlib_fname())
from matplotlib import pyplot as plt

#colors = ['red','yellowgreen','lightskyblue',"olive","violet","maroon","tomato","yellow"]
colors = ['#F9E701','#EDEE8A','#569ED9',"#075FC3","#11418C","#1C278C","#657B6C","#335159"]

def paintThisWeekTypePie(image_path,sum_list):
    """
    绘制 本周类别 饼状图
    :param sum_list:
    :param type_list:
    :return:
    """
    #生成label,size
    labels=[]
    sizes=[]

    for row in sum_list[1:][:-1]:
        labels.append(row[0])
        sizes.append(row[-1].total_seconds())
    #调节图形大小，宽，高
    plt.figure(figsize=(6,6))
    patches,l_text,p_text = plt.pie(sizes,
                                labels=labels,colors=colors,
                                labeldistance = 1.1,
                                autopct = '%3.1f%%',
                                shadow = False,
                                startangle = 90,
                                pctdistance = 0.6)
    for t in l_text:
        t.set_size=(30)
    for t in p_text:
        t.set_size=(20)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend()
    plt.title("本周时间类别饼状图")
    plt.savefig(image_path)
    #plt.show()
    plt.close('all')

def paintTimeSumBar(image_path,sum_list,tag):
    """
        绘制 本周 tag 时间柱状图
        :param image_path:
        :param sum_list:
        :return:
        """
    data = []
    labels = sum_list[0][1:][:-1]
    index = 0;
    for row in sum_list[1:][:-1]:
        index += 1
        if row[0] == tag:
            for delta in row[1:][:-1]:
                data.append(delta.total_seconds() / (60 * 60))
                # print(data[-1])
            break
    #print(tag,colors[(index - 1)%len(colors)])
    plt.bar(range(len(data)), data, tick_label=labels, color=colors[(index - 1)%len(colors)])
    for a, b in zip(range(0, len(labels)), data):
        plt.text(a, b + 0.05, '%.1f' % b, ha='center', va='bottom')
    plt.xlabel("日期")
    plt.ylabel("小时")
    plt.title("本周 每天 "+tag+" 时间")
    plt.savefig(image_path)
    plt.close('all')
