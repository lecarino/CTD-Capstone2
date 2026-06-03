import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

# create  csv file
with open("popular_cities.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["City", "Current Time", "Temperature"])
    print("headers written to csv")

    driver.get("https://www.timeanddate.com/weather/")
    
    # giving the massive table 3 seconds to fully load
    print("waiting 3 seconds for the table to load...")
    time.sleep(3)
    
    #Looking for rows (tr)
    rows = driver.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        #Each row can have 2 or 3 cities. each city having 4 tags (td).
        cols = row.find_elements(By.TAG_NAME, "td")

        #DEBUG
        # print("\n--- LOOKING AT A NEW ROW ---")
        # print(f"Selenium found {len(cols)} columns in this row.")
        
        # for index, col in enumerate(cols):
        #     print(f"   Column {index} holds: '{col.text}'")

        # each column per city goes: Name[0,4,8], Time[1,5,9], Img(not use)[2,6,10], Temp[3,7,11]
        #4 columns each city
        #each row has 2 cities, except for last two rows
        if len(cols) >= 4:
            city1 = cols[0].text
            print(city1)
            time1 = cols[1].text
            print(time1)
            temp1 = cols[3].text
            print(temp1)
            
            #Write if city is present
            if city1 != "":
                writer.writerow([city1, time1, temp1])
                print(f"saved: {city1} | {time1} | {temp1}")
        
        if len(cols) >= 8:
            city2 = cols[4].text
            time2 = cols[5].text
            temp2 = cols[7].text
            
            if city2 != "":
                writer.writerow([city2,time2, temp2])
                print(f"saved: {city2} | {time2} | {temp2}")
        #third city
        if len(cols) >= 8:
            city3 = cols[8].text
            time3 = cols[9].text
            temp3 = cols[11].text
            
            if city3 != "":
                writer.writerow([city3, time3, temp3])
                print(f"saved: {city3} | {time3} | {temp3}")


print("\nclosing browser...")
driver.quit()
print("popular_cities.csv file success.")