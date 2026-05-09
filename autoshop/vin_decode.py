from functools import lru_cache

import requests


VIN_FIELDS = {
    "Model Year": "year",
    "Make": "make",
    "Model": "model",
    "Drive Type": "drive_type",
    "Engine Number of Cylinders": "engine_cylinders",
}


def _normalize_vin(vin: str) -> str:
    return (vin or "").strip().upper()


@lru_cache(maxsize=512)
def decode_vin(vin: str):
    normalized_vin = _normalize_vin(vin)
    if len(normalized_vin) != 17:
        return {"error": "VIN must be 17 characters long."}

    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{normalized_vin}?format=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("Results", [])

        vehicle_info = {value: "" for value in VIN_FIELDS.values()}
        for item in results:
            variable = item.get("Variable")
            value = item.get("Value")
            field_name = VIN_FIELDS.get(variable)
            if field_name and value not in (None, "", "Not Applicable"):
                vehicle_info[field_name] = str(value).strip()

        vehicle_info["vin"] = normalized_vin
        return vehicle_info
    except requests.RequestException as exc:
        return {"error": f"Request failed: {exc}"}
    except ValueError:
        return {"error": "VIN service returned an invalid response."}


if __name__ == "__main__":
    vin_to_check = input("Enter the VIN to decode: ")
    print(decode_vin(vin_to_check))
