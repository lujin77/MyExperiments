from sklearn.preprocessing import scale
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier


def classify(attributes, targets, model):
	# Split data into 'test' and 'train' for cross validation
	splits = cv.train_test_split(attributes, targets, test_size=0.2)
	X_train, X_test, y_train, y_test = splits
	model.fit(X_train, y_train)
	y_true = y_test
	y_pred = model.predict(X_test)
	print(confusion_matrix(y_true, y_pred))


# Divide data frame into features and labels
features = occupancy[['temp', 'humid', 'light', 'co2', 'hratio']]
labels = occupancy['occupied']
# Scale the features
stdfeatures = scale(features)
classify(stdfeatures, labels, LinearSVC())
classify(stdfeatures, labels, KNeighborsClassifier())
