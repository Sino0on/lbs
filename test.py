import requests

start_place = '42.875491,74.632649'
end_place = '43.253385,76.900547'
url = f'http://router.project-osrm.org/route/v1/driving/42.875491,74.632649;42.649861,77.057086?steps=true&geometries=geojson&overview=full'
response = requests.get(url=url)
print(response.json()['routes'])
