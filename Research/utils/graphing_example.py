import matplotlib.pyplot as plt

one = [[0, 30], [35, 45], [54,100]]
two = [[10,40], [44, 90]]
three = [[3, 12], [18, 30], [35, 49], [57,100]]
big = [2, 99]
syn = [[10,12], [18,30], [35,40], [44,45], [57,90]]
selected = [73,78]
coins = [one, two, three]
for i in range(len(coins)):
    for j in range(len(coins[i])):
        plt.plot(coins[i][j], [5 - i, 5-i], 'b')
plt.plot(big, [6,6], 'c')
for i in range(len(syn)):
    plt.plot(syn[i], [2,2], 'm')
plt.plot(selected, [1,1], 'r')
plt.show()