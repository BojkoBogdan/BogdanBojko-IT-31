import math
import sys

NAME = "Your Name"
SURNAME = "Your Surname"
GROUP = "Your Group"

ROOM_LENGTH = 4.2
ROOM_WIDTH = 3.5
ROOM_HEIGHT = 2.7
DOOR_WIDTH = 0.9
DOOR_HEIGHT = 2.0
WINDOW_WIDTH = 1.4
WINDOW_HEIGHT = 1.5
TILE_WIDTH = 0.30
TILE_LENGTH = 0.30
TILE_PRICE = 42.30


def main():
    print(f"{NAME} {SURNAME}, {GROUP}")
    floor_area = ROOM_LENGTH * ROOM_WIDTH
    wall_area = 2 * (ROOM_LENGTH + ROOM_WIDTH) * ROOM_HEIGHT - DOOR_WIDTH * DOOR_HEIGHT - WINDOW_WIDTH * WINDOW_HEIGHT
    floor_diagonal = math.hypot(ROOM_LENGTH, ROOM_WIDTH)
    room_diagonal = math.dist((0, 0, 0), (ROOM_LENGTH, ROOM_WIDTH, ROOM_HEIGHT))
    tile_area = TILE_WIDTH * TILE_LENGTH
    tiles_exact = floor_area / tile_area
    tiles_round = round(tiles_exact)
    tiles_floor = math.floor(tiles_exact)
    tiles_ceil = math.ceil(tiles_exact)
    tiles_to_buy = math.ceil(tiles_exact * 1.10)
    paint_liters = wall_area / 10 * 2
    paint_cans = math.ceil(paint_liters / 2.5)
    cost_mul = tiles_to_buy * TILE_PRICE
    cost_sum = math.fsum([TILE_PRICE for _ in range(tiles_to_buy)])

    print(f"room:          {ROOM_LENGTH} x {ROOM_WIDTH} x {ROOM_HEIGHT} m")
    print(f"floor area:    {floor_area:.2f} m2")
    print(f"wall area:     {wall_area:.2f} m2 (without door and window)")
    print(f"floor diag:    {floor_diagonal:.2f} m")
    print(f"room diag:     {room_diagonal:.2f} m")
    print(f"\ntiles exact:   {tiles_exact:.2f}")
    print(f"  round:       {tiles_round}")
    print(f"  floor:       {tiles_floor}")
    print(f"  ceil:        {tiles_ceil}")
    print(f"tiles to buy:  {tiles_to_buy} (+10% spare)")
    print(f"paint:         {paint_liters:.2f} l -> {paint_cans} cans of 2.5 l")
    print(f"\ntiles cost:    {cost_mul:.2f} UAH")
    print(f"sum == mul:    {cost_sum == cost_mul}")
    print(f"isclose:       {math.isclose(cost_sum, cost_mul)}")
    print(f"difference:    {abs(cost_sum - cost_mul)}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
