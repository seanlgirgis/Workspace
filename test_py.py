import sys
import itertools
import pandas as pd
import numpy as np
import io
from collections import defaultdict

print("--- Testing g03 ---")
try:
    N = 1_000_000
    dates_series = pd.Series(pd.date_range("2020-01-01", periods=N))
    island_ids_pd = (dates_series.diff().dt.days != 1).cumsum()
    def lazy_date_generator(n):
        for i in range(n):
            yield "2020-01-01"
    gen_group = itertools.groupby(lazy_date_generator(N))
    print("g03 success")
except Exception as e:
    import traceback
    traceback.print_exc()

print("--- Testing g05 ---")
try:
    SAMPLE_CSV = """server_id,cpu_pct,date,tier
srv-01,72,2026-02-01,prod
srv-01,73,2026-02-02,prod
srv-01,95,2026-02-03,prod
srv-01,97,2026-02-06,prod
srv-01,99,2026-02-07,prod
srv-02,45,2026-02-01,dev
"""
    df = pd.read_csv(io.StringIO(SAMPLE_CSV))
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['server_id', 'date']).reset_index(drop=True)
    df['day_diff'] = df.groupby('server_id')['date'].diff().dt.days
    df['is_new_island'] = df['day_diff'] != 1
    df['island_id'] = df['is_new_island'].cumsum()
    islands = df.groupby(['server_id', 'island_id']).agg(
        streak_start=('date', 'min'),
        streak_end=('date', 'max'),
        streak_days=('date', 'count')
    ).reset_index()
    print("g05 success")
except Exception as e:
    import traceback
    traceback.print_exc()

print("--- Testing g06 ---")
try:
    def parse_csv_stream(fileobj):
        next(fileobj)
        for line in fileobj:
            p = line.strip().split(',')
            if len(p) >= 3:
                yield {'server_id': p[0], 'date': p[2]}

    def map_to_servers(record_stream):
        observed = defaultdict(set)
        for rec in record_stream:
            observed[rec['server_id']].add(rec['date'])
        return observed

    def calculate_gaps(server_map, date_spine_set):
        for srv, dates_seen in server_map.items():
            missing = date_spine_set - dates_seen
            yield srv, missing

    f = io.StringIO(SAMPLE_CSV)
    expected_spine = {f"2026-02-{day:02d}" for day in range(1, 8)}
    parsed_stream = parse_csv_stream(f)
    server_dict = map_to_servers(parsed_stream)
    gaps_stream = calculate_gaps(server_dict, expected_spine)
    for srv, missing_set in gaps_stream:
        pass
    print("g06 success")
except Exception as e:
    import traceback
    traceback.print_exc()

print("--- Testing g08 ---")
try:
    spine = pd.date_range('2026-03-01', periods=3)
    data_points = [1, 2, 3, 10, 11, 4, 5]
    for is_valid, group in itertools.groupby(data_points, key=lambda x: x < 10):
        pass
    s = pd.Series(["A", "B"], index=pd.to_datetime(['2026-03-01', '2026-03-03']))
    filled = s.reindex(spine)
    print("g08 success")
except Exception as e:
    import traceback
    traceback.print_exc()
