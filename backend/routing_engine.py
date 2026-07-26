import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta, date
from database import get_db_connection


WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

def parse_time(time_str):
    if not time_str:
        return 0, 0
    parts = time_str.split(":")
    return int(parts[0]), int(parts[1])

def calculate_fare(distance_km, train_type="Express"):
    multiplier = 1.0
    if train_type == "Rajdhani":
        multiplier = 1.8
    elif train_type == "Vande Bharat":
        multiplier = 2.0
    elif train_type == "Superfast":
        multiplier = 1.3
    elif train_type == "Garib Rath":
        multiplier = 1.1
    
    base_fare = 50 + (distance_km * 0.85 * multiplier)
    return round(base_fare)

def check_train_runs_on_day(train_row, day_index):
    # day_index: 0=Mon, 1=Tue, ..., 6=Sun
    col = f"runs_{WEEKDAYS[day_index]}"
    return bool(train_row[col])

def get_direct_routes(origin, destination, departure_date):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        s1.train_no,
        t.name as train_name,
        t.train_type,
        t.runs_mon, t.runs_tue, t.runs_wed, t.runs_thu, t.runs_fri, t.runs_sat, t.runs_sun,
        s1.departure_time as origin_dep_time,
        s1.day_number as origin_day_seq,
        s1.platform as origin_platform,
        s2.arrival_time as dest_arr_time,
        s2.day_number as dest_day_seq,
        s2.platform as dest_platform,
        (s2.distance_km - s1.distance_km) as distance_km,
        st1.name as origin_name,
        st2.name as dest_name
    FROM schedules s1
    JOIN schedules s2 ON s1.train_no = s2.train_no AND s1.stop_seq < s2.stop_seq
    JOIN trains t ON s1.train_no = t.train_no
    JOIN stations st1 ON s1.station_code = st1.code
    JOIN stations st2 ON s2.station_code = st2.code
    WHERE s1.station_code = ? AND s2.station_code = ?
    """

    cursor.execute(query, (origin, destination))
    rows = cursor.fetchall()
    
    direct_routes = []
    dep_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()

    for row in rows:
        # Check if train operates on departure_date's day of week
        day_idx = dep_date_obj.weekday()
        if not check_train_runs_on_day(row, day_idx):
            continue

        # Calculate exact origin departure datetime
        dep_h, dep_m = parse_time(row['origin_dep_time'])
        origin_dep_dt = datetime.combine(dep_date_obj, datetime.min.time()) + timedelta(hours=dep_h, minutes=dep_m)

        # Calculate destination arrival datetime accounting for day offsets
        day_diff = row['dest_day_seq'] - row['origin_day_seq']
        arr_h, arr_m = parse_time(row['dest_arr_time'])
        dest_arr_dt = datetime.combine(dep_date_obj + timedelta(days=day_diff), datetime.min.time()) + timedelta(hours=arr_h, minutes=arr_m)

        duration_mins = int((dest_arr_dt - origin_dep_dt).total_seconds() / 60)
        fare = calculate_fare(row['distance_km'], row['train_type'])

        route = {
            "type": "DIRECT",
            "total_duration_mins": duration_mins,
            "total_fare": fare,
            "total_transfers": 0,
            "origin": {"code": origin, "name": row['origin_name']},
            "destination": {"code": destination, "name": row['dest_name']},
            "departure_datetime": origin_dep_dt.strftime("%Y-%m-%d %H:%M"),
            "arrival_datetime": dest_arr_dt.strftime("%Y-%m-%d %H:%M"),
            "legs": [
                {
                    "leg_number": 1,
                    "train_no": row['train_no'],
                    "train_name": row['train_name'],
                    "train_type": row['train_type'],
                    "from_station": origin,
                    "from_station_name": row['origin_name'],
                    "to_station": destination,
                    "to_station_name": row['dest_name'],
                    "departure": origin_dep_dt.strftime("%Y-%m-%d %H:%M"),
                    "arrival": dest_arr_dt.strftime("%Y-%m-%d %H:%M"),
                    "departure_platform": row['origin_platform'],
                    "arrival_platform": row['dest_platform'],
                    "distance_km": row['distance_km'],
                    "duration_mins": duration_mins,
                    "fare": fare
                }
            ]
        }
        direct_routes.append(route)

    conn.close()
    return direct_routes

def find_connecting_routes(origin, destination, departure_date, min_buffer_mins=45, max_buffer_mins=360):
    conn = get_db_connection()
    cursor = conn.cursor()

    dep_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()

    # PHASE 1: Identify Junction Stations
    # Set 1: Stations reachable from Origin A
    cursor.execute("""
        SELECT DISTINCT s2.station_code 
        FROM schedules s1
        JOIN schedules s2 ON s1.train_no = s2.train_no AND s1.stop_seq < s2.stop_seq
        WHERE s1.station_code = ?
    """, (origin,))
    set1 = {row['station_code'] for row in cursor.fetchall()}

    # Set 2: Stations that can reach Destination C
    cursor.execute("""
        SELECT DISTINCT s1.station_code 
        FROM schedules s1
        JOIN schedules s2 ON s1.train_no = s2.train_no AND s1.stop_seq < s2.stop_seq
        WHERE s2.station_code = ?
    """, (destination,))
    set2 = {row['station_code'] for row in cursor.fetchall()}

    # Candidate transfer junctions B = Set 1 ∩ Set 2 (excluding Origin and Destination)
    junctions = (set1 & set2) - {origin, destination}

    connecting_routes = []

    # PHASE 2: Apply Time Constraints for each candidate junction B
    for junction in junctions:
        # Leg 1: Origin A -> Junction B
        cursor.execute("""
            SELECT 
                s1.train_no, t.name as train_name, t.train_type,
                t.runs_mon, t.runs_tue, t.runs_wed, t.runs_thu, t.runs_fri, t.runs_sat, t.runs_sun,
                s1.departure_time as origin_dep_time, s1.day_number as origin_day_seq, s1.platform as origin_platform,
                s2.arrival_time as junc_arr_time, s2.day_number as junc_day_seq, s2.platform as junc_arr_platform,
                (s2.distance_km - s1.distance_km) as distance_km,
                st1.name as origin_name, st2.name as junction_name
            FROM schedules s1
            JOIN schedules s2 ON s1.train_no = s2.train_no AND s1.stop_seq < s2.stop_seq
            JOIN trains t ON s1.train_no = t.train_no
            JOIN stations st1 ON s1.station_code = st1.code
            JOIN stations st2 ON s2.station_code = st2.code
            WHERE s1.station_code = ? AND s2.station_code = ?
        """, (origin, junction))
        leg1_candidates = cursor.fetchall()

        # Leg 2: Junction B -> Destination C
        cursor.execute("""
            SELECT 
                s1.train_no, t.name as train_name, t.train_type,
                t.runs_mon, t.runs_tue, t.runs_wed, t.runs_thu, t.runs_fri, t.runs_sat, t.runs_sun,
                s1.departure_time as junc_dep_time, s1.day_number as junc_day_seq, s1.platform as junc_dep_platform,
                s2.arrival_time as dest_arr_time, s2.day_number as dest_day_seq, s2.platform as dest_platform,
                (s2.distance_km - s1.distance_km) as distance_km,
                st1.name as junction_name, st2.name as dest_name
            FROM schedules s1
            JOIN schedules s2 ON s1.train_no = s2.train_no AND s1.stop_seq < s2.stop_seq
            JOIN trains t ON s1.train_no = t.train_no
            JOIN stations st1 ON s1.station_code = st1.code
            JOIN stations st2 ON s2.station_code = st2.code
            WHERE s1.station_code = ? AND s2.station_code = ?
        """, (junction, destination))
        leg2_candidates = cursor.fetchall()

        for leg1 in leg1_candidates:
            # Check Leg 1 operating day
            if not check_train_runs_on_day(leg1, dep_date_obj.weekday()):
                continue

            leg1_dep_h, leg1_dep_m = parse_time(leg1['origin_dep_time'])
            leg1_dep_dt = datetime.combine(dep_date_obj, datetime.min.time()) + timedelta(hours=leg1_dep_h, minutes=leg1_dep_m)

            leg1_day_diff = leg1['junc_day_seq'] - leg1['origin_day_seq']
            leg1_arr_h, leg1_arr_m = parse_time(leg1['junc_arr_time'])
            leg1_arr_dt = datetime.combine(dep_date_obj + timedelta(days=leg1_day_diff), datetime.min.time()) + timedelta(hours=leg1_arr_h, minutes=leg1_arr_m)

            for leg2 in leg2_candidates:
                # Avoid taking the exact same train for both legs (which would be a direct train)
                if leg1['train_no'] == leg2['train_no']:
                    continue

                # Find valid departure for Leg 2 at Junction B on or after leg1_arr_dt + min_buffer
                # Check next 7 days for matching day-of-week operation for Leg 2 origin start
                leg2_dep_h, leg2_dep_m = parse_time(leg2['junc_dep_time'])

                # Try potential calendar departure dates for Leg 2
                found_valid_leg2 = False
                for day_offset in range(0, 4): # Search up to 3 days after arrival
                    check_junc_date = leg1_arr_dt.date() + timedelta(days=day_offset)
                    
                    # Calculate original start date of Leg 2 train based on junc_day_seq offset
                    leg2_start_date = check_junc_date - timedelta(days=leg2['junc_day_seq'] - 1)
                    if not check_train_runs_on_day(leg2, leg2_start_date.weekday()):
                        continue

                    leg2_dep_dt = datetime.combine(check_junc_date, datetime.min.time()) + timedelta(hours=leg2_dep_h, minutes=leg2_dep_m)

                    # Calculate wait / buffer time at Junction B
                    buffer_mins = int((leg2_dep_dt - leg1_arr_dt).total_seconds() / 60)

                    # Δtmin <= Departure(Train2) - Arrival(Train1) <= Δtmax
                    if min_buffer_mins <= buffer_mins <= max_buffer_mins:
                        found_valid_leg2 = True
                        
                        # Calculate Leg 2 arrival at Destination C
                        leg2_day_diff = leg2['dest_day_seq'] - leg2['junc_day_seq']
                        leg2_arr_h, leg2_arr_m = parse_time(leg2['dest_arr_time'])
                        leg2_arr_dt = datetime.combine(check_junc_date + timedelta(days=leg2_day_diff), datetime.min.time()) + timedelta(hours=leg2_arr_h, minutes=leg2_arr_m)

                        leg1_duration = int((leg1_arr_dt - leg1_dep_dt).total_seconds() / 60)
                        leg2_duration = int((leg2_arr_dt - leg2_dep_dt).total_seconds() / 60)
                        total_duration = int((leg2_arr_dt - leg1_dep_dt).total_seconds() / 60)

                        leg1_fare = calculate_fare(leg1['distance_km'], leg1['train_type'])
                        leg2_fare = calculate_fare(leg2['distance_km'], leg2['train_type'])
                        total_fare = leg1_fare + leg2_fare

                        route = {
                            "type": "1-STOP CONNECTING",
                            "junction": {"code": junction, "name": leg1['junction_name']},
                            "total_duration_mins": total_duration,
                            "layover_mins": buffer_mins,
                            "total_fare": total_fare,
                            "total_transfers": 1,
                            "origin": {"code": origin, "name": leg1['origin_name']},
                            "destination": {"code": destination, "name": leg2['dest_name']},
                            "departure_datetime": leg1_dep_dt.strftime("%Y-%m-%d %H:%M"),
                            "arrival_datetime": leg2_arr_dt.strftime("%Y-%m-%d %H:%M"),
                            "legs": [
                                {
                                    "leg_number": 1,
                                    "train_no": leg1['train_no'],
                                    "train_name": leg1['train_name'],
                                    "train_type": leg1['train_type'],
                                    "from_station": origin,
                                    "from_station_name": leg1['origin_name'],
                                    "to_station": junction,
                                    "to_station_name": leg1['junction_name'],
                                    "departure": leg1_dep_dt.strftime("%Y-%m-%d %H:%M"),
                                    "arrival": leg1_arr_dt.strftime("%Y-%m-%d %H:%M"),
                                    "departure_platform": leg1['origin_platform'],
                                    "arrival_platform": leg1['junc_arr_platform'],
                                    "distance_km": leg1['distance_km'],
                                    "duration_mins": leg1_duration,
                                    "fare": leg1_fare
                                },
                                {
                                    "leg_number": 2,
                                    "train_no": leg2['train_no'],
                                    "train_name": leg2['train_name'],
                                    "train_type": leg2['train_type'],
                                    "from_station": junction,
                                    "from_station_name": leg2['junction_name'],
                                    "to_station": destination,
                                    "to_station_name": leg2['dest_name'],
                                    "departure": leg2_dep_dt.strftime("%Y-%m-%d %H:%M"),
                                    "arrival": leg2_arr_dt.strftime("%Y-%m-%d %H:%M"),
                                    "departure_platform": leg2['junc_dep_platform'],
                                    "arrival_platform": leg2['dest_platform'],
                                    "distance_km": leg2['distance_km'],
                                    "duration_mins": leg2_duration,
                                    "fare": leg2_fare
                                }
                            ]
                        }
                        connecting_routes.append(route)
                        break # Found nearest valid connection for this pair

    conn.close()
    return connecting_routes

def search_routes(origin, destination, departure_date, min_buffer_mins=45, max_buffer_mins=360, sort_by="duration"):
    direct = get_direct_routes(origin, destination, departure_date)
    connecting = find_connecting_routes(origin, destination, departure_date, min_buffer_mins, max_buffer_mins)

    all_routes = direct + connecting

    # PHASE 3: Rank & Sort Options
    if sort_by == "layover":
        all_routes.sort(key=lambda x: (x.get("layover_mins", 0), x["total_duration_mins"]))
    elif sort_by == "fare":
        all_routes.sort(key=lambda x: (x["total_fare"], x["total_duration_mins"]))
    elif sort_by == "earliest_arrival":
        all_routes.sort(key=lambda x: x["arrival_datetime"])
    else: # "duration" (default)
        all_routes.sort(key=lambda x: x["total_duration_mins"])

    return {
        "search_parameters": {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "min_buffer_mins": min_buffer_mins,
            "max_buffer_mins": max_buffer_mins,
            "sort_by": sort_by
        },
        "total_routes_found": len(all_routes),
        "direct_routes_count": len(direct),
        "connecting_routes_count": len(connecting),
        "routes": all_routes
    }
