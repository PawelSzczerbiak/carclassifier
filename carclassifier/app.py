from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import pickle
import sqlite3
import os

from vectorizer import vect
from update import update_model

app = Flask(__name__)

cur_dir = os.path.dirname(__file__)

############### CLASSIFICATION ###############

# classifier deserialization
clf = pickle.load(open(os.path.join(cur_dir, 
                 'pkl_objects',
                 'classifier.pkl'), 'rb'))
# database path
db = os.path.join(cur_dir, 'reviews.sqlite')

# model update - based on db content
#clf = update_model(db_path=db, model=clf, batch_size=10000)

# WARNING: save updated model into classifier.pkl permanently
#pickle.dump(clf, open(os.path.join(cur_dir,
#	'pkl_objects', 'classifier.pkl'), 'wb')
#	, protocol=4)

# classification
def classify(opinion):
	label = {0: 'negative', 1: 'positive'}
	X = vect.transform([opinion])
	y = clf.predict(X)[0]
	proba = clf.predict_proba(X).max()
	return label[y], proba

# out-of-core learning
def train(opinion, y):
	X = vect.transform([opinion])
	clf.partial_fit(X, [y])

# insertion into database
def sqlite_entry(path, opinion, y):
	conn = sqlite3.connect(path)
	c = conn.cursor()
	c.execute("INSERT INTO review_db (review, sentiment, date)" \
		" VALUES (?, ?, DATETIME('now'))", (opinion, y))
	conn.commit()
	conn.close()

################## FLASK ####################

class ReviewForm(Form):
	carreview = TextAreaField('', 
                                [validators.DataRequired(), 
                                validators.length(min=2)]) # e.g. 'OK'

@app.route("/")
def index():
	form = ReviewForm(request.form)
	return render_template('reviewform.html', form=form)

@app.route('/results', methods=['POST'])
def results():
	form = ReviewForm(request.form)
	if request.method == 'POST' and form.validate():
		review = request.form['carreview']
		y, proba = classify(review)
		return render_template('results.html',
								content=review,
								prediction=y,
								probability=round(proba*100, 2))
	return render_template('reviewform.html', form=form)

@app.route("/thanks", methods=['POST'])
def feedback():
	# two options ('Incorrect' or 'Correct')
	feedback = request.form['feedback_button']
	review = request.form['review']
	prediction = request.form['prediction']

	inv_label = {'negative': 0, 'positive': 1}
	y = inv_label[prediction]
	if feedback == 'Incorrect':
		y = int(not(y)) # reverse

	train(review, y)
	sqlite_entry(db, review, y)

	return render_template('thanks.html')

if __name__ == '__main__':
	app.run(debug=False)