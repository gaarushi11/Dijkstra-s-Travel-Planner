# Dijkstra-s-Travel-Planner

A travel route optimization project built using **Dijkstra’s Algorithm** that helps users find the best route between two cities based on their preferences. The system supports multiple transportation modes and calculates either the **shortest** or the **most cost-effective** journey.

# Project Features

* Takes **source** and **destination** cities as input
* Provides route planning using:
  * ✈️ Flights
  * 🚆 Trains
  * 🚗 Cars
  * 🚌 Buses
    
* Allows users to choose between:
  * **Shortest Path**
  * **Cheapest Path**
    
* Displays:
  * Complete travel route
  * Names of intermediate stops/cities
  * Total journey cost
  * Total travel time

# Algorithm Used

The project uses **Dijkstra’s Shortest Path Algorithm** on a weighted graph:

* Cities are represented as **nodes**
* Transport connections are represented as **edges**
* Edge weights depend on:
  * Distance/Time
  * Cost

Based on user preference, the algorithm computes the most optimized route efficiently.

# Technologies Used

* C++, Python, Java, HTML, CSS
* Graph Data Structure
* Priority Queue/Min Heap
* Dijkstra’s Algorithm

# Objective

The aim of this project is to demonstrate how graph algorithms can be applied in real-world travel and transportation systems to improve route planning and decision-making.

# Possible Future Enhancements

* Real-time fare and traffic update
* Graphical User Interface (GUI)
* Interactive map integration
* Hotel and stay recommendations
* Multi-city travel planning
* User authentication and saved trips
