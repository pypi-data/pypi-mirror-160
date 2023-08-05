import matplotlib.pyplot as plt
import numpy as np

def getPerformancePlot(results):
    fig, ax = plt.subplots()	# 创建画布
    names = []
    data = []

    for i in range(len(results)):
        names.append(results[i]['name']);
        data.append([results[i]['performance'][1], results[i]['performance'][2]])

    ax.set_title('The performance bar chart of Multi OCR Models')	# 设置标题

    X = np.arange(2)
    i = 0
    w = 0.25

    plt.xlabel("Precison-rate and Recall-rate")
    for i in range(len(data)):
        plt.bar(X + i * w, data[i], width=w, label = names[i])
    plt.legend(loc=1)

    plt.show()