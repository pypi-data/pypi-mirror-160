import matplotlib.pyplot as plt
import numpy as np

def getTimePlot(results):
    fig, ax = plt.subplots()	# 创建画布

    # 设置标题
    ax.set_title('The running time chart of Multi OCR Models')
    
    names = []
    data = []

    for i in range(len(results)):
        names.append(results[i]['name']);
        data.append([results[i]['performance'][0]])

    X = np.arange(1)
    i = 0
    w = 0.25

    plt.xlabel("running time")
    for i in range(len(data)):
        plt.bar(X + i * w, data[i], width=w, label = names[i])
    plt.legend(loc=1)

    plt.show()