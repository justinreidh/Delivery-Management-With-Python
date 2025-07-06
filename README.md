# Delivery Management with Python
This Python program simulates a package delivery system using two trucks. It uses a nearest neighbor algorithm to optimize delivery routes and allows the user to view package statuses and delivery times at various points during the day.

## Project Overview
This project includes:

A custom-built hash table for package storage and lookup, using chaining for collision resolution.

Trucks find and deliver packages using a Neirest Neighbor algorithm.

Dynamic time-based status queries for individual or all packages, and simulating time based on a constant assumed truck speed (18 mph).

A console-based menu system for user interaction.

## Running the Program
Open a terminal in the project directory and run:

python main.py

You'll see a menu with the following options:

1. View total mileage and all package statuses by end of day.

2. View package statuses at a specific time.

3. Lookup a specific package at a specific time.

4. Exit.
