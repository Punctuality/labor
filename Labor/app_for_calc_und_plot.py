import pandas as pd
import matplotlib.pyplot as plt

filein = input('Input file (.csv) path: ')

Df = pd.DataFrame.from_csv(filein)

X = Df['Rpm']
y = Df['Piguins']

a = 1.3
p = 1.225
d = 0.6
Pig_kg = 0.4536
X_s = [i/60 for i in X]

y_predicted = [a*p*(i**2)*(d**4) for i in X_s]

l1l2 = 0.968
g = 1

y_true = [g*l1l2*Pig_kg*i for i in y]

print('_'*18)

print('|Rpm  | True_Kg')
for i in range(len(X)):
    out = str(X[i])+' | '+str(y_true[i])
    if out.index('|') == 4:
        out=out[:4]+' '+out[4:]
    print('|'+out)

print('_'*18+'\n')

print('|Rpm  | Pred_Kg')
for i in range(len(X)):
    out = str(X[i])+' | '+str(y_predicted[i])
    if out.index('|') == 4:
        out=out[:4]+' '+out[4:]
    print('|'+out)

print('_'*18)
    
plt.plot(X, y_predicted, c='green')
plt.scatter(X, y_predicted, c='green', marker='X')
plt.plot(X, y_true, c ='red')
plt.scatter(X, y_true, c ='red', marker='X')
plt.show()