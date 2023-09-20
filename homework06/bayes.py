import math
import string


class NaiveBayesClassifier:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.dictionary = {}
        self.labels = []
        self.l_chance = []

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        # X: Данные, которые обрабатываем
        # у: Классы, которым принадлежат данные
        X = [clean(x).lower() for x in X]
        self.labels = [label for label in set(y)]
        self.l_chance = [y.count(label) / len(y) for label in self.labels]  # счётчик вероятности класса  (1/3)
        for id, word_list in enumerate(X):
            word_list = word_list.split()  # в потоке названий статей выделяем каждое слово
            for word in word_list:
                if self.dictionary.get(
                    word
                ):  # проверяем если это слово в словаре со всеми данными (слово, количество раз оно встречается)
                    self.dictionary[word][0][self.labels.index(y[id])] += 1  # счетчик определённого слова в классе
                else:
                    self.dictionary.update({word: [[0 for label in self.labels], [0 for label in self.labels]]})
                    # если слова нет в словаре, то добавляется некий счётчик, к кторому потом прибавится 1, если слово
                    # приписали к тому или иному классу
                    self.dictionary[word][0][self.labels.index(y[id])] += 1
        labels = [0 for label in self.labels]
        for id in range(len(labels)):  # счетчик кол-во слов в том или ином классе
            for word in self.dictionary:
                labels[id] += self.dictionary[word][0][id]
        for word in self.dictionary:
            for id in range(len(self.dictionary[word][1])):
                self.dictionary[word][1][id] = (self.alpha + self.dictionary[word][0][id]) / (
                    self.alpha * len(self.dictionary) + labels[id]
                )

    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        # Вычисление класса по входящим данным
        X = [clean(x).lower() for x in X]
        y = []
        for word_list in X:
            chance_of_class = []
            word_list = word_list.split()
            for id in range(len(self.labels)):
                chance_label = math.log(self.l_chance[id])
                for word in word_list:
                    if self.dictionary.get(word):
                        chance_label += math.log(
                            self.dictionary[word][1][id]
                        )  # нат логарифм от количества слова в этом классе (складываем логарифмы)
                chance_of_class.append(chance_label)
            y.append(self.labels[chance_of_class.index(max(chance_of_class))])

        return y

    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        # X_test: Данные, которые проверяем
        # y_test: Классы, которым должны принадлежать Проверяемые Данные
        score = 0
        y = self.predict(X_test)
        for id in range(len(y_test)):
            if y[id] == y_test[id]:
                score += 1
        score /= len(X_test)
        return score


def clean(X):
    translator = str.maketrans("", "", string.punctuation)
    return X.translate(translator)
