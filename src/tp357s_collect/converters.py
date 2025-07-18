def convert_celsius_to_fahrenheit(temp_c: float):
    return temp_c * 1.8 + 32

def get_heat_index(temp_f: float, hum: int):
    return (
        -42.379 +
        (2.04901523*temp_f) +
        (10.14333127*hum)-
        (.22475541*temp_f*hum) -
        (.00683783*temp_f*temp_f) -
        (.05481717*hum*hum) +
        (.00122874*temp_f*temp_f*hum) +
        (.00085282*temp_f*hum*hum) -
        (.00000199*temp_f*temp_f*hum*hum)
    )
