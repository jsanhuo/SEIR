from pylab import *
import matplotlib.pyplot as plt
mpl.rcParams['font.sans-serif'] = ['FangSong']
def seir_model_simulate():
    N = 10000
    I = [1] #infectious
    S = [N-1]; #susceptible
    R = [0]; #recovered
    E = [0]; #exposeds

    r = 2; #接触数
    beta = 0.03; #被感染者传染
    beta_1 = 0.03; #被潜伏着传染
    alpha = 0.1; #潜伏期10天
    gamma = 0.5; #康复概率

    T = range(1,150)
    for i in range(len(T) - 1):

        S.append(S[i] - r * (beta * I[i] + beta_1 * E[i]) * S[i] / N)
        E.append(E[i] + r * (beta * I[i] + beta_1 * E[i]) * S[i] / N - alpha * E[i])
        I.append(I[i] + alpha * E[i] - gamma * I[i])
        R.append(R[i] + gamma * I[i])

    plot1, = plt.plot(T, S, 'r')
    plot2, = plt.plot(T, I, 'b')
    plot3, = plt.plot(T, E, 'y')
    plot4, = plt.plot(T, R, 'g')

    plt.xlabel('天');
    plt.ylabel('人数')
    plt.legend([plot1, plot2,plot3,plot4], ['易感者','潜伏者','感染者','治愈者'])

    plt.show()
if __name__ == '__main__':
    seir_model_simulate()