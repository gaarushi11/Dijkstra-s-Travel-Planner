#include <iostream>
#include <string>
#include "GraphFunctions.h"
#include "FileOperations.h"

using namespace std;

int main() {
    string origin, destination, choice, file;
    cout << "Output File: "; getline(cin, file);
    cout << "Origin: "; getline(cin, origin);
    cout << "Destination: "; getline(cin, destination);
    cout << "Optimize [cheapest/fastest]: "; getline(cin, choice);

    Graph graph;
    graph.routes = routeParser("routes.csv");
    graph.cities = locationParser("cities.csv", graph.routes);

    if (!graph.getCity(origin)) {
        cout << "Origin city not found: " << origin << endl;
        return 1;
    }
    if (!graph.getCity(destination)) {
        cout << "Destination city not found: " << destination << endl;
        return 1;
    }

    graph.DijkstrasFiltered(origin, (choice == "cheapest"));
    outputGenerator(file, graph.cityStacker(destination), graph.routeStacker(destination, (choice == "cheapest")), (choice == "cheapest"));
    
    return 0;
}
