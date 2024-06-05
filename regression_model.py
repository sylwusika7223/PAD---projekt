import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

data = pd.read_excel('cleaned_data.xlsx')

if data['m2'].dtype != 'object':
    data['m2'] = data['m2'].astype(str)

data['m2'] = data['m2'].str.replace(',', '.').astype(float)

label_encoders = {}
categorical_columns = ['Street', 'Urban area', 'District', 'Currency', 'Seller type', 'Estate agency']

for col in categorical_columns:
    label_encoders[col] = LabelEncoder()
    data[col] = label_encoders[col].fit_transform(data[col])

X = data.drop(['Price', 'Price per m2'], axis=1)
y = data['Price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=43)

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, 'regression_model.pkl')

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse**0.5)

r2 = r2_score(y_test, y_pred)
print('Coefficient of determination:', r2)

results = pd.DataFrame({'Predicted': y_pred, 'Actual': y_test})
results['Predicted'] = results['Predicted'].round().astype(int)
results.to_excel('predicted_results.xlsx', index=False)
print(results.head())