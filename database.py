import sqlite3
import csv
#from flask import Flask, render_template, request, redirect, url_for

def initialize_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data (TOTUSJH REAL, TOTBSQ REAL, TOTPOT REAL, TOTUSJZ REAL, ABSNJZH REAL, SAVNCPP REAL, USFLUX REAL, TOTFZ REAL, MEANPOT REAL, EPSZ REAL, MEANSHR REAL, SHRGT45 REAL, MEANGAM REAL, MEANGBT REAL, MEANGBZ REAL, MEANGBH REAL, MEANJZH REAL, TOTFY REAL, MEANJZD REAL, MEANALP REAL, TOTFX REAL, EPSY REAL, EPSX REAL, R_VALUE REAL, CRVAL1 REAL, CRLN_OBS REAL, CRLT_OBS REAL, CRVAL2 REAL, HC_ANGLE REAL, SPEI REAL, LAT_MIN REAL, LON_MIN REAL, LAT_MAX REAL, LON_MAX REAL, DateTime TEXT, IS_TMFI REAL)')
    conn.commit()
    conn.close()

def load_data(filename):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            # Insert data into the table
            c.execute("INSERT INTO data (TOTUSJH, TOTBSQ, TOTPOT, TOTUSJZ, ABSNJZH, SAVNCPP, USFLUX, TOTFZ, MEANPOT, EPSZ, MEANSHR, SHRGT45, MEANGAM, MEANGBT, MEANGBZ, MEANGBH, MEANJZH, TOTFY, MEANJZD, MEANALP, TOTFX, EPSY, EPSX, R_VALUE, CRVAL1, CRLN_OBS, CRLT_OBS, CRVAL2, HC_ANGLE, SPEI, LAT_MIN, LON_MIN, LAT_MAX, LON_MAX, DateTime, IS_TMFI) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33],row[34],row[35]
))
        conn.commit()

    conn.close()

def initialize_database1():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data3 (time_tag TEXT, satellite TEXT, flux REAL, energy REAL)')
    conn.commit()
    conn.close()

def load_data1(filename):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for row in reader:
            # Insert data into the table
            c.execute("INSERT INTO data3 (time_tag, flux, satellite, energy) VALUES (?, ?, ?, ?)",
                      (row[0],row[1],row[2],row[3]
))
        conn.commit()

    conn.close()

initialize_database1()
load_data1('differential-electrons-3-day.csv')

