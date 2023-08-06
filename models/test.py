layersss = [3,3,3]


print(sum(layersss[i] * layersss[i+1] for i in range(len(layersss)-1)))