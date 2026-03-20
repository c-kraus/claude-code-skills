#!/usr/bin/env python3
"""
analyze_fit.py – Liest eine oder mehrere FIT-Dateien und gibt eine
strukturierte JSON-Zusammenfassung aus, die der Skill weiterverarbeitet.

Usage:
    python analyze_fit.py <fit_or_fit_gz_file> [<file2> ...]
"""

import sys
import gzip
import json
import math
from pathlib import Path
from datetime import timedelta

try:
    import fitparse
except ImportError:
    print("ERROR: fitparse nicht installiert. Bitte: pip install fitparse", file=sys.stderr)
    sys.exit(1)


def load_fitfile(path: Path) -> fitparse.FitFile:
    if path.suffix == ".gz":
        with gzip.open(path, "rb") as f:
            data = f.read()
        return fitparse.FitFile(data)
    else:
        return fitparse.FitFile(str(path))


def seconds_to_hms(s: float) -> str:
    s = int(s)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}"


def analyze_session(path: Path) -> dict:
    fitfile = load_fitfile(path)

    # --- Session-Daten ---
    session_data = {}
    for session in fitfile.get_messages("session"):
        session_data = {d.name: d.value for d in session if d.value is not None}
    if not session_data:
        return {"error": f"Keine Session-Daten in {path.name}"}

    ftp = session_data.get("threshold_power", None)
    total_time_s = session_data.get("total_timer_time", 0)
    np = session_data.get("normalized_power", None)
    avg_power = session_data.get("avg_power", None)
    tss = session_data.get("training_stress_score", None)
    if_val = session_data.get("intensity_factor", None)

    # --- Power-Zonen (% Zeit) ---
    pz_raw = session_data.get("time_in_power_zone", None)
    power_zones = None
    if pz_raw and total_time_s > 0:
        labels = ["Z1 (<55%)", "Z2 (56-75%)", "Z3 (76-90%)", "Z4 (91-105%)", "Z5 (106-120%)", "Z6 (>120%)"]
        total_pz = sum(pz_raw)
        power_zones = {
            labels[i]: {
                "seconds": round(pz_raw[i], 1),
                "pct": round(pz_raw[i] / total_pz * 100, 1) if total_pz > 0 else 0
            }
            for i in range(min(len(labels), len(pz_raw)))
        }

    # --- HR-Zonen (% Zeit) ---
    hr_raw = session_data.get("time_in_hr_zone", None)
    hr_zones = None
    if hr_raw and total_time_s > 0:
        hr_labels = ["Z1 (Erholung)", "Z2 (Grundlage)", "Z3 (Tempo)", "Z4 (Schwelle)", "Z5 (VO2max)"]
        total_hr = sum(hr_raw)
        hr_zones = {
            hr_labels[i]: {
                "seconds": round(hr_raw[i], 1),
                "pct": round(hr_raw[i] / total_hr * 100, 1) if total_hr > 0 else 0
            }
            for i in range(min(len(hr_labels), len(hr_raw)))
        }

    # --- Workout-Typ aus workout-Message ---
    workout_name = None
    for wkt in fitfile.get_messages("workout"):
        wkt_data = {d.name: d.value for d in wkt if d.value is not None}
        workout_name = wkt_data.get("wkt_name", None)

    # --- Polarisierungsindex (einfach: Z1+Z2 vs Z4+Z5+Z6) ---
    polarization_index = None
    if power_zones:
        low = sum(v["pct"] for k, v in power_zones.items() if k.startswith(("Z1", "Z2")))
        high = sum(v["pct"] for k, v in power_zones.items() if k.startswith(("Z4", "Z5", "Z6")))
        mid = sum(v["pct"] for k, v in power_zones.items() if k.startswith("Z3"))
        polarization_index = {"low_pct": round(low, 1), "mid_pct": round(mid, 1), "high_pct": round(high, 1)}

    # --- Kadenz: aktiver Durchschnitt (Nullwerte = Leerlauf/Ausrollen herausfiltern) ---
    cadence_active_avg = None
    try:
        fitfile2 = load_fitfile(path)
        cadences = [
            d.value for msg in fitfile2.get_messages("record")
            for d in msg if d.name == "cadence" and d.value is not None and d.value > 0
        ]
        if cadences:
            cadence_active_avg = round(sum(cadences) / len(cadences), 1)
    except Exception:
        pass

    result = {
        "file": path.name,
        "date": session_data.get("start_time").isoformat() if session_data.get("start_time") else None,
        "duration_hms": seconds_to_hms(total_time_s),
        "duration_s": total_time_s,
        "distance_km": round(session_data.get("total_distance", 0) / 1000, 2),
        "total_calories": session_data.get("total_calories"),
        "total_ascent_m": session_data.get("total_ascent"),
        "avg_power_w": avg_power,
        "normalized_power_w": np,
        "ftp_w": ftp,
        "intensity_factor": round(if_val, 3) if if_val else None,
        "tss": round(tss, 1) if tss else None,
        "avg_hr": session_data.get("avg_heart_rate"),
        "max_hr": session_data.get("max_heart_rate"),
        "avg_cadence": session_data.get("avg_cadence"),
        "avg_cadence_active": cadence_active_avg,
        "avg_speed_kmh": round(session_data.get("avg_speed", 0) * 3.6, 1),
        "sport": session_data.get("sport"),
        "workout_name": workout_name,
        "power_zones": power_zones,
        "hr_zones": hr_zones,
        "polarization": polarization_index,
    }
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: analyze_fit.py <file.fit[.gz]> [<file2> ...]")
        sys.exit(1)

    results = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.exists():
            results.append({"error": f"Datei nicht gefunden: {arg}"})
            continue
        results.append(analyze_session(p))

    if len(results) == 1:
        print(json.dumps(results[0], indent=2, default=str))
    else:
        print(json.dumps(results, indent=2, default=str))
