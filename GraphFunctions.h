#ifndef GRAPHFUNCTIONS_H
#define GRAPHFUNCTIONS_H
#include <vector>
#include <stack>
#include <queue>
#include "Location.h"
#include "Route.h"

struct QueueNode {
    Location* city;
    float currentWeight;
    bool operator>(const QueueNode& other) const { return currentWeight > other.currentWeight; }
};

class Graph {
public:
    Graph() {}
    vector<Location*> cities;
    vector<Route*> routes;
    Location* getCity(string name) { for (Location* c : cities) if (c->capital == name) return c; return NULL; }

    void DijkstrasFiltered(string startCity, bool chooseCheapest) {
        for (Location* c : cities) { c->lengthFromStart = 999999.0f; c->previous = NULL; }
        Location* start = getCity(startCity);
        if (!start) return;
        priority_queue<QueueNode, vector<QueueNode>, greater<QueueNode>> pq;
        start->lengthFromStart = 0.0f;
        pq.push({start, 0.0f});
        while (!pq.empty()) {
            QueueNode current = pq.top(); pq.pop();
            Location* u = current.city;
            if (current.currentWeight > u->lengthFromStart) continue;
            for (Route* edge : u->routes) {
                Location* v = edge->destination;
                // STRICT: If not cheapest, ALWAYS use time.
                float edgeWeight = chooseCheapest ? (edge->transport == "plane" ? edge->cost/MULTI : edge->cost) : edge->time;
                if (u->lengthFromStart + edgeWeight < v->lengthFromStart) {
                    v->lengthFromStart = u->lengthFromStart + edgeWeight;
                    v->previous = u;
                    pq.push({v, v->lengthFromStart});
                }
            }
        }
    }

    // 1. Corrected City Stacker
    stack<Location*> cityStacker(string destCity) {
        vector<Location*> temp;
        Location* curr = getCity(destCity);
        while (curr) { temp.push_back(curr); curr = curr->previous; }
        
        stack<Location*> s;
        // Push in reverse order so Origin is on top
        for (int i = temp.size() - 1; i >= 0; i--) s.push(temp[i]);
        return s;
    }

    // 2. Corrected Route Stacker
    stack<Route*> routeStacker(string destCity, bool chooseCheapest) {
        vector<Route*> temp;
        Location* curr = getCity(destCity);
        while (curr && curr->previous) {
            Location* prev = curr->previous;
            Route* bestEdge = NULL;
            float bestWeight = 999999.0f;
            for (Route* edge : prev->routes) {
                if (edge->destination == curr) {
                    float weight = chooseCheapest ? (edge->transport == "plane" ? edge->cost/MULTI : edge->cost) : edge->time;
                    if (weight < bestWeight) { bestWeight = weight; bestEdge = edge; }
                }
            }
            if (bestEdge) temp.push_back(bestEdge);
            curr = prev;
        }
        
        stack<Route*> s;
        // Push in reverse order so the first leg is on top
        for (int i = temp.size() - 1; i >= 0; i--) s.push(temp[i]);
        return s;
    }
};
#endif