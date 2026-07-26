import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from database import get_db_connection
from routing_engine import search_routes

conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT code, name FROM stations")
stations = cursor.fetchall()
conn.close()

print(f"Total stations in DB: {len(stations)}")
st_codes = [s["code"] for s in stations]

date_str = "2026-07-27" # Monday

missing_pairs = []
found_pairs = []

for i, src in enumerate(st_codes):
    for dst in st_codes:
        if src == dst:
            continue
        res = search_routes(src, dst, date_str, min_buffer_mins=15, max_buffer_mins=1440)
        total = res["total_routes_found"]
        if total == 0:
            missing_pairs.append((src, dst))
        else:
            found_pairs.append((src, dst, res['direct_routes_count'], res['connecting_routes_count']))

print(f"\nPairs WITH routes: {len(found_pairs)}")
print(f"Pairs MISSING routes: {len(missing_pairs)}")

print("\nSample missing pairs (No train connections in current seed data):")
for p in missing_pairs[:10]:
    print(f"  {p[0]} -> {p[1]}")
