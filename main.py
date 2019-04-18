# from gen_algo import gen_algo
from rl import game_run
from neural_network import NN
import pandas as pd

if __name__ == '__main__':
    # cali_dataframe = pd.read_csv("./california_housing_train.csv")
    # x_train = cali_dataframe.drop("median_house_value", 1)
    # y_train = cali_dataframe.median_house_value / 1000

    # def normalize(x):
    #     return (x-min(x))/(max(x)-min(x))

    # for x in x_train:
    #     x_train[x] = normalize(x_train[x])
    #     pass

    # x_val = x_train.tail(500)
    # y_val = y_train.tail(500)

    # model = NN(x_train.shape[1], (4, 5, 1))
    # for l in model.weights:
    #     print(l)

    # model.fit(x_train, y_train, step=10000, epochs=10, batch_size=20, learning_rate=0.005, validation_datas=(x_val, y_val))

    nn = NN(202, (400, 400, 400, 400, 400, 400, 1))
    game_run(nn)
