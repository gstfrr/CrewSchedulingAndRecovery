from datetime import datetime, timedelta
import pandas as pd

from Domain import Pairing


def generate_pairings(flights, max_duty_time_hours=10):
    max_duty_time = timedelta(hours=max_duty_time_hours)

    # Generate initial pairings
    pairings = []
    for flight in flights:
        new_pairing = Pairing()
        new_pairing.add_flight(flight)
        pairings.append(new_pairing)

    # Combine flights into pairings
    for i in range(len(pairings)):
        for j in range(i + 1, len(pairings)):
            if pairings[i].is_legal(max_duty_time) and pairings[j].is_legal(max_duty_time):
                combined_pairing = Pairing()
                combined_pairing.flights = pairings[i].flights + pairings[j].flights
                combined_pairing.total_duty_time = pairings[i].total_duty_time + pairings[j].total_duty_time
                if combined_pairing.is_legal(max_duty_time):
                    pairings.append(combined_pairing)

    # Filter out illegal pairings
    pairings = [pairing for pairing in pairings if pairing.is_legal(max_duty_time)]
    pairings.sort(key=lambda x: len(x.flights))

    # Prepare data for Excel
    pairings_data = []
    for idx, pairing in enumerate(pairings):
        for flight in pairing.flights:
            pairings_data.append({
                "Pairing": idx + 1,
                "Flight": flight.name,
                "Departure Airport": flight.origin,
                "Arrival Airport": flight.destination,
                "Departure": flight.start.strftime('%H:%M'),
                "Arrival": flight.end.strftime('%H:%M'),
                "Total Duty Time": str(pairing.total_duty_time)
            })

    # Convert the data into a DataFrame
    df_pairings = pd.DataFrame(pairings_data)

    for i, p in enumerate(pairings):
        p.name = i

    # Save the DataFrame to an Excel file
    excel_file_path = "instances/pairings_generated.xlsx"
    df_pairings.to_excel(excel_file_path, index=False)

    print(f"Pairings saved to: {excel_file_path}")
    return pairings
