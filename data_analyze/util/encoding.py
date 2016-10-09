import pandas as pd
from sklearn.preprocessing import LabelEncoder

#Auto encodes any dataframe column of type category or object.
def dummyEncode(df):
        columnsToEncode = list(df.select_dtypes(include=['category','object']))
        le = LabelEncoder()
        for feature in columnsToEncode:
            try:
                df[feature] = le.fit_transform(df[feature])
            except:
                print('Error encoding '+feature)
        return df

orgin = list('abbcddee')
data = pd.DataFrame(orgin, columns=["origin"])
print "\noriginal data:"
print data


dummy = data.copy()
print "\ndummy result:"
print dummyEncode(dummy)

# one-hot
ser = pd.Series(orgin)
print "\n onehot input:"
print ser


onehot = pd.get_dummies(ser);
print "\nonehot result:"
print onehot

#print pd.merge(data, onehot,left_index=True,right_index=True,how='outer')
print "\n merge result:"
print data.join(onehot)