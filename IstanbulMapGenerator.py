#!/usr/bin/env python3
import argparse, random, sys

FOUNTAIN = 7
BLACK_MARKET = 8
TEA_HOUSE = 9

class IstanbulMap():
    def __init__(self, game_version):
        if game_version.upper() == 'ORIGINAL':
            self.game_version = 'Original'
            self.map_size = 16
            self.num_col = 4
            self.acceptable_fountain_positions = [5, 6, 9, 10]
        elif game_version.upper() == 'MOCHA_BAKSHEESH':
            self.game_version = 'Mocha & Baksheesh'
            self.map_size = 20
            self.num_col = 5
            self.acceptable_fountain_positions = [6, 7, 8, 11, 12, 13]
        self.tiles = list(random.sample(range(1,self.map_size + 1), self.map_size))
        self.enforce_fountain_rule()
        self.enforce_black_market_tea_house_rule()

    def get_x_coordinate(self, index):
        return index % self.num_col + 1

    def get_y_coordinate(self, index):
        return index / self.num_col + 1

    def get_distance(self, first_index, second_index):
        delta_x = self.get_x_coordinate(second_index) - self.get_x_coordinate(first_index)
        delta_y = self.get_y_coordinate(second_index) - self.get_y_coordinate(first_index)
        return abs(delta_x) + abs(delta_y)

    def enforce_fountain_rule(self):
        index_fountain = self.tiles.index(FOUNTAIN)
        if index_fountain not in self.acceptable_fountain_positions:
            new_index_fountain = random.choice(self.acceptable_fountain_positions)
            self.tiles[index_fountain], self.tiles[new_index_fountain] = self.tiles[new_index_fountain], self.tiles[index_fountain]

    def enforce_black_market_tea_house_rule(self):
        index_black_market = self.tiles.index(BLACK_MARKET)
        index_tea_house = self.tiles.index(TEA_HOUSE)
        while (self.get_distance(index_black_market, index_tea_house) < 3):
            new_index = random.randint(0, self.map_size - 1)
            if (self.tiles[new_index] not in (FOUNTAIN,TEA_HOUSE)):
                self.tiles[index_black_market], self.tiles[new_index] = self.tiles[new_index], self.tiles[index_black_market]
            index_black_market = self.tiles.index(BLACK_MARKET);
            index_tea_house = self.tiles.index(TEA_HOUSE);

    def get_row(self, row_num):
        first_index = 0+row_num*self.num_col
        last_index = self.num_col+row_num*self.num_col
        for tile in self.tiles[first_index:last_index]:
            yield str(tile)

    def get_rows(self):
        for row_num in range(int(self.map_size/self.num_col)):
            yield self.get_row(row_num)

    def printMap(self, output=sys.stdout):
        print('Istanbul Map {}'.format(self.game_version), file=output)
        for row in self.get_rows():
            print(*row,sep='\t',file=output)

parser = argparse.ArgumentParser()
parser.add_argument("game_version", default='O', nargs='?')
parser.add_argument('-o', '--output', type=argparse.FileType('w'))
args = parser.parse_args()
v = args.game_version
if v.upper() == 'O':
    im = IstanbulMap('ORIGINAL')
    im.printMap(output=args.output)
elif v.upper() == 'M':
    im = IstanbulMap('MOCHA_BAKSHEESH')
    im.printMap(output=args.output)
