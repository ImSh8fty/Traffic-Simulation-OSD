from enum import Enum, auto
from abc import ABC, abstractmethod

# Constants Definition
class Constants:
    AccRate = 3.5
    AccRateEmpty = 2.5
    AccRateFull = 1.0
    DecRate = 7.0
    DecRateEmpty = 5.0
    DecRateFull = 2.0
    MpsToMph = 2.237
    MpsToKph = 3.6
    MetersToMiles = 0.000621371
    MetersToKm = 0.001
    CharMapSize = 40
    WorldSize = 200.0

# Conversion Utility
class Conversions:
    @staticmethod
    def WCpointToCCpoint(val):
        return int(val * (Constants.CharMapSize / Constants.WorldSize) + (Constants.CharMapSize // 2))

    @staticmethod
    def WClengthToCClength(val):
        return int(val * (Constants.CharMapSize / Constants.WorldSize))

# Heading Enum
class Heading(Enum):
    North = auto()
    South = auto()
    East = auto()
    West = auto()

# GUI Abstract Class
class GUI(ABC):
    @abstractmethod
    def create_road(self, name, locx, locy, len, hdg):
        pass

# MetricGUI Implementation
class MetricGUI(GUI):
    def create_road(self, name, locx, locy, len, hdg):
        return Road(name, locx / Constants.MetersToKm, locy / Constants.MetersToKm, len / Constants.MetersToKm, hdg)

# ImperialGUI Implementation - Not used in main, but implemented for completeness
class ImperialGUI(GUI):
    def create_road(self, name, locx, locy, len, hdg):
        return Road(name, locx / Constants.MetersToMiles, locy / Constants.MetersToMiles, len / Constants.MetersToMiles, hdg)

# Map Class
class Map:
    def __init__(self):
        self.roads = []

    def add_road(self, road):
        self.roads.append(road)

# Road Class
class Road:
    NumOfRoads = 0

    def __init__(self, name, locX, locY, length, heading):
        self.name = name
        self.length = length
        self.xlocation = locX
        self.ylocation = locY
        self.heading = heading
        Road.NumOfRoads += 1

# CharMatrix Class for Display
class CharMatrix:
    def __init__(self):
        self.map = [[' ' for _ in range(Constants.CharMapSize)] for _ in range(Constants.CharMapSize)]

# Print Driver Interface
class IPrintDriver(ABC):
    @abstractmethod
    def PrintRoad(self, road, char_matrix):
        pass

# ConsolePrint Class for Console Output
class ConsolePrint(IPrintDriver):
    def PrintRoad(self, road, char_matrix):
        CCx = Conversions.WCpointToCCpoint(road.xlocation)
        CCy = Conversions.WCpointToCCpoint(-road.ylocation)
        CCRoadLength = Conversions.WClengthToCClength(road.length)

        if road.heading == Heading.North or road.heading == Heading.South:
            for i in range(-CCRoadLength//2, CCRoadLength//2, 1):
                y = CCy + i
                for offset in [-1, 0, 1]:  # Three vertical lines
                    if 0 <= y < Constants.CharMapSize and (i % 2 == 0):
                        char_matrix.map[y][CCx + offset] = '|'
        elif road.heading == Heading.East or road.heading == Heading.West:
            for i in range(-CCRoadLength//2, CCRoadLength//2, 1):
                x = CCx + i
                for offset in [-1, 0, 1]:  # Three horizontal lines
                    if 0 <= x < Constants.CharMapSize and (i % 2 == 0):
                        char_matrix.map[CCy + offset][x] = '-'

# Main Program Execution
def main():
    sim_input = MetricGUI()
    my_map = Map()

    # Create two roads: "Uptown" and "Crosstown" at the center of the map
    uptown = sim_input.create_road("Uptown", 0.0, 0.0, 200.0, Heading.North)
    crosstown = sim_input.create_road("Crosstown", 0.0, 0.0, 200.0, Heading.East)

    my_map.add_road(uptown)
    my_map.add_road(crosstown)

    # Initialize CharMatrix and ConsolePrint for drawing the map
    char_matrix = CharMatrix()
    console_print = ConsolePrint()

    # Draw the roads on the character matrix
    for road in my_map.roads:
        console_print.PrintRoad(road, char_matrix)

    # Print the character matrix to the console
    for row in char_matrix.map:
        print(''.join(row))

if __name__ == "__main__":
    main()
