##DB and Collections names
MongoDB name: world_data
Collections name: airports, volcanos, meteorites, earthquakes, countries, states, cities

##How to Run the Script
First of all, open the batch file and make sure the file pathing is correct for all of the files (C:\Users\Ben\Desktop\GEO\geo\geojson\airports.geojson). Open your command prompt and change directory until you get into your mongoDB directory. Then type ./load_mongo.sh 

##Example Queries
Query1: (33.9137, 98.4934) (34.7465, 92.2896) 500
Query2: volcanos Altitude 500 max 100 1000
Query3: volcanos 5 10
