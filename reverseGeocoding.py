from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")
location = geolocator.reverse("-35.846261, -71.582636") ##  -35.8461069,-71.5854832
addressLocation = location.address.split(',')
print("Estas en la calle " + addressLocation[0])
print(location.address)