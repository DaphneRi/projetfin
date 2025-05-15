import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# lire le fichier csv
data = pd.read_csv('KNN 1.csv')

# converti valeurs pour type de environment en chiffres car un ML model peut pas comprendre les chaines de caractères
label_encoder = LabelEncoder()
data['Environment'] = label_encoder.fit_transform(data['Environment'])

# split les features et les targets, 
X = data[['Temperature', 'Pressure', 'CO2']].values
y = data['Environment'].values

# pour tout scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# split les data en training et testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# crée et entraine le KNN classifier, jai mis 3 voisins 
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

#pour que on puisse entrer les conditions
def get_user_input():
    print("\nEnter the environmental conditions:")
    temperature = float(input("Temperature (°C): "))
    pressure = float(input("Pressure (hPa): "))
    co2 = float(input("CO2 level (ppm): "))
    return np.array([[temperature, pressure, co2]])

def classify_conditions():
    while True:
        try:
            # Get user input
            new_data = get_user_input()
            
            # Scale the new data
            new_data_scaled = scaler.transform(new_data)
            
            # Make prediction
            prediction = knn.predict(new_data_scaled)[0]
            
            # Map prediction to environment type
            environment = label_encoder.inverse_transform([prediction])[0]
            
            print(f"\nClassification Result: {environment}")


if __name__ == "__main__":
    print("Environmental Condition Classifier using KNN")
    print("This classifier uses temperature, pressure, and CO2 levels to determine the environment type.")
    print("Available environment types:", list(label_encoder.classes_))
    classify_conditions() 
