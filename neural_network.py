import numpy as np


class NN:
    def __init__(self, input_shape, units):
        """
        units: (10, 11, 12)
            => 3 couches avec 10 neurones pour la premiere
        """
        nb_output = input_shape
        self.weights = []
        for nb_neurones in units:
            self.weights.append(np.random.rand(nb_output, nb_neurones))
            self.weights.append(np.zeros(nb_neurones))
            nb_output = nb_neurones
        for w in self.weights:
            print(w)

    def preactiv(self, x):
        res = x
        # print(x.dtype)
        # print(self.weights[0].dtype)
        for i in range(0, len(self.weights), 2):
            res = self.activ(res @ self.weights[i] + self.weights[i + 1])

        return res

    def activ(self, res):
        res[res < 0] = 0
        return res

    def predict(self, x):
        return self.activ(self.preactiv(x))

    def predict_on_dataset(self, x):
        res = np.zeros(len(x))
        for i in range(len(x)):
            res[i] = self.predict(x.iloc[i])
        return res

    def loss(self, res, y):  # 1 example
        return res - y

    def d_activation(self, res):
        if res > 0:
            return 1
        else:
            return 0

    def cost(self, x, y):  # dataset
        total_cost = 0

        for i in range(len(x)):
            features = x.iloc(i)
            target = y.iloc(i)
            total_cost += (target - self.predict(features)) ** 2

        return total_cost

    def fit_on_one(self, x, y, learning_rate):
        # store the gradient calculated on the whole batch
        gradient = []
        for k in range(0, len(self.weights), 2):
            gradient.append(np.zeros(self.weights[k].shape))
            gradient.append(np.zeros(self.weights[k + 1].shape))

        res_l = [x]  # store the result after each layer
        res = x

        # calculate the result for the current features
        for h in range(0, len(self.weights), 2):
            pre_a = res @ self.weights[h] + self.weights[h + 1]
            # store the intermediate result before activation
            res_l.append(pre_a)
            res = self.activ(pre_a)

        loss = self.loss(res, y)
        # print(y, " / ", res)

        # update of the last neurone
        act_deriv = 1  # self.activation_deriv(post_a)
        gradient[-2] += loss * act_deriv * np.expand_dims(res_l[-2], 1)
        gradient[-1] += loss * act_deriv
        h = 0
        for h in range(0, len(self.weights), -2):  # backpropagation
            print("testetst")
            loss = self.activ(res_l[h / 2]) * np.dot(self.weights[h + 2], loss)
            gradient[h] = res_l[h / 2] * loss
            gradient[h + 1] = res_l[h / 2]
            print(gradient[h])
            print(gradient[h + 1])

        for k in range(0, len(self.weights), 2):
            # print(gradient[k])
            self.weights[k] -= learning_rate * gradient[k]
            self.weights[k + 1] -= learning_rate * gradient[k + 1]

    def fit(self, x, y, step, epochs, batch_size, learning_rate, validation_datas):
        x_val = validation_datas[0]
        y_val = validation_datas[1]
        x = x
        y = y
        i = 0
        epo = 0

        default_batch_gradient = []
        for k in range(0, len(self.weights), 2):
            default_batch_gradient.append(np.zeros(self.weights[k].shape))
            default_batch_gradient.append(np.zeros(self.weights[k + 1].shape))

        for etape in range(step):
            i += 1
            bx = x.iloc[batch_size * i : batch_size * (i + 1) - 1]
            by = y.iloc[batch_size * i : batch_size * (i + 1) - 1]

            # store the gradient calculated on the whole batch
            batch_gradient = default_batch_gradient

            for k in range(len(bx)):  # iterate over the batch
                res_l = [bx.iloc[k]]  # store the result after each layer
                res = bx.iloc[k]

                # calculate the result for the current features
                for h in range(0, len(self.weights), 2):
                    pre_a = res @ self.weights[h] + self.weights[h + 1]
                    # store the intermediate result before activation
                    res_l.append(pre_a)
                    res = self.activ(pre_a)

                loss = self.loss(by.iloc[k], res)

                # update of the last neurone
                act_deriv = 1  # self.activation_deriv(post_a)
                batch_gradient[-2] += loss * act_deriv * np.expand_dims(res_l[-2], 1)
                batch_gradient[-1] += loss * act_deriv

                for h in range(len(self.weights), 0, -2):  # backpropagation
                    print([x for x in range(len(self.weights), 0, -2)])
                    loss = self.activ(res_l[h // 2]) * np.dot(self.weights[h + 2], loss)
                    batch_gradient[h] = res_l[h // 2] * loss
                    batch_gradient[h + 1] = res_l[h // 2]

            for k in range(0, len(self.weights), 2):
                a = learning_rate * (1 / batch_size)
                self.weights[k] -= a * batch_gradient[k]
                self.weights[k + 1] -= a * batch_gradient[k + 1]

            if x.shape[0] < batch_size * (i + 1):
                p = np.random.permutation(len(x))
                x = x.iloc[p]
                y = y.iloc[p]
                i = 0

            if etape != 0 and etape % (step / epochs) == 0:
                print("=====================")
                predic = self.predict_on_dataset(x_val)
                predic_train = self.predict_on_dataset(x)
                print(
                    "Epoch: ",
                    epo,
                    "| loss val: ",
                    ((predic - y_val) ** 2).mean() / 2,
                    " | loss train ",
                    ((predic_train - y) ** 2).mean() / 2,
                )
                epo += 1


"""
dataset = pd.read_csv("./winequality-red.csv")

train = dataset
#validation = dataset.tail(199)

x_train = train.drop('quality', 1)
y_train = train.quality

# train_sata = pd.read_csv("./train.csv")
# x_train = train_sata.drop('target', 1)
# y_train = train_sata.target

cali_dataframe = pd.read_csv("./california_housing_train.csv")
x_train = cali_dataframe.drop("median_house_value", 1)
y_train = cali_dataframe.median_house_value / 1000

def normalize(x):
    return (x-min(x))/(max(x)-min(x))

for x in x_train:
    x_train[x] = normalize(x_train[x])
    pass


x_val = x_train.tail(500)
y_val = y_train.tail(500)

model = NN(x_train.shape[1], (4, 5, 1))
#print(model.predict(x_train.iloc[0]))
for l in model.weights:
    print(l)

model.fit(x_train, y_train, step=10000, epochs=10, batch_size=20, learning_rate=0.005, validation_datas=(x_val, y_val))
"""
