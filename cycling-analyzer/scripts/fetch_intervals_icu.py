#!/usr/bin/env python3
"""
fetch_intervals_icu.py – Ruft Aktivitätsdaten von intervals.icu ab
und gibt strukturiertes JSON aus, das der Skill weiterverarbeitet.

Usage:
    # Einzelner Tag
    python fetch_intervals_icu.py --athlete-id i12345 --api-key abc123 --date 2026-03-20

    # Letzte N Tage
    python fetch_intervals_icu.py --athlete-id i12345 --api-key abc123 --days 7

    # Expliziter Datumsbereich
    python fetch_intervals_icu.py --athlete-id i12345 --api-key abc123 \\
        --oldest 2026-02-01 --newest 2026-03-20

    # Mit Intervall-Details (pro Aktivität)
    python fetch_intervals_icu.py ... --with-intervals

    # Credentials aus Datei lesen (statt Args)
    python fetch_intervals_icu.py --creds-file /tmp/.icu_creds --date 2026-03-20
"""

import requests
import json
import sys
import argparse
from datetime import date, timedelta
from pathlib import Path


BASE_URL = "https://intervals.icu/api/v1"

# Cycling-relevante Sport-Typen
CYCLING_TYPES = {
    "Ride", "VirtualRide", "GravelRide", "MountainBikeRide",
    "EBikeRide", "EMountainBikeRide", "Velomobile"
}


def seconds_to_hms(s: int) -> str:
    if not s:
        return "0:00:00"
    s = int(s)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}"


def get_auth(api_key: str):
    return ("API_KEY", api_key)


def fetch_activities(athlete_id: str, api_key: str, oldest: str, newest: str) -> list:
    """Ruft alle Aktivitäten in einem Datumsbereich ab (JSON-Liste)."""
    url = f"{BASE_URL}/athlete/{athlete_id}/activities"
    resp = requests.get(
        url,
        auth=get_auth(api_key),
        params={"oldest": oldest, "newest": newest},
        timeout=30,
    )
    if resp.status_code == 401:
        print(json.dumps({"error": "Authentifizierung fehlgeschlagen — API Key oder Athlete ID prüfen"}))
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def fetch_activity_detail(api_key: str, activity_id: str) -> dict:
    """Ruft Detaildaten inkl. Intervalle für eine Aktivität ab."""
    url = f"{BASE_URL}/activity/{activity_id}"
    resp = requests.get(
        url,
        auth=get_auth(api_key),
        params={"intervals": "true"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def extract_activity_summary(a: dict) -> dict:
    """Extrahiert die wesentlichen Felder aus einem Aktivitätsobjekt der Listen-API."""
    # Wahoo/intervals.icu-spezifische Feldnamen
    np_w = a.get("icu_weighted_avg_watts")
    avg_w = a.get("icu_average_watts")
    ftp = a.get("icu_ftp")
    if_raw = a.get("icu_intensity")  # Wert ist IF * 100
    if_val = if_raw / 100 if if_raw else None
    tss = a.get("icu_training_load")
    moving_time = a.get("moving_time") or 0

    # Zonendaten aus Listen-Antwort (Format: [{'id': 'Z1', 'secs': N}, ...])
    zone_list = a.get("icu_zone_times") or []
    power_zones = None
    if zone_list and isinstance(zone_list[0], dict):
        total_z = sum(z.get("secs", 0) for z in zone_list)
        power_zones = {
            z["id"]: {
                "seconds": z["secs"],
                "pct": round(z["secs"] / total_z * 100, 1) if total_z > 0 else 0,
            }
            for z in zone_list if "id" in z and "secs" in z
        }

    hr_zone_list = a.get("icu_hr_zone_times") or []
    hr_zones = None
    if hr_zone_list and isinstance(hr_zone_list, list) and hr_zone_list:
        hr_labels = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7"]
        if isinstance(hr_zone_list[0], int):
            total_hr = sum(hr_zone_list)
            hr_zones = {
                hr_labels[i]: {
                    "seconds": hr_zone_list[i],
                    "pct": round(hr_zone_list[i] / total_hr * 100, 1) if total_hr > 0 else 0,
                }
                for i in range(min(len(hr_labels), len(hr_zone_list)))
            }

    return {
        "id": a.get("id"),
        "name": a.get("name"),
        "date": (a.get("start_date_local") or "")[:10],
        "sport_type": a.get("type"),
        "duration_hms": seconds_to_hms(moving_time),
        "duration_s": moving_time,
        "distance_km": round((a.get("distance") or 0) / 1000, 2),
        "elevation_m": a.get("total_elevation_gain"),
        "avg_power_w": avg_w,
        "normalized_power_w": np_w,
        "ftp_w": ftp,
        "intensity_factor": round(if_val, 3) if if_val else None,
        "tss": round(tss, 1) if tss else None,
        "variability_index": round(np_w / avg_w, 3) if np_w and avg_w and avg_w > 0 else None,
        "avg_hr": a.get("average_heartrate"),
        "max_hr": a.get("max_heartrate"),
        "avg_cadence": a.get("average_cadence"),
        "left_right_balance": a.get("left_right_balance"),
        "pw_hr": a.get("icu_power_hr"),  # Pw:Hr Effizienzfaktor
        "power_zones": power_zones,
        "hr_zones": hr_zones,
    }


def extract_interval(i: dict, idx: int) -> dict:
    """Extrahiert ein einzelnes Intervall aus dem icu_intervals-Array."""
    return {
        "index": idx,
        "type": i.get("type"),           # WORK oder REST
        "label": i.get("label") or i.get("group_id"),
        "duration_s": i.get("moving_time"),
        "duration_hms": seconds_to_hms(i.get("moving_time") or 0),
        "avg_watts": i.get("average_watts"),
        "np_watts": i.get("weighted_average_watts"),
        "min_watts": i.get("min_watts"),
        "max_watts": i.get("max_watts"),
        "avg_watts_kg": i.get("average_watts_kg"),
        "intensity_pct": i.get("intensity"),          # IF * 100
        "zone": i.get("zone"),
        "avg_hr": i.get("average_heartrate"),
        "max_hr": i.get("max_heartrate"),
        "min_hr": i.get("min_heartrate"),
        "avg_cadence": i.get("average_cadence"),
        "min_cadence": i.get("min_cadence"),
        "max_cadence": i.get("max_cadence"),
        "avg_torque_nm": i.get("average_torque"),     # Schlüssel für K3-Analyse
        "max_torque_nm": i.get("max_torque"),
        "decoupling_pct": i.get("decoupling"),        # Pw:Hr-Entkopplung
        "training_load": i.get("training_load"),      # TSS-Anteil
    }


def compute_interval_summary(work_intervals: list) -> dict:
    """Berechnet zusammenfassende Metriken über alle WORK-Intervalle."""
    if not work_intervals:
        return {}

    n = len(work_intervals)

    def avg_field(field):
        vals = [i.get(field) for i in work_intervals if i.get(field) is not None]
        return round(sum(vals) / len(vals), 2) if vals else None

    first_w = work_intervals[0].get("avg_watts")
    last_w = work_intervals[-1].get("avg_watts")
    decay_pct = round((last_w - first_w) / first_w * 100, 1) if first_w and last_w else None

    first_hr = work_intervals[0].get("avg_hr")
    last_hr = work_intervals[-1].get("avg_hr")
    hr_drift_pct = round((last_hr - first_hr) / first_hr * 100, 1) if first_hr and last_hr else None

    return {
        "count_work_intervals": n,
        "avg_watts_first_interval": first_w,
        "avg_watts_last_interval": last_w,
        "power_decay_pct": decay_pct,       # negativ = Leistungsabfall
        "avg_watts_all": avg_field("avg_watts"),
        "avg_np_all": avg_field("np_watts"),
        "avg_hr_first_interval": first_hr,
        "avg_hr_last_interval": last_hr,
        "hr_drift_pct": hr_drift_pct,
        "avg_hr_all": avg_field("avg_hr"),
        "max_hr_peak": max((i.get("max_hr") or 0 for i in work_intervals), default=None),
        "avg_cadence_all": avg_field("avg_cadence"),
        "avg_torque_nm": avg_field("avg_torque_nm"),   # K3-Qualitätsmerkmal
        "avg_decoupling_pct": avg_field("decoupling_pct"),
    }


def enrich_with_detail(activity: dict, api_key: str) -> dict:
    """Holt Intervall-Detaildaten und fügt sie zur Aktivitätszusammenfassung hinzu."""
    try:
        detail = fetch_activity_detail(api_key, activity["id"])
    except Exception as e:
        activity["intervals_error"] = str(e)
        return activity

    raw_intervals = detail.get("icu_intervals") or []
    parsed = [extract_interval(i, idx) for idx, i in enumerate(raw_intervals)]
    work_intervals = [i for i in parsed if i.get("type") == "WORK"]

    activity["intervals"] = parsed
    activity["interval_summary"] = compute_interval_summary(work_intervals)
    # Power- und HR-Zonen kommen bereits aus extract_activity_summary (Listen-API)
    return activity


def load_creds_file(path: str) -> tuple:
    """Liest Athlete-ID und API-Key aus einer simplen Key=Value-Datei."""
    athlete_id, api_key = None, None
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("ATHLETE_ID="):
                    athlete_id = line.split("=", 1)[1]
                elif line.startswith("API_KEY="):
                    api_key = line.split("=", 1)[1]
    except FileNotFoundError:
        pass
    return athlete_id, api_key


def main():
    parser = argparse.ArgumentParser(description="Intervals.icu Aktivitätsdaten abrufen")
    parser.add_argument("--athlete-id", help="Intervals.icu Athlete-ID (z.B. i12345)")
    parser.add_argument("--api-key", help="Intervals.icu API Key")
    parser.add_argument("--creds-file",
                        default=str(Path(__file__).parent.parent / ".icu_creds"),
                        help="Datei mit ATHLETE_ID= und API_KEY=")
    parser.add_argument("--date", help="Einzelner Tag YYYY-MM-DD")
    parser.add_argument("--days", type=int, help="Letzte N Tage (ab heute)")
    parser.add_argument("--oldest", help="Ältestes Datum YYYY-MM-DD")
    parser.add_argument("--newest", help="Neuestes Datum YYYY-MM-DD")
    parser.add_argument("--with-intervals", action="store_true",
                        help="Intervall-Details für jede Aktivität abrufen")
    parser.add_argument("--all-sports", action="store_true",
                        help="Alle Sportarten (Standard: nur Rad)")
    args = parser.parse_args()

    # Credentials: CLI-Args haben Vorrang vor Creds-Datei
    athlete_id = args.athlete_id
    api_key = args.api_key
    if not athlete_id or not api_key:
        file_id, file_key = load_creds_file(args.creds_file)
        athlete_id = athlete_id or file_id
        api_key = api_key or file_key

    if not athlete_id or not api_key:
        print(json.dumps({
            "error": "Keine Credentials. Bitte --athlete-id und --api-key angeben "
                     f"oder in {args.creds_file} speichern."
        }))
        sys.exit(1)

    # Datumsbereich bestimmen
    today = date.today()
    if args.date:
        oldest = newest = args.date
    elif args.days:
        oldest = (today - timedelta(days=args.days - 1)).isoformat()
        newest = today.isoformat()
    elif args.oldest and args.newest:
        oldest = args.oldest
        newest = args.newest
    else:
        # Standardmäßig: heute
        oldest = newest = today.isoformat()

    # Aktivitäten abrufen
    raw_activities = fetch_activities(athlete_id, api_key, oldest, newest)

    # Nur Rad-Aktivitäten (außer --all-sports)
    if not args.all_sports:
        raw_activities = [a for a in raw_activities if a.get("type") in CYCLING_TYPES]

    activities = [extract_activity_summary(a) for a in raw_activities]

    # Intervall-Details anreichern
    if args.with_intervals:
        activities = [enrich_with_detail(a, api_key) for a in activities]

    output = {
        "fetched_range": {"oldest": oldest, "newest": newest},
        "activity_count": len(activities),
        "activities": activities,
    }
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
