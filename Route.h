#ifndef ROUTE_H
#define ROUTE_H
#include <string>
using namespace std;
class Location;
const float MULTI = 3.0f;
class Route {
public:
    Location *origin, *destination;
    string originS, destinationS, transport, note;
    float time, cost;
    Route() : origin(NULL), destination(NULL), transport(""), time(0), cost(0), note("") {}
    Route(Location* org, Location* dest, string trans, float tim, float cst, string notee)
        : origin(org), destination(dest), transport(trans), time(tim), cost(cst), note(notee) {}
};
#endif