
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from arcade import Sound
from arcade import Sprite
from arcade import SpriteList
from arcade import check_for_collision_with_list

from pytrek.Constants import SOUND_VOLUME_HIGH
from pytrek.LocateResources import LocateResources
from pytrek.engine.ArcadePosition import ArcadePosition
from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.gui.gamepieces.Enterprise import Enterprise
from pytrek.gui.gamepieces.GamePieceTypes import KlingonId

from pytrek.gui.gamepieces.Klingon import Klingon
from pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from pytrek.gui.gamepieces.KlingonTorpedoFollower import KlingonTorpedoFollower

from pytrek.model.Quadrant import Quadrant


class KlingonTorpedoHandler:

    KLINGON_TORPEDO_EVENT_SECONDS = 10      # TODO  Compute this

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

        self._gameEngine: GameEngine = GameEngine()
        self._computer:   Computer   = Computer()

        self._klingonTorpedoes: SpriteList = cast(SpriteList, None)
        self._torpedoFollowers: SpriteList = cast(SpriteList, None)

        fqFileName = LocateResources.getResourcesPath(resourcePackageName=LocateResources.SOUND_RESOURCES_PACKAGE_NAME,
                                                      bareFileName='klingon_torpedo.wav')
        self._soundKlingonTorpedo: Sound = Sound(file_name=fqFileName)

        self._lastTimeCheck: float = self._gameEngine.gameClock / 1000
        self.logger.info(f'{self._lastTimeCheck=}')

    @property
    def klingonTorpedoes(self) -> SpriteList:
        return self._klingonTorpedoes

    @klingonTorpedoes.setter
    def klingonTorpedoes(self, newList: SpriteList):
        """
        Args:
            newList:
        """
        self._klingonTorpedoes = newList

    @property
    def torpedoFollowers(self) -> SpriteList:
        return self._torpedoFollowers

    @torpedoFollowers.setter
    def torpedoFollowers(self, newValues: SpriteList):
        self._torpedoFollowers = newValues

    @property
    def klingonList(self) -> SpriteList:
        return self._klingonList

    @klingonList.setter
    def klingonList(self, newValues: SpriteList):
        self._klingonList = newValues

    def fireTorpedoesAtEnterpriseIfNecessary(self, quadrant: Quadrant):

        currentTime:    float = self._gameEngine.gameClock
        deltaClockTime: float = currentTime - self._lastTimeCheck
        if deltaClockTime > KlingonTorpedoHandler.KLINGON_TORPEDO_EVENT_SECONDS:
            self.logger.info(f'Time for Klingons to fire torpedoes')
            klingons: List[Klingon] = quadrant.klingons
            for klingon in klingons:
                self._fireKlingonTorpedo(klingon=klingon, enterprise=quadrant.enterprise)

            self._lastTimeCheck = currentTime

    def handleKlingonTorpedoHits(self, quadrant: Quadrant):
        """
        For each torpedo use arcade to determine collision

         * Remove it's followers
         * Determine which Klingon fired it
         * Determine how severe of a hit it was
         * Adjust the Enterprise shield power value or the Enterprise power value itself
        Args:
            quadrant:  The current quadrant we are in
        """

        expendedTorpedoes: List[Sprite] = check_for_collision_with_list(sprite=quadrant.enterprise, sprite_list=self.klingonTorpedoes)
        for expendedTorpedo in expendedTorpedoes:
            expendedTorpedo: KlingonTorpedo = cast(KlingonTorpedo, expendedTorpedo)
            self.logger.info(f'{expendedTorpedo.uuid} arrived at destination')
            self._removeTorpedoFollowers(klingonTorpedo=expendedTorpedo)

            firedBy: KlingonId = expendedTorpedo.firedBy
            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)

            hitValue: float = self._computer.computeHitValueOnEnterprise(klingonPosition=shootingKlingon.currentPosition,
                                                                         enterprisePosition=quadrant.enterpriseCoordinates,
                                                                         klingonPower=shootingKlingon.power)
            self.logger.info(f'*** Enterprise was hit ***  {hitValue=} {shootingKlingon}')

            expendedTorpedo.remove_from_sprite_lists()

    def handleKlingonTorpedoMisses(self):

        torpedoDuds: List[KlingonTorpedo] = self._findTorpedoMisses()

        for torpedoDud in torpedoDuds:
            self._removeTorpedoFollowers(klingonTorpedo=torpedoDud)

            firedBy: KlingonId = torpedoDud.firedBy

            shootingKlingon: Klingon = self._findFiringKlingon(klingonId=firedBy)
            self.logger.info(f'{shootingKlingon} missed !!!!')
            torpedoDud.remove_from_sprite_lists()

    def _fireKlingonTorpedo(self, klingon: Klingon, enterprise: Enterprise):

        self.logger.info(f'Klingon @ {klingon.currentPosition} firing; Enterprise @ {enterprise.currentPosition}')

        #
        # Use the enterprise arcade position rather than compute the sector center;  That way we
        # can use Arcade collision detection
        #
        klingonPoint:    ArcadePosition = Computer.gamePositionToScreenPosition(gameCoordinates=klingon.currentPosition)
        enterprisePoint: ArcadePosition = ArcadePosition(x=enterprise.center_x, y=enterprise.center_y)

        klingonTorpedo: KlingonTorpedo = KlingonTorpedo()
        klingonTorpedo.center_x = klingonPoint.x
        klingonTorpedo.center_y = klingonPoint.y
        klingonTorpedo.inMotion = True
        klingonTorpedo.destinationPoint  = enterprisePoint
        klingonTorpedo.firedFromPosition = klingon.currentPosition
        klingonTorpedo.firedBy           = klingon.id
        klingonTorpedo.followers         = self.torpedoFollowers

        self.klingonTorpedoes.append(klingonTorpedo)
        self._soundKlingonTorpedo.play(volume=SOUND_VOLUME_HIGH)
        self.logger.info(f'{klingonTorpedo.firedFromPosition=}')

    def _removeTorpedoFollowers(self, klingonTorpedo: KlingonTorpedo):

        followersToRemove: List[Sprite] = []
        for follower in self.torpedoFollowers:
            follower: KlingonTorpedoFollower = cast(KlingonTorpedoFollower, follower)
            if follower.following == klingonTorpedo.uuid:
                self.logger.debug(f'Removing follower: {follower.uuid}')
                followersToRemove.append(follower)

        for followerToRemove in followersToRemove:
            followerToRemove.remove_from_sprite_lists()

    def _findFiringKlingon(self, klingonId: KlingonId) -> Klingon:

        fndKlingon: Klingon = cast(Klingon, None)
        for klingon in self._klingonList:
            klingon: Klingon = cast(Klingon, klingon)
            if klingon.id == klingonId:
                fndKlingon = klingon
                break

        return fndKlingon

    def _findTorpedoMisses(self):

        torpedoDuds: List[KlingonTorpedo] = []
        for torpedo in self.klingonTorpedoes:
            torpedo: KlingonTorpedo = cast(KlingonTorpedo, torpedo)
            if torpedo.inMotion is False:
                torpedoDuds.append(torpedo)
        return torpedoDuds
