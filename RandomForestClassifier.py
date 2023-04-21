import pandas as pd
from sklearn.ensemble import RandomForestClassifier  
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,RobustScaler,MinMaxScaler
import pickle

# Load csv file
df = pd.read_csv("preprocessed_data.csv")


# Selecting independent and dependent variables
# Gender,Married,Dependents,Education,Self_Employed,ApplicantIncome,CoapplicantIncome,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,Loan_Status,LoanAmountOverIncome,Total_Income

X = df[["Gender","Married","Dependents","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Credit_History","Property_Area"]]
Y = df["Loan_Status"]

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=50)

# Feature scaling
sc = RobustScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

#Instantiate the model

classifier = RandomForestClassifier()

# Fit the model
classifier.fit(X_train,Y_train)

# Make pickle object of our model

pickle.dump(classifier,open("model.pkl","wb"))





