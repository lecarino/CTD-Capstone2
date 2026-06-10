import pandas as pd
import sqlite3

#Load file
df = pd.read_csv("popular_cities.csv") 

print("--- BEFORE CLEANING ---")
print(df.head())
print(f"Data types:\n{df.dtypes}\n")

#make copy to clean
clean_df = df.copy()

# Drop duplicates if any
clean_df = clean_df.drop_duplicates()

#Transformation
# REGEX to remove symbols (like °F or °C)  (r'(\d+)')
clean_df['Temperature'] = clean_df['Temperature'].astype(str).str.extract(r'(\d+)').astype(float)

print("--- AFTER CLEANING ---")
print(clean_df.head())
print(f"Data types:\n{clean_df.dtypes}\n")


#DATABASE
try:
    conn = sqlite3.connect("capstone_database.db")
    conn.execute("PRAGMA foreign_keys = 1")
    
    clean_df.to_sql(
        name='weather_data', 
        con=conn,                    
        if_exists='replace',         
        index=False                  
    )
    
    print("successfully made into a db")

except Exception as e:
    print("Error: ",e)

finally:
    if conn:
        conn.close()
        print("Database connection safely closed.")