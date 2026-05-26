#ifndef LOCATION_H
#define LOCATION_H
#include <string>
#include <vector>
using namespace std;
class Route;
class Location {
public:
    string country, capital;
    float lat, lon;
    vector<Route*> routes;
    Location* previous;
    float lengthFromStart;
    Location() : country(""), capital(""), lat(0), lon(0), previous(NULL), lengthFromStart(999999) {}
    Location(string count, string cap, float lt, float lg) 
        : country(count), capital(cap), lat(lt), lon(lg), previous(NULL), lengthFromStart(999999) {}
};
#endif