import pickle
import sqlite3
import numpy as np
import os

# import HashingVectorizer from local dir
from vectorizer import vect
batch_size = 1000
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir,
                 'pkl_objects',
                 'classifier.pkl'), 'rb'))
db = os.path.join(cur_dir, 'reviews.sqlite')

conn = sqlite3.connect(db)
c = conn.cursor()
c.execute('SELECT * from review_db')

results = c.fetchmany(batch_size)
data = np.array(results)
X = data[:, 0]
y = data[:, 1]

classes = np.array([0, 1])
X_train = vect.transform(X)

print(data)
print
print(X)
print
print(y)
print
print(vect.transform(X))

conn.close()	