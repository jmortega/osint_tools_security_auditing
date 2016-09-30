import argparse
import re
import sqlite3
import geoip2.database
import folium

reader = geoip2.database.Reader("GeoLite2-City.mmdb")

ip_map       = folium.Map()
ip_addresses = ['8.8.8.8']
print("[*] Locating ip on map!")

for ip_address in ip_addresses:
    print("ip address: "+ip_address)
	
    record  = reader.city(ip_address)
    
    if record.location.latitude:
        
        popup      = folium.Popup(ip_address)
        marker = folium.Marker([record.location.latitude,record.location.longitude],popup=popup)
        
        ip_map.add_child(marker)
 
ip_map.save("map.html")
 
print("[*] Finished creating map!")