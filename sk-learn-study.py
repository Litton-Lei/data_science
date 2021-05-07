from sklearn import datasets
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

boston = datasets.load_wine()
boston_x = boston.data
boston_y = boston.target

xtrain,xtest,ytrain,ytest=train_test_split(boston_x,boston_y,test_size=0.3)


x,y=datasets.make_regression(n_samples=100,n_features=1,n_targets=1,noise=10)
print(x,y)
plt.scatter(x,y)
plt.show()