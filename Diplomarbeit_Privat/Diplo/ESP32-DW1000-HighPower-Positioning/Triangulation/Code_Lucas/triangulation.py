from multiprocessing import connection
import mysql.connector
import time
import math
import numpy
from numpy import sqrt
from datetime import datetime



listeDerJsonObjekte = []

zaehler = 0
counter = 2
#mögliche Lösung --> listeDerJsonObjekte mit den 3 AchorsID; wenn Anchor in listeDerJsonObjekte vorhanden - distance wird überschrieben ansonsten wird anchor in listeDerJsonObjekte aufgenommen
#-->wartet bis 3 Anchors in der listeDerJsonObjekte vermerkt wurden

def DBQuery():
    mydb = mysql.connector.connect(
    host="localhost",
    user="ESP32",
    password="esp32io.com",
    database="strack"
    )
    
    while True:
        getLatLongFromAnchor = mydb.cursor()
        getLatLongFromAnchor.execute("Select a_Lat, a_Lon from anchor")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT fk_Anchor_MAC,r_Range FROM ranges order by r_ID DESC Limit 1;")
        myresult = mycursor.fetchall()
        for x in myresult:
            checkIfElementInList(x)
            time.sleep(1)
        
        break
    mydb.close()




def checkIfElementInList(outputFromList):

        if not listeDerJsonObjekte:
            listeDerJsonObjekte.append({outputFromList[0]:outputFromList[1]})
            print("Daten wurde hinzugefügt")

            return

        else:
            zaehler = 0
            while zaehler < len(listeDerJsonObjekte):
                for espID in listeDerJsonObjekte[zaehler]:
                    if espID == outputFromList[0]:
                        del listeDerJsonObjekte[zaehler]
                        listeDerJsonObjekte.insert(zaehler,{outputFromList[0]:outputFromList[1]})
                        print("UPDATE")
                        print(listeDerJsonObjekte)
                        if len(listeDerJsonObjekte) == 3:
                            triangulation()
                        else:
                            return #springt aus der funktion heraus

                    else:
                        zaehler = zaehler + 1
                        break #sprint aus der for loop heraus

        if len(listeDerJsonObjekte)<3:  
            listeDerJsonObjekte.append({outputFromList[0]:outputFromList[1]})
            return
        else:
            triangulation()
        
def getValue():
    for i in listeDerJsonObjekte:
        if '6017' in i:
            global AnchorA 
            AnchorA = i['6017']

        elif '6020' in i:
            global AnchorB
            AnchorB = i['6020']

        elif '6019' in i:
            global AnchorC
            AnchorC = i['6019']

        else:
            print("Es konnte keinen Wert gefunden werden")

            
        


def triangulation():
    getValue()
    

    #print(res['6020'])
    #assuming elevation = 0

    earthR = 6371
    LatA = 47.189
    LonA = 9.71631
    DistA = AnchorA
    LatB = 47.1886
    LonB = 9.71638
    DistB = AnchorB
    LatC = 47.1888
    LonC = 9.71601
    DistC = AnchorC

    #using authalic sphere
    #if using an ellipsoid this step is slightly different
    #Convert geodetic Lat/Long to ECEF xyz
    #   1. Convert Lat/Long to radians
    #   2. Convert Lat/Long(radians) to ECEF
    xA = earthR *(math.cos(math.radians(LatA)) * math.cos(math.radians(LonA)))
    yA = earthR *(math.cos(math.radians(LatA)) * math.sin(math.radians(LonA)))
    zA = earthR *(math.sin(math.radians(LatA)))

    xB = earthR *(math.cos(math.radians(LatB)) * math.cos(math.radians(LonB)))
    yB = earthR *(math.cos(math.radians(LatB)) * math.sin(math.radians(LonB)))
    zB = earthR *(math.sin(math.radians(LatB)))

    xC = earthR *(math.cos(math.radians(LatC)) * math.cos(math.radians(LonC)))
    yC = earthR *(math.cos(math.radians(LatC)) * math.sin(math.radians(LonC)))
    zC = earthR *(math.sin(math.radians(LatC)))

    P1 = numpy.array([xA, yA, zA])
    P2 = numpy.array([xB, yB, zB])
    P3 = numpy.array([xC, yC, zC])

    #from wikipedia
    #transform to get circle 1 at origin
    #transform to get circle 2 on x axis
    ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
    i = numpy.dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
    ez = numpy.cross(ex,ey)
    d = numpy.linalg.norm(P2 - P1)
    j = numpy.dot(ey, P3 - P1)

    #from wikipedia
    #plug and chug using above values
    x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
    y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

    # only one case shown here
    z = pow(DistA,2) - pow(x,2) - pow(y,2)
    test = sqrt(abs(z))

    #triPt is an array with ECEF x,y,z of trilateration point
    triPt = P1 + x*ex + y*ey + test*ez

    #convert back to lat/long from ECEF
    #convert to degrees
    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1],triPt[0]))

    print (lat, lon)
    # datetime object containing current date and time
    now = datetime.now()
    print(now)
        
    for i in listeDerJsonObjekte:
        global counter
        while counter >= 0:
            
            listeDerJsonObjekte.remove(listeDerJsonObjekte[counter])
            counter = counter-1
    print("AKTION FERTIG")
    counter = 2
    return


def loop():
    while True:
        DBQuery()

loop()