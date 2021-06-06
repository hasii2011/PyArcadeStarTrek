from logging import Logger
from logging import getLogger

from arcade import Sprite

from pytrek.gui.gamepieces.GamePiece import GamePiece
from pytrek.gui.gamepieces.PlanetType import PlanetType

from pytrek.engine.ArcadePoint import ArcadePoint

from pytrek.LocateResources import LocateResources

from pytrek.model.Coordinates import Coordinates


class Planet(Sprite):

    def __init__(self, planetType: PlanetType, sectorCoordinates: Coordinates):

        self.logger: Logger = getLogger(__name__)

        bareFileName: str = f'{planetType.value}.png'
        fqFileName: str = LocateResources.getResourcesPath(resourcePackageName=LocateResources.IMAGE_RESOURCES_PACKAGE_NAME, bareFileName=f'{bareFileName}')

        super().__init__(filename=fqFileName, scale=0.35)

        # Compute these once since planets don't move
        arcadePoint: ArcadePoint = GamePiece.gamePositionToScreenPosition(sectorCoordinates)

        self.center_x = arcadePoint.x
        self.center_y = arcadePoint.y

        self._type: PlanetType = planetType
        self._id:   str        = f'{self._type.value} type planet'

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return self.id

    def __str__(self) -> str:
        return self.__str__()
