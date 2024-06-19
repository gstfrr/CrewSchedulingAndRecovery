from datetime import timedelta
import pandas as pd

from Domain import Pairing


def generate_pairings(flights, max_duty_time_hours: float = 500) -> list[Pairing]:
    """

    :param flights: 
    :param max_duty_time_hours: float:  (Default value = 10)

    """
    max_duty_time = timedelta(hours=max_duty_time_hours)

    # Generate initial pairings
    pairings = []

    def find_valid_pairings(current_pairing):
        if current_pairing.total_duty_time > max_duty_time:
            return

        if len(current_pairing.flights) >= 2:
            pairings.append(current_pairing)

        last_airport = current_pairing.flights[-1].destination
        last_end_time = current_pairing.flights[-1].end

        for flight in flights:
            if flight.origin == last_airport and flight.start >= last_end_time + timedelta(minutes=30) and flight.start <= last_end_time + timedelta(hours=10):
                new_pairing = Pairing()
                new_pairing.flights = current_pairing.flights + [flight]
                new_pairing.total_duty_time = current_pairing.total_duty_time + (flight.start - last_end_time) + (
                    flight.end - flight.start)
                find_valid_pairings(new_pairing)

    for flight in flights:
        initial_pairing = Pairing()
        initial_pairing.add_flight(flight)
        find_valid_pairings(initial_pairing)

    # Filter out illegal pairings and pairings with only one flight
    pairings = [pairing for pairing in pairings if pairing.is_legal(
        max_duty_time) and len(pairing.flights) > 1]

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
