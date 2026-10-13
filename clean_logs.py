"""Clean a corrupted remote weather station log and export it as a CSV."""

INPUT_FILE = "environmental_raw.txt"
OUTPUT_FILE = "environmental_clean.csv"


def celsius_converter(f_temp):
    """Convert a Fahrenheit string/float to Celsius, rounded to 2 decimals."""
    return round((float(f_temp) - 32) * 5 / 9, 2)


def parse_and_clean(line):
    """Parse one raw log line.

    Returns a list [timestamp, station_id, temp_f, humidity, status]
    for a valid line, or None if the line is corrupted or the
    sensor status is anything other than ACTIVE.
    """
    line = line.strip()
    if not line:  # blank line
        return None

    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 5:  # missing delimiter(s)
        return None

    timestamp, station_id, temp, humidity, status = parts

    # Any empty field means missing data
    if not all(parts):
        return None

    # Only ACTIVE readings are kept
    if status != "ACTIVE":
        return None

    # Temperature must be a real number (rejects ERROR, N/A, the header row)
    try:
        float(temp)
        float(humidity)
    except ValueError:
        return None

    return [timestamp, station_id, temp, humidity, status]


def main():
    skipped = 0
    kept = 0

    with open(INPUT_FILE, "r") as infile, open(OUTPUT_FILE, "w") as outfile:
        outfile.write("Timestamp,StationID,Temp(C),Humidity(%),Sensor_Status\n")

        for line in infile:  # line-by-line, never loads the whole file
            row = parse_and_clean(line)
            if row is None:
                skipped += 1
                continue

            timestamp, station_id, temp_f, humidity, status = row
            temp_c = celsius_converter(temp_f)
            outfile.write(f"{timestamp},{station_id},{temp_c},{humidity},{status}\n")
            kept += 1

    print(f"Valid rows written: {kept}")
    print(f"Corrupted lines skipped: {skipped}")


if __name__ == "__main__":
    main()

