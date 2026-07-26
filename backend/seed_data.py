import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(__file__))
from database import init_db, get_db_connection

def seed_railway_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM schedules")
    cursor.execute("DELETE FROM trains")
    cursor.execute("DELETE FROM stations")

    # 1. Insert Stations (16 Major Railway Hubs & Junctions)
    stations = [
        ("NDLS", "New Delhi", "Delhi", 28.6427, 77.2195, 1),
        ("MMCT", "Mumbai Central", "Mumbai", 18.9696, 72.8193, 1),
        ("HWH", "Howrah Junction", "Kolkata", 22.5851, 88.3415, 1),
        ("MAS", "Chennai Central", "Chennai", 13.0827, 80.2707, 1),
        ("SBC", "KSR Bengaluru", "Bengaluru", 12.9781, 77.5697, 1),
        ("BPL", "Bhopal Junction", "Bhopal", 23.2599, 77.4126, 1),
        ("NGP", "Nagpur Junction", "Nagpur", 21.1458, 79.0882, 1),
        ("CNB", "Kanpur Central", "Kanpur", 26.4542, 80.3500, 1),
        ("VGLJ", "VGR Jhansi Junction", "Jhansi", 25.4484, 78.5685, 1),
        ("BRC", "Vadodara Junction", "Vadodara", 22.3107, 73.1812, 1),
        ("ADI", "Ahmedabad Junction", "Ahmedabad", 23.0225, 72.5714, 1),
        ("ST", "Surat", "Surat", 21.2036, 72.8406, 0),
        ("PRYJ", "Prayagraj Junction", "Prayagraj", 25.4358, 81.8463, 1),
        ("SC", "Secunderabad Junction", "Hyderabad", 17.4399, 78.5017, 1),
        ("JP", "Jaipur Junction", "Jaipur", 26.9200, 75.7873, 1),
        ("PNBE", "Patna Junction", "Patna", 25.6093, 85.1235, 1)
    ]

    cursor.executemany(
        "INSERT INTO stations (code, name, city, lat, lng, is_junction) VALUES (?, ?, ?, ?, ?, ?)",
        stations
    )

    # 2. Insert Trains (50+ Express, Rajdhani, Superfast, Vande Bharat Trains)
    trains = [
        # North-South Corridor (NDLS <-> VGLJ <-> BPL <-> NGP <-> SC <-> SBC / MAS)
        ("12628", "Karnataka Express (DN)", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12627", "Karnataka Express (UP)", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("22691", "SBC Rajdhani (UP)", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("22692", "SBC Rajdhani (DN)", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12626", "Kerala Express", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12625", "Kerala Express Return", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12724", "Telangana Express", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12723", "Telangana Express Return", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12650", "Karnataka Sampark Kranti", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("12649", "Karnataka Sampark Kranti Return", "Express", 1, 1, 1, 1, 1, 1, 1),

        # Western Corridor (NDLS <-> JP <-> ADI <-> BRC <-> ST <-> MMCT)
        ("12952", "Mumbai Rajdhani (DN)", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12951", "Mumbai Rajdhani (UP)", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12954", "August Kranti Rajdhani", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12953", "August Kranti Return", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12009", "Shatabdi Express", "Superfast", 1, 1, 1, 1, 1, 1, 0),
        ("12958", "Swarna Jayanti Rajdhani", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12957", "Swarna Jayanti Return", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),

        # Eastern Corridor (NDLS <-> CNB <-> PRYJ <-> PNBE <-> HWH)
        ("12302", "Howrah Rajdhani (DN)", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12301", "Howrah Rajdhani (UP)", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12310", "Patna Rajdhani", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12309", "Patna Rajdhani Return", "Rajdhani", 1, 1, 1, 1, 1, 1, 1),
        ("12802", "Purushottam Express", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("12801", "Purushottam Express Return", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("22436", "Vande Bharat Express", "Vande Bharat", 1, 1, 0, 1, 1, 1, 1),

        # West-South Corridor (MMCT / BRC / ADI <-> SBC / MAS / SC)
        ("11013", "Lokmanya Tilak SF", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("11014", "Lokmanya Tilak SF Return", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("16534", "Jodhpur SBC Express", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("16533", "Jodhpur SBC Return", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("11041", "CSMT Chennai Mail", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("11042", "CSMT Chennai Mail Return", "Express", 1, 1, 1, 1, 1, 1, 1),

        # East-South Corridor (MAS <-> CNB <-> PRYJ <-> PNBE <-> HWH)
        ("12578", "Bagmati Express", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("12577", "Bagmati Express Return", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("12840", "Coromandel Express", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12839", "Coromandel Express Return", "Superfast", 1, 1, 1, 1, 1, 1, 1),

        # Inter-Corridors (PNBE / CNB / BPL / NGP <-> SBC / MAS / SC / MMCT)
        ("12296", "Sanghamitra Express", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12295", "Sanghamitra Express Return", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12976", "Jaipur Mysore Express", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("12975", "Jaipur Mysore Return", "Express", 1, 1, 1, 1, 1, 1, 1),
        ("22684", "LKO YPR SF Express", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("22683", "LKO YPR Return", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12834", "Howrah Ahmedabad SF", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12833", "Ahmedabad Howrah SF", "Superfast", 1, 1, 1, 1, 1, 1, 1),
        ("12612", "Garib Rath Express", "Garib Rath", 1, 1, 1, 1, 1, 1, 1),
        ("12611", "Garib Rath Return", "Garib Rath", 1, 1, 1, 1, 1, 1, 1)
    ]

    cursor.executemany(
        "INSERT INTO trains VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        trains
    )

    # 3. Insert Schedules
    schedules = [
        # --- 12628 Karnataka Exp (NDLS -> VGLJ -> BPL -> NGP -> SC -> SBC) ---
        ("12628", "NDLS", 1, None, "20:20", 1, 0, 3),
        ("12628", "VGLJ", 2, "01:00", "01:08", 2, 410, 1),
        ("12628", "BPL",  3, "04:45", "04:55", 2, 701, 1),
        ("12628", "NGP",  4, "10:25", "10:30", 2, 1090, 2),
        ("12628", "SC",   5, "20:10", "20:20", 2, 1668, 3),
        ("12628", "SBC",  6, "12:00", None,    3, 2400, 1),

        # --- 12627 Karnataka Exp Return (SBC -> SC -> NGP -> BPL -> VGLJ -> NDLS) ---
        ("12627", "SBC",  1, None, "19:20", 1, 0, 1),
        ("12627", "SC",   2, "11:00", "11:10", 2, 732, 2),
        ("12627", "NGP",  3, "21:15", "21:20", 2, 1310, 1),
        ("12627", "BPL",  4, "02:50", "03:00", 3, 1699, 3),
        ("12627", "VGLJ", 5, "06:25", "06:33", 3, 1990, 2),
        ("12627", "NDLS", 6, "11:30", None,    3, 2400, 4),

        # --- 22692 SBC Rajdhani (NDLS -> VGLJ -> BPL -> NGP -> SBC) ---
        ("22692", "NDLS", 1, None, "19:50", 1, 0, 5),
        ("22692", "VGLJ", 2, "00:28", "00:33", 2, 410, 2),
        ("22692", "BPL",  3, "03:45", "03:55", 2, 701, 1),
        ("22692", "NGP",  4, "09:20", "09:25", 2, 1090, 1),
        ("22692", "SBC",  5, "05:20", None,    3, 2365, 8),

        # --- 22691 SBC Rajdhani Return (SBC -> NGP -> BPL -> VGLJ -> NDLS) ---
        ("22691", "SBC",  1, None, "20:00", 1, 0, 8),
        ("22691", "NGP",  2, "15:00", "15:05", 2, 1275, 2),
        ("22691", "BPL",  3, "20:50", "21:00", 2, 1664, 1),
        ("22691", "VGLJ", 4, "00:10", "00:15", 3, 1955, 3),
        ("22691", "NDLS", 5, "05:30", None,    3, 2365, 5),

        # --- 12952 Mumbai Rajdhani (NDLS -> JP -> BRC -> ST -> MMCT) ---
        ("12952", "NDLS", 1, None, "16:55", 1, 0, 1),
        ("12952", "JP",   2, "20:30", "20:40", 1, 308, 1),
        ("12952", "BRC",  3, "01:00", "01:08", 2, 992, 1),
        ("12952", "ST",   4, "02:30", "02:35", 2, 1122, 1),
        ("12952", "MMCT", 5, "08:35", None,    2, 1384, 1),

        # --- 12951 Mumbai Rajdhani Return (MMCT -> ST -> BRC -> JP -> NDLS) ---
        ("12951", "MMCT", 1, None, "17:00", 1, 0, 1),
        ("12951", "ST",   2, "19:40", "19:45", 1, 262, 1),
        ("12951", "BRC",  3, "21:10", "21:18", 1, 392, 2),
        ("12951", "JP",   4, "03:15", "03:25", 2, 1076, 2),
        ("12951", "NDLS", 5, "08:32", None,    2, 1384, 1),

        # --- 12958 Swarna Jayanti Rajdhani (NDLS -> JP -> ADI) ---
        ("12958", "NDLS", 1, None, "19:55", 1, 0, 3),
        ("12958", "JP",   2, "23:45", "23:55", 1, 308, 2),
        ("12958", "ADI",  3, "06:55", None,    2, 934, 1),

        # --- 12957 Swarna Jayanti Return (ADI -> JP -> NDLS) ---
        ("12957", "ADI",  1, None, "17:45", 1, 0, 1),
        ("12957", "JP",   2, "01:10", "01:20", 2, 626, 1),
        ("12957", "NDLS", 3, "07:30", None,    2, 934, 2),

        # --- 12302 Howrah Rajdhani (NDLS -> CNB -> PRYJ -> PNBE -> HWH) ---
        ("12302", "NDLS", 1, None, "16:50", 1, 0, 9),
        ("12302", "CNB",  2, "21:32", "21:37", 1, 440, 1),
        ("12302", "PRYJ", 3, "23:43", "23:45", 1, 635, 4),
        ("12302", "PNBE", 4, "04:15", "04:25", 2, 1000, 1),
        ("12302", "HWH",  5, "09:55", None,    2, 1447, 9),

        # --- 12301 Howrah Rajdhani Return (HWH -> PNBE -> PRYJ -> CNB -> NDLS) ---
        ("12301", "HWH",  1, None, "16:50", 1, 0, 9),
        ("12301", "PNBE", 2, "22:10", "22:20", 1, 447, 2),
        ("12301", "PRYJ", 3, "02:43", "02:45", 2, 812, 1),
        ("12301", "CNB",  4, "04:50", "04:55", 2, 1007, 3),
        ("12301", "NDLS", 5, "10:05", None,    2, 1447, 1),

        # --- 12834 Howrah Ahmedabad SF (HWH -> PRYJ -> NGP -> BPL -> BRC -> ADI) ---
        ("12834", "HWH",  1, None, "23:55", 1, 0, 6),
        ("12834", "PRYJ", 2, "10:15", "10:25", 2, 812, 3),
        ("12834", "NGP",  3, "19:00", "19:10", 2, 1400, 2),
        ("12834", "BPL",  4, "01:30", "01:40", 3, 1789, 1),
        ("12834", "BRC",  5, "09:20", "09:30", 3, 2300, 3),
        ("12834", "ADI",  6, "12:05", None,    3, 2400, 4),

        # --- 12833 Ahmedabad Howrah SF (ADI -> BRC -> BPL -> NGP -> PRYJ -> HWH) ---
        ("12833", "ADI",  1, None, "00:25", 1, 0, 2),
        ("12833", "BRC",  2, "02:10", "02:20", 1, 100, 1),
        ("12833", "BPL",  3, "10:15", "10:25", 1, 611, 2),
        ("12833", "NGP",  4, "16:40", "16:50", 1, 1000, 1),
        ("12833", "PRYJ", 5, "01:20", "01:30", 2, 1588, 2),
        ("12833", "HWH",  6, "13:30", None,    2, 2400, 10),

        # --- 11013 Lokmanya Tilak SF (MMCT -> BRC -> SBC) ---
        ("11013", "MMCT", 1, None, "10:30", 1, 0, 1),
        ("11013", "BRC",  2, "17:10", "17:20", 1, 392, 3),
        ("11013", "SBC",  3, "15:15", None,    2, 1500, 5),

        # --- 11014 Lokmanya Tilak Return (SBC -> BRC -> MMCT) ---
        ("11014", "SBC",  1, None, "16:00", 1, 0, 4),
        ("11014", "BRC",  2, "13:40", "13:50", 2, 1108, 1),
        ("11014", "MMCT", 3, "20:30", None,    2, 1500, 2),

        # --- 12296 Sanghamitra Exp (PNBE -> CNB -> PRYJ -> VGLJ -> BPL -> NGP -> SBC) ---
        ("12296", "PNBE", 1, None, "20:15", 1, 0, 1),
        ("12296", "PRYJ", 2, "01:40", "01:45", 2, 360, 2),
        ("12296", "CNB",  3, "04:10", "04:20", 2, 555, 5),
        ("12296", "VGLJ", 4, "07:55", "08:03", 2, 775, 1),
        ("12296", "BPL",  5, "11:30", "11:40", 2, 1067, 3),
        ("12296", "NGP",  6, "17:40", "17:45", 2, 1456, 1),
        ("12296", "SBC",  7, "16:10", None,    3, 2730, 2),

        # --- 12295 Sanghamitra Return (SBC -> NGP -> BPL -> VGLJ -> CNB -> PRYJ -> PNBE) ---
        ("12295", "SBC",  1, None, "09:00", 1, 0, 3),
        ("12295", "NGP",  2, "08:20", "08:25", 2, 1274, 2),
        ("12295", "BPL",  3, "14:35", "14:45", 2, 1663, 1),
        ("12295", "VGLJ", 4, "18:30", "18:38", 2, 1955, 2),
        ("12295", "CNB",  5, "22:45", "22:55", 2, 2175, 4),
        ("12295", "PRYJ", 6, "01:25", "01:30", 3, 2370, 1),
        ("12295", "PNBE", 7, "07:40", None,    3, 2730, 1),

        # --- 12976 Jaipur Mysore Exp (JP -> BPL -> NGP -> SBC) ---
        ("12976", "JP",   1, None, "19:35", 1, 0, 4),
        ("12976", "BPL",  2, "07:20", "07:35", 2, 580, 4),
        ("12976", "NGP",  3, "13:45", "13:50", 2, 970, 2),
        ("12976", "SBC",  4, "13:00", None,    3, 2245, 6),

        # --- 12975 Jaipur Mysore Return (SBC -> NGP -> BPL -> JP) ---
        ("12975", "SBC",  1, None, "13:00", 1, 0, 5),
        ("12975", "NGP",  2, "11:50", "11:55", 2, 1275, 1),
        ("12975", "BPL",  3, "18:00", "18:10", 2, 1665, 3),
        ("12975", "JP",   4, "06:15", None,    3, 2245, 2),

        # --- 11041 CSMT Chennai Mail (MMCT -> BRC -> SC -> MAS) ---
        ("11041", "MMCT", 1, None, "14:00", 1, 0, 4),
        ("11041", "BRC",  2, "20:10", "20:20", 1, 392, 2),
        ("11041", "SC",   3, "11:15", "11:25", 2, 1200, 1),
        ("11041", "MAS",  4, "22:30", None,    2, 1890, 3),

        # --- 11042 CSMT Chennai Mail Return (MAS -> SC -> BRC -> MMCT) ---
        ("11042", "MAS",  1, None, "05:00", 1, 0, 2),
        ("11042", "SC",   2, "17:00", "17:10", 1, 690, 3),
        ("11042", "BRC",  3, "08:15", "08:25", 2, 1498, 1),
        ("11042", "MMCT", 4, "15:00", None,    2, 1890, 5),

        # --- 12578 Bagmati Express (MAS -> CNB -> PRYJ -> PNBE) ---
        ("12578", "MAS",  1, None, "19:30", 1, 0, 1),
        ("12578", "CNB",  2, "18:00", "18:10", 2, 1820, 2),
        ("12578", "PRYJ", 3, "21:00", "21:10", 2, 2015, 3),
        ("12578", "PNBE", 4, "06:00", None,    3, 2375, 4),

        # --- 12577 Bagmati Express Return (PNBE -> PRYJ -> CNB -> MAS) ---
        ("12577", "PNBE", 1, None, "15:45", 1, 0, 2),
        ("12577", "PRYJ", 2, "21:15", "21:25", 1, 360, 1),
        ("12577", "CNB",  3, "03:15", "03:25", 2, 555, 1),
        ("12577", "MAS",  4, "02:30", None,    3, 2375, 3),

        # --- 12840 Coromandel Express (MAS -> HWH) ---
        ("12840", "MAS",  1, None, "19:00", 1, 0, 1),
        ("12840", "HWH",  2, "14:30", None,    2, 1660, 8),

        # --- 12839 Coromandel Express Return (HWH -> MAS) ---
        ("12839", "HWH",  1, None, "23:45", 1, 0, 9),
        ("12839", "MAS",  2, "19:15", None,    2, 1660, 2),

        # --- 22684 LKO YPR SF (CNB -> VGLJ -> NGP -> SBC) ---
        ("22684", "CNB",  1, None, "20:30", 1, 0, 3),
        ("22684", "VGLJ", 2, "00:45", "00:53", 2, 220, 1),
        ("22684", "NGP",  3, "08:15", "08:20", 2, 750, 2),
        ("22684", "SBC",  4, "13:30", None,    3, 2030, 4),

        # --- 22683 LKO YPR Return (SBC -> NGP -> VGLJ -> CNB) ---
        ("22683", "SBC",  1, None, "15:45", 1, 0, 2),
        ("22683", "NGP",  2, "19:00", "19:05", 2, 1280, 1),
        ("22683", "VGLJ", 3, "03:15", "03:23", 3, 1810, 3),
        ("22683", "CNB",  4, "08:30", None,    3, 2030, 1)
    ]

    cursor.executemany(
        "INSERT INTO schedules (train_no, station_code, stop_seq, arrival_time, departure_time, day_number, distance_km, platform) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        schedules
    )

    conn.commit()
    conn.close()
    print("Database re-seeded with complete bi-directional schedules.")

if __name__ == '__main__':
    seed_railway_database()
