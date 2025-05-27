import mysql.connector
import time
import numpy as np
from datetime import datetime

zaehler = 0
resultRanges = []


def DBQuery():
    global mydb
    mydb = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='ESP32',
        password='esp32io.com',
        database='strack'
    )


def checkIfElementInList():
    global resultRanges
    resultRanges.clear()
    while len(resultRanges) < 3:
        mycursor = mydb.cursor()
        mycursor.execute(
            "select fk_Anchor_MAC, r_Range from (SELECT fk_Anchor_MAC,r_Range FROM Ranges order by r_ID DESC Limit 3) as r GROUP by fk_Anchor_MAC HAVING COUNT(*) < 2;")
        resultRanges = mycursor.fetchall()

    if (len(resultRanges) == 3):
        trilateration()


def getValue():
    counter = 0
    while counter < 3:
        for i in resultRanges[counter]:
            for x in myresultAnchor:
                if x[0] == i:
                    getDistance = globals()[f"d{counter}"] = [
                        x[0], resultRanges[counter][1]]
                    getAnchor = globals()[f"a{counter}"] = [x[0], x[1], x[2]]
                    counter += 1


def getLatLongFromAnchor():
    time.sleep(0.5)
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT a_MAC, a_x, a_y FROM Anchor")
    global myresultAnchor
    myresultAnchor = mycursor.fetchall()


def trilateration():
    getLatLongFromAnchor()
    getValue()

    p1 = np.array([a0[1], a0[2], 0.0])
    p2 = np.array([a1[1], a1[2], 0.0])
    p3 = np.array([a2[1], a2[2], 0.0])

    r1 = d0[1]
    r2 = d1[1]
    r3 = d2[1]

    def norm(v):
        return np.sqrt(np.sum(v**2))

    def dot(v1, v2):
        return np.dot(v1, v2)

    def cross(v1, v2):
        return np.cross(v1, v2)

    ex = (p2-p1) / norm(p2-p1)
    i = dot(ex, p3-p1)
    a = (p3-p1) - ex*i
    ey = a / norm(a)
    ez = cross(ex, ey)
    d = norm(p2-p1)
    j = dot(ey, p3-p1)
    x = (r1**2 - r2**2 + d**2) / (2*d)
    y = (r1**2 - r3**2 + i**2 + j**2) / (2*j) - (i/j) * x
    b = r1**2 - x**2 - y**2

    if (np.abs(b) < 0.0000000001):
        b = 0

    z = np.sqrt(abs(b))
    if np.isnan(z):
        raise Exception('NaN met, cannot solve for z')

    a = p1 + ex*x + ey*y

    p4a = a + ez*z

    position = list(p4a)
    insertXY(position)


def insertXY(location):
    mycursor = mydb.cursor()
    current_time = datetime.now()
    sql = "INSERT INTO Location (l_Time, l_x, l_y) VALUES (%s, %s, %s)"
    val = (current_time, float(location[0]), float(location[1]))
    mycursor.execute(sql, val)
    mydb.commit()


def loop():
    while True:
        checkIfElementInList()


DBQuery()
loop()
