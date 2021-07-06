
from logging import Logger
from logging import getLogger

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.base.BaseEnemy import BaseEnemy
from pytrek.gui.gamepieces.base.BaseEnemy import EnemyId

from pytrek.model.Coordinates import Coordinates


class SuperCommander(BaseEnemy):

    FILENAME: str = 'SuperCommander.png'

    def __init__(self, coordinates: Coordinates, moveInterval: int):

        super().__init__(filename=SuperCommander.FILENAME, coordinates=coordinates, moveInterval=moveInterval, scale=0.075)

        self.logger: Logger = getLogger(__name__)

        self.id = EnemyId(f'Commander-{self.gameCoordinates}')

        # Compute at creation;  Mediator will move the commander
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(coordinates)

        self.center_x = arcadePoint.x
        self.center_y = arcadePoint.y

    def __str__(self):

        lookAtMe: str = f'{self.id}'

        return lookAtMe

    def __repr__(self):

        devMe: str = (
            f'Commander['
            f'id={self.id} '
            f'power={self.power:.3f} '
            f'moveInterval={self.moveInterval} '
            f'timeSinceMovement={self.timeSinceMovement} '
            f'currentPosition={self.gameCoordinates}'
            ']'
        )

        return devMe
