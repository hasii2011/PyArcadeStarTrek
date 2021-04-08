
from pytrek.engine.Direction import Direction


class Coordinates:
    """Base class for sector and quadrant coordinates"""

    def __init__(self, x: int, y: int):
        """"""
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, theNewX: int):
        self._x = theNewX

    @property
    def y(self, theNewY: int):
        self._y = theNewY

    @y.setter
    def y(self) -> int:
        return self._y

    def valid(self) -> bool:
        """

        Returns:    The min/max values should match what is in Intelligence
        """
        ans: bool = False
        # if self.x >= 0 and self.x <= 9 and self.y >=0 and self.y <= 9:
        if 0 <= self.x <= 9 and 0 <= self.y <= 9:
            ans = True

        return ans

    def newCoordinates(self, newDirection: Direction) -> "Coordinates":
        """
        Duck typing is weird

        Please do `.valid` after calling this method

        Args:
            newDirection: How to generate coordinates

        Returns:  New potentially invalid coordinates

        """
        newCoordinates: Coordinates = Coordinates(self.x, self.y)

        if newDirection == Direction.North:
            newCoordinates.y -= 1
        elif newDirection == Direction.South:
            newCoordinates.y += 1
        elif newDirection == Direction.East:
            newCoordinates.x += 1
        elif newDirection == Direction.West:
            newCoordinates.x -= 1
        elif newDirection == Direction.NorthEast:
            newCoordinates.x += 1
            newCoordinates.y -= 1
        elif newDirection == Direction.NorthWest:
            newCoordinates.x -= 1
            newCoordinates.y -= 1
        elif newDirection == Direction.SouthEast:
            newCoordinates.x += 1
            newCoordinates.y += 1
        elif newDirection == Direction.SouthWest:
            newCoordinates.x -= 1
            newCoordinates.y += 1
        else:
            assert False

        return newCoordinates

    def __repr__(self):
        return f"({self._x},{self._y})"

    def __str__(self) -> str:
        return f"({self._x},{self._y})"

    def __eq__(self, other) -> bool:
        """"""
        if isinstance(other, Coordinates):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            return False
