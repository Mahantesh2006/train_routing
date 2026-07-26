import pytest
from backend.seed_data import seed_railway_database
from backend.routing_engine import search_routes, get_direct_routes, find_connecting_routes

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    seed_railway_database()

def test_direct_route_search():
    # NDLS -> SBC has direct trains (12628 Karnataka Exp, 22692 Rajdhani, 12650 Sampark Kranti)
    results = search_routes("NDLS", "SBC", "2026-07-27") # Monday
    assert results["direct_routes_count"] > 0
    direct = [r for r in results["routes"] if r["type"] == "DIRECT"]
    assert len(direct) >= 1
    assert direct[0]["legs"][0]["from_station"] == "NDLS"
    assert direct[0]["legs"][0]["to_station"] == "SBC"

def test_connecting_route_search_with_buffer_constraints():
    # Test indirect connection from Patna (PNBE) to Bengaluru (SBC) or New Delhi to Bengaluru via Bhopal (BPL)
    # Leg 1: NDLS -> BPL (12650 Sampark Kranti arrives at BPL at 16:55 Day 1)
    # Leg 2 options: 12976 Jaipur Mysore Exp (dep BPL 07:35 Day 2) -> Layover = 14h 40m (880 mins)
    # With min_buffer = 45, max_buffer = 1200 mins (20 hours), it should be found!
    results = search_routes("NDLS", "SBC", "2026-07-27", min_buffer_mins=45, max_buffer_mins=1200)
    assert results["connecting_routes_count"] > 0
    
    connecting = [r for r in results["routes"] if r["type"] == "1-STOP CONNECTING"]
    assert len(connecting) > 0
    first_conn = connecting[0]
    assert first_conn["total_transfers"] == 1
    assert "junction" in first_conn
    assert first_conn["layover_mins"] >= 45
    assert first_conn["layover_mins"] <= 1200

def test_buffer_constraint_filtering():
    # Narrow buffer range: min=45 mins, max=120 mins
    results_narrow = search_routes("NDLS", "SBC", "2026-07-27", min_buffer_mins=45, max_buffer_mins=120)
    # Wide buffer range: min=45 mins, max=1200 mins
    results_wide = search_routes("NDLS", "SBC", "2026-07-27", min_buffer_mins=45, max_buffer_mins=1200)
    
    assert results_wide["connecting_routes_count"] >= results_narrow["connecting_routes_count"]

def test_sorting_modes():
    # Test sorting by duration, fare, layover
    dur_results = search_routes("NDLS", "SBC", "2026-07-27", min_buffer_mins=45, max_buffer_mins=1200, sort_by="duration")
    fare_results = search_routes("NDLS", "SBC", "2026-07-27", min_buffer_mins=45, max_buffer_mins=1200, sort_by="fare")
    
    # Assert sorted order
    durations = [r["total_duration_mins"] for r in dur_results["routes"]]
    assert durations == sorted(durations)

    fares = [r["total_fare"] for r in fare_results["routes"]]
    assert fares == sorted(fares)

if __name__ == '__main__':
    pytest.main(["-v", "test_routing.py"])
