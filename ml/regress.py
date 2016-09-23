from sklearn.linear_model import Ridge, Lasso, ElasticNet


def regress(attributes, targets, model):
	splits = cv.train_test_split(attributes, targets, test_size=0.2)
	X_train, X_test, y_train, y_test = splits
	model.fit(X_train, y_train)
	y_true = y_test
	y_pred = model.predict(X_test)
	print('Mean squared error = {:0.3f}'.format(mse(y_true, y_pred)))
	print('R2 score = {:0.3f}'.format(r2_score(y_true, y_pred)))


features = concrete[[
	'cement', 'slag', 'ash', 'water', 'splast', 'coarse', 'fine', 'age'
]]
labels = concrete['strength']
regress(features, labels, Ridge())
regress(features, labels, Lasso())
regress(features, labels, ElasticNet())
