import matplotlib.pyplot as plt

    #DATA EXTRACTION

def traiter_ligne(ligne):

    #clean the line

    ligne = ligne.strip().rstrip(";")
    valeurs = [v.strip() for v in ligne.split(',')]

    #get the values
    temps = pression = temperature = altitude = None
    for valeur in valeurs:
        if 's' in valeur:
            temps = float(''.join(c for c in valeur if c.isdigit() or c == '.' or c == '-'))
        elif 'hPa' in valeur:
            pression = float(''.join(c for c in valeur if c.isdigit() or c == '.' or c == '-'))
        elif '°C' in valeur:
            temperature = float(''.join(c for c in valeur if c.isdigit() or c == '.' or c == '-'))
        elif 'm' in valeur:
            altitude = float(''.join(c for c in valeur if c.isdigit() or c == '.' or c == '-'))

    return [temps, pression, temperature, altitude]


#write the NAME of the file here !

fichier_nom = "data"


#analysis

resultat = []
with open(fichier_nom, 'r', encoding='utf-8') as fichier:
    for ligne in fichier:
        if "(sol)" in ligne:
            continue
        resultat.append(traiter_ligne(ligne))
resultat.remove(resultat[len(resultat)-1])
resultat.remove(resultat[0])

#display of the results

pressures = [pressure[1] for pressure in resultat]
temperatures = [temperature[2] for temperature in resultat]
altitudes = [alt[3] for alt in resultat]
time = [time[0] for time in resultat]


#for ligne_traitee in resultat:
#    print(ligne_traitee)

#print()

max_temperature = max(temperatures)
max_pressure = max(pressures)
max_altitude = max(altitudes)

min_temperature = min(temperatures)
min_pressure = min(pressures)
min_altitude = min(altitudes)

print("Max :")
print("- Temperature : "+str(max_temperature)+"°C")
print("- Pressure : "+str(max_pressure)+"hPa")
print("- Altitude : "+str(max_altitude)+"m")

print("Min :")
print("- Temperature : "+str(min_temperature)+"°C")
print("- Pressure : "+str(min_pressure)+"hPa")
print("- Altitude : "+str(min_altitude)+"m")


    #GRAPHICAL ANALYSIS OF THE DATA

#data

x = [t for t in time]
y1 = [p for p in pressures]
y2 = [temp for temp in temperatures]
y3 = [alt for alt in altitudes]


#graphical representation

#Pressure

plt.figure(figsize=(10, 6))

plt.plot(x, y1, label='Pressure', color='purple')

plt.title("Pressure curve")
plt.xlabel("Time (s)")
plt.ylabel("Pressure (hPa)")
plt.xticks(rotation=45)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#Temperature

plt.figure(figsize=(10, 6))

plt.plot(x, y2, label='Temperature', color='green')

plt.title("Temperature curve")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


#Altitude

plt.figure(figsize=(10, 6))

plt.plot(x, y3, label='Altitude', color='red')

plt.title("Altitude curve")
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.xticks(rotation=45)

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
