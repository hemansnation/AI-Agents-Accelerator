import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

def train_model():
    df = pd.read_csv('data/mock_data.csv')
    le_company = LabelEncoder()
    le_industry = LabelEncoder()
    df['company_size'] = le_company.fit_transform(df['company_size'])
    df['industry'] = le_industry.fit_transform(df['industry'])
    
    X = df.drop('converted', axis=1)
    y = df['converted']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)

    joblib.dump(model, 'models/lead_model.joblib')
    joblib.dump(le_company, 'models/le_company.joblib')
    joblib.dump(le_industry, 'models/le_industry.joblib')
    return model.score(X_test, y_test)

def score_lead(lead_data):
    model = joblib.load('models/lead_model.joblib')
    le_company = joblib.load('models/le_company.joblib')
    le_industry = joblib.load('models/le_industry.joblib')
    df = pd.DataFrame([lead_data])
    df['company_size'] = le_company.transform(df['company_size'])
    df['industry'] = le_industry.transform(df['industry'])
    score = model.predict_proba(df)[0][1] * 100
    return score


