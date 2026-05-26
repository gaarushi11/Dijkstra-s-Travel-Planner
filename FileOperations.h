#ifndef FILEOPERATIONS_H
#define FILEOPERATIONS_H
#include <iomanip>
#include <cstdlib>
#include <string>
#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <stack>
#include <algorithm>

#include "Location.h"
#include "Route.h"

using namespace std;

class Route; 

inline string removeQuotes(string s){
    if(!s.empty() && s[0] == '"'){
        s.erase(0,1);
    }
    if(!s.empty() && s[s.length()-1] == '"'){
        s.erase(s.length()-1,1);
    }
    return s;
}

inline string formatCurrency(float value){
    ostringstream stream;
    stream << fixed << setprecision(2) << value;
    return stream.str();
}

inline vector<Location*> locationParser(string filename, vector<Route*> routes){
    ifstream locations(filename.c_str());
    if(!locations.is_open()){
        cout << "Cities file failed to open\n";
        return {};
    }

    string country, city, latitude, longitude;
    vector<Location*> cities;
    Location* node;

    while(getline(locations, country, ',')){
        getline(locations, city, ',');
        getline(locations, latitude, ',');
        getline(locations, longitude);

        country = removeQuotes(country);
        city = removeQuotes(city);
        latitude = removeQuotes(latitude);
        longitude = removeQuotes(longitude);

        node = new Location(country, city, atof(latitude.c_str()), atof(longitude.c_str()));
        vector<Route*>::iterator it = routes.begin();

        while(it != routes.end()){
            if((*it)->originS.compare(node->capital) == 0){
                (*it)->origin = node;
                node->routes.push_back((*it));
            }
            else if((*it)->destinationS.compare(node->capital) == 0){
                (*it)->destination = node;
            }
            ++it;
        }
        cities.push_back(node);
    }

    cout << "Cities Parsed from: " << filename << endl;
    return cities;
}

inline vector<Route*> routeParser(string filename){
    ifstream routes(filename.c_str());
    if(!routes.is_open()){
        cout << "Routes file failed to open\n";
        return {};
    }

    string originS, destinationS, type, time, cost, note;
    Location* origin = new Location();
    Location* destination = new Location();
    vector<Route*> allRoutes;
    Route* edge;

    while(getline(routes, originS, ',')){
        getline(routes, destinationS, ',');
        getline(routes, type, ',');
        getline(routes, time, ',');
        getline(routes, cost, ',');
        getline(routes, note);

        originS = removeQuotes(originS);
        destinationS = removeQuotes(destinationS);
        type = removeQuotes(type);
        time = removeQuotes(time);
        cost = removeQuotes(cost);
        note = removeQuotes(note);

        edge = new Route(origin, destination, type, atof(time.c_str()), atof(cost.c_str()), note);
        edge->destinationS = destinationS;
        edge->originS = originS;

        allRoutes.push_back(edge);
    }

    cout << "Routes Parsed from: " << filename << endl;
    return allRoutes;
}

/*
Generate Dynamic HTML Map Output with Synchronized Colors & Travel Planner Panel
*/
inline void outputGenerator(string filename,
                            stack<Location*> cities,
                            stack<Route*> routes,
                            bool costOrTime){

    ofstream output(filename.c_str());
    if(!output.is_open()) return;

    vector<Location*> cVec;
    vector<Route*> rVec;

    while(!cities.empty()) { cVec.push_back(cities.top()); cities.pop(); }
    while(!routes.empty()) { rVec.push_back(routes.top()); routes.pop(); }

    reverse(cVec.begin(), cVec.end());
    reverse(rVec.begin(), rVec.end());

    // Calculate total layout summary statistics
    float totalTime = 0;
    float totalCost = 0;
    for(size_t i = 0; i < rVec.size(); ++i) {
        totalTime += rVec[i]->time;
        totalCost += (rVec[i]->transport == "plane") ? (rVec[i]->cost / MULTI) : rVec[i]->cost;
    }

    output
    << "<!DOCTYPE html>\n<html>\n<head>\n<title>Global Travel Planner</title>\n"
    << "<meta charset='utf-8'>\n"
    << "<style>\n"
    << "  html, body { height: 100%; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; overflow: hidden; }\n"
    << "  #container { display: flex; height: 100%; width: 100%; }\n"
    << "  #sidebar { width: 360px; background: #ffffff; box-shadow: 3px 0 10px rgba(0,0,0,0.15); z-index: 10; display: flex; flex-direction: column; }\n"
    << "  #map { flex: 1; height: 100%; }\n"
    << "  .header { padding: 20px; background: #1a73e8; color: white; }\n"
    << "  .header h2 { margin: 0 0 10px 0; font-size: 22px; font-weight: 600; letter-spacing: -0.5px; }\n"
    << "  .route-mode { margin-bottom: 10px; font-size: 13px; font-weight: 500; opacity: 0.95; }\n"
    << "  .summary-stats { font-size: 14px; opacity: 0.9; }\n"
    << "  .route-list { flex: 1; overflow-y: auto; padding: 15px; background: #f8f9fa; }\n"
    << "  .step-card { background: white; border: 1px solid #e0e0e0; border-radius: 6px; padding: 12px; margin-bottom: 10px; cursor: pointer; transition: all 0.2s; }\n"
    << "  .step-card:hover { border-color: #1a73e8; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }\n"
    << "  .step-title { font-weight: bold; color: #202124; font-size: 14px; margin-bottom: 6px; }\n"
    << "  .step-details { font-size: 12px; color: #5f6368; line-height: 1.5; }\n"
    << "  .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; color: white; text-transform: uppercase; margin-bottom: 6px; }\n"
    << "</style>\n"
    << "<script type='text/javascript' src='https://maps.googleapis.com/maps/api/js'></script>\n"
    << "<script>\n"
    << "  var map, bounds, polylines = [];\n"
    << "  function initialize() { \n"
    << "    var myOptions = { \n"
    << "      zoom: 3, \n"
    << "      center: new google.maps.LatLng(30, 20), \n"
    << "      mapTypeId: google.maps.MapTypeId.ROADMAP\n"
    << "    };\n"
    << "    map = new google.maps.Map(document.getElementById('map'), myOptions);\n"
    << "    bounds = new google.maps.LatLngBounds();\n";

    int markerCount = 0;
    int pathCount = 0;

    if(cVec.size() >= 2 && rVec.size() == cVec.size() - 1) {
        for(size_t i = 0; i < rVec.size(); ++i) {
            Location* origin = cVec[i];
            Location* destination = cVec[i+1];
            Route* route = rVec[i];

            float adjustedCost = (route->transport == "plane") ? (route->cost / MULTI) : route->cost;

            // Generate map pins
            output
            << "    var p1_" << markerCount << " = new google.maps.LatLng(" << origin->lat << ", " << origin->lon << ");\n"
            << "    bounds.extend(p1_" << markerCount << ");\n"
            << "    new google.maps.Marker({ position: p1_" << markerCount << ", map: map, title: '" << origin->capital << "' });\n";
            markerCount++;

            output
            << "    var p2_" << markerCount << " = new google.maps.LatLng(" << destination->lat << ", " << destination->lon << ");\n"
            << "    bounds.extend(p2_" << markerCount << ");\n"
            << "    if(" << i << " === " << (rVec.size() - 1) << ") { new google.maps.Marker({ position: p2_" << markerCount << ", map: map, title: '" << destination->capital << "' }); }\n";
            markerCount++;

            // FIXED COLOR CODING LOGIC (Perfect Map-to-Badge Match)
            string colorCode = "#FF6600"; // Default: Car / Road Route (Orange)
            if (route->transport == "plane") {
                colorCode = "#4A90E2";    // Flight (Blue)
            } else if (route->transport == "train") {
                colorCode = "#10B981";    // Rail (Emerald Green)
            }

            output
            << "    var path_" << pathCount << " = new google.maps.Polyline({ \n"
            << "      path: [p1_" << (markerCount-2) << ", p2_" << (markerCount-1) << "], \n"
            << "      geodesic: true, \n"
            << "      strokeColor: '" << colorCode << "', \n"
            << "      strokeOpacity: 0.85, \n"
            << "      strokeWeight: 5\n"
            << "    });\n"
            << "    path_" << pathCount << ".setMap(map);\n"
            << "    polylines.push(path_" << pathCount << ");\n"
            
            << "    google.maps.event.addListener(path_" << pathCount << ", 'click', function() { \n"
            << "      highlightStep(" << pathCount << ");\n"
            << "      alert('Segment " << (i+1) << ": " << origin->capital << " -> " << destination->capital << "\\nMode: " << route->transport << "\\nTime: " << route->time << " hrs\\nCost: $" << formatCurrency(adjustedCost) << "');\n"
            << "    });\n";

            pathCount++;
        }
        output << "    map.fitBounds(bounds);\n";
    }

    output
    << "  }\n"
    << "  function highlightStep(index) {\n"
    << "    for(var i=0; i<polylines.length; i++) {\n"
    << "      polylines[i].setOptions({ \n"
    << "        strokeWeight: (i === index ? 8 : 5), \n"
    << "        strokeOpacity: (i === index ? 1.0 : 0.3) \n"
    << "      });\n"
    << "    }\n"
    << "  }\n"
    << "  google.maps.event.addDomListener(window, 'load', initialize);\n"
    << "</script>\n"
    << "</head>\n"
    << "<body>\n"
    << "  <div id='container'>\n"
    << "    <div id='sidebar'>\n"
    
    // UPDATED SIDEBAR TITLE
    << "      <div class='header'>\n"
    << "        <h2>Travel Planner</h2>\n" 
    << "        <div class='route-mode'>Optimized for " << (costOrTime ? "Cheapest Route" : "Fastest Route") << "</div>\n"
    << "        <div class='summary-stats'>\n"
    << "          Total Time: <b>" << totalTime << " hrs</b><br>\n"
    << "          Total Cost: <b>$" << formatCurrency(totalCost) << "</b>\n"
    << "        </div>\n"
    << "      </div>\n"
    << "      <div class='route-list'>\n";

    // Loop through data vectors to output matching synchronized text badges
    if(cVec.size() >= 2 && rVec.size() == cVec.size() - 1) {
        for(size_t i = 0; i < rVec.size(); ++i) {
            float legCost = (rVec[i]->transport == "plane") ? (rVec[i]->cost / MULTI) : rVec[i]->cost;
            
            // Matches the exact hex colors tracking polyline styles above
            string badgeColor = "#FF6600"; 
            if (rVec[i]->transport == "plane") {
                badgeColor = "#4A90E2";
            } else if (rVec[i]->transport == "train") {
                badgeColor = "#10B981";
            }
            
            output
            << "        <div class='step-card' onclick='highlightStep(" << i << ")'>\n"
            << "          <span class='badge' style='background:" << badgeColor << ";'>" << rVec[i]->transport << "</span>\n"
            << "          <div class='step-title'>" << cVec[i]->capital << " &rarr; " << cVec[i+1]->capital << "</div>\n"
            << "          <div class='step-details'>\n"
            << "            Time: " << rVec[i]->time << " hrs | Cost: $" << formatCurrency(legCost) << "<br>\n"
            << "            <i style='font-size:11px; color:#777;'>" << rVec[i]->note << "</i>\n"
            << "          </div>\n"
            << "        </div>\n";
        }
    }

    output
    << "      </div>\n"
    << "    </div>\n"
    << "    <div id='map'></div>\n"
    << "  </div>\n"
    << "</body>\n"
    << "</html>";

    output.close();
    cout << "Output File Generated Successfully with Synced Color Mapping: " << filename << endl;
}

#endif
