import googlemaps
from itertools import permutations
import collections

import re

gmaps = googlemaps.Client("AIzaSyBZXViMj-misldj7YixUXBVYbH6qC8OSJs")

drivers = ["142 Langdon St","2210 University Ave","313 N Frances St, Madison"]
driver_space = [3,4,3]
riders = ["45 Lathrop St., Madison","527 W Mifflin St","1022 W Johnson Street","110 N Brooks Street","432 W Gorham St","633 N Henry St., Madison","107 N Randall Ave","1022 W Johnson St","257 Langdon St","217 N Bassett Street"]
finalDestination="Nielsen Tennis Stadium"
ridersDict = collections.defaultdict(dict)
driverToRiderDict = collections.defaultdict(dict)
riderToDest = {}

def getTime(origin, destination):
    directions = gmaps.directions(origin, destination)
    time = int(re.search(r'\d+', directions[0]['legs'][0]['duration']['text']).group())
    return time


for rider in range(len(riders)):
    for n in range(len(riders)):
        if rider == n:
            continue
        ridersDict[riders[rider]][riders[n]] = getTime(riders[rider],riders[n])

for driver in range(len(drivers)):
    for rider in range(len(riders)):
        driverToRiderDict[drivers[driver]][riders[rider]] = getTime(drivers[driver], riders[rider])

for rider in range(len(riders)):
    riderToDest[riders[rider]] = getTime(riders[rider],finalDestination)




temp_list = []
permDict = {}
spaceCount = 0
routeTimes = {}
route = []




for space in driver_space:
    spaceCount+=1
    if space in temp_list:
        currentPerm = permDict[space]
    else:
        perms = list(permutations(riders,space))#Creates list of permutations each of length space
        temp_list.append(space)                             #Adds space to temp list so no repeat
        permDict[space] = perms                           #creates a dict of space to perms
        currentPerm = permDict[space]          #gets the current perm, which might not have been created this loop

    for perm in currentPerm:
        time = 0
        routeString = ""
        routeString = routeString + drivers[spaceCount -1] + "|"
        for x in range(len(perm)-1):
            time = time + ridersDict[perm[x]][perm[x + 1]]
            routeString = routeString + perm[x] + "|"
        routeString = routeString + perm[len(perm)-1]
        time = time + driverToRiderDict[drivers[spaceCount - 1]][perm[0]]
        time = time + riderToDest[perm[-1]]
        routeTimes[routeString] = time

routeTimesSorted = {k: v for k, v in sorted(routeTimes.items(), key=lambda item: item[1])}



fastestRoute = []

acceptedRoutes = {}
used_places = []


def getRoutes():
    for route in routeTimesSorted.keys():
        used_places.clear()
        acceptedRoutes.clear()
        driverCount = 1
        fastestRoute = route.split("|")
        for place in fastestRoute:
            used_places.append(place)
        acceptedRoutes[route] = routeTimesSorted[route]
        for nextRoute in routeTimesSorted.keys():
            find = False
            for location in used_places:
                if location in nextRoute:
                    find = True
                    break
            if find:
                continue
            for place in nextRoute.split("|"):
                used_places.append(place)
            driverCount = driverCount + 1
            acceptedRoutes[nextRoute] = routeTimesSorted[nextRoute]
            if (driverCount == len(drivers)):
                return (used_places, acceptedRoutes)


print(getRoutes())


