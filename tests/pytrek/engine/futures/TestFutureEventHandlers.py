
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pytrek.GameState import GameState

from pytrek.engine.Computer import Computer
from pytrek.engine.GameEngine import GameEngine
from pytrek.engine.Intelligence import Intelligence

from pytrek.model.Coordinates import Coordinates
from pytrek.model.Galaxy import Galaxy
from pytrek.model.Quadrant import Quadrant

from pytrek.settings.GameSettings import GameSettings
from pytrek.settings.SettingsCommon import SettingsCommon

from tests.TestBase import TestBase

from pytrek.engine.futures.FutureEventHandlers import FutureEventHandlers
from tests.pytrek.engine.futures.LogMessageConsole import LogMessageConsole


class TestFutureEventHandlers(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    clsGameSettings: GameSettings = cast(GameSettings, None)
    clsGameState:    GameState    = cast(GameState, None)
    clsGameEngine:   GameEngine   = cast(GameEngine, None)
    clsIntelligence: Intelligence = cast(Intelligence, None)
    clsComputer:     Computer     = cast(Computer, None)
    clsGalaxy:       Galaxy       = cast(Galaxy, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestFutureEventHandlers.clsLogger = getLogger(__name__)
        SettingsCommon.determineSettingsLocation()
        TestFutureEventHandlers._setupGame()
        TestFutureEventHandlers.clsLogger.info(f'Running TestFutureEventHandlers')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestFutureEventHandlers.clsLogger

        self._gameSettings: GameSettings = TestFutureEventHandlers.clsGameSettings
        self._gameState:    GameState    = TestFutureEventHandlers.clsGameState
        self._gameEngine:   GameEngine   = TestFutureEventHandlers.clsGameEngine
        self._intelligence: Intelligence = TestFutureEventHandlers.clsIntelligence
        self._computer:     Computer     = TestFutureEventHandlers.clsComputer
        self._galaxy:       Galaxy       = TestFutureEventHandlers.clsGalaxy

        self._eventHandlers: FutureEventHandlers = FutureEventHandlers(LogMessageConsole())

    def tearDown(self):
        pass

    def testSuperNovaEventHandlerKlingonsAreDead(self):

        quadrant: Quadrant = self._getANovaEventQuadrant()
        self._testEnemyDeadHandler(quadrant=quadrant, enemyName='Klingon')

    def testSuperNovaEventHandlerCommandersAreDead(self):

        quadrant: Quadrant = self._getANovaEventQuadrant()
        self._testEnemyDeadHandler(quadrant=quadrant, enemyName='Commander')

    def testSuperNovaEventHandlerSuperCommandersAreDead(self):

        quadrant: Quadrant = self._getANovaEventQuadrant()
        self._testEnemyDeadHandler(quadrant=quadrant, enemyName='SuperCommander')

    def testSuperNovaEventStarBaseDestroyed(self):

        quadrant:              Quadrant = self._getANovaEventQuadrant()
        previousStarBaseCount: int      = self._gameState.starBaseCount

        self._eventHandlers.superNovaEventHandler(quadrant=quadrant)

        if previousStarBaseCount != 0:
            expectedStarBaseCount: int = previousStarBaseCount - 1
        else:
            expectedStarBaseCount = 0

        actualStarBaseCount: int = self._gameState.starBaseCount

        self.assertEqual(expectedStarBaseCount, actualStarBaseCount, 'StarBase not properly destroyed')

    def testSuperNovaEventPlanetDestroyed(self):

        quadrant:            Quadrant = self._getANovaEventQuadrant()
        previousPlanetCount: int      = self._gameState.planetCount

        self._eventHandlers.superNovaEventHandler(quadrant=quadrant)

        if previousPlanetCount != 0:
            expectedPlanetCount: int = previousPlanetCount - 1
        else:
            expectedPlanetCount = 0

        actualPlanetCount: int = self._gameState.planetCount

        self.assertEqual(expectedPlanetCount, actualPlanetCount, 'Planet not properly destroyed')

    def testSuperNovaEventStarBaseDestroyedNeverNegative(self):
        """
        Destroy all the StarBases and then try one more time
        """

        coordinates: Coordinates = self._galaxy.getStarBaseCoordinates()
        while coordinates is not None:
            quadrant: Quadrant = self._galaxy.getQuadrant(quadrantCoordinates=coordinates)

            self._eventHandlers.superNovaEventHandler(quadrant=quadrant)

            coordinates = self._galaxy.getStarBaseCoordinates()

        self.assertEqual(0, self._gameState.starBaseCount, 'Did not destroy all StarBases')
        coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
        quadrant: Quadrant = Quadrant(coordinates=coordinates)

        self._eventHandlers.superNovaEventHandler(quadrant=quadrant)
        self.assertEqual(0, self._gameState.starBaseCount, 'Should be zero all StarBases destroyed')

    def testTractorBeamEventHandler(self):
        """Another test"""
        pass

    def testCommanderAttacksBaseEventHandler(self):
        """
        """
        self._eventHandlers.commanderAttacksBaseEventHandler()

    def _getANovaEventQuadrant(self) -> Quadrant:
        """
        Returns:
        """

        coordinates: Coordinates = self._intelligence.generateQuadrantCoordinates()
        quadrant:    Quadrant    = Quadrant(coordinates=coordinates)

        self.logger.debug (f'{quadrant.hasSuperNova=}')
        quadrant.addKlingon()
        quadrant.addCommander()
        quadrant.addSuperCommander()

        if quadrant.hasPlanet is False:
            self._gameState.planetCount += 1
            quadrant.addPlanet()
        if quadrant.hasStarBase is False:
            self._gameState.starBaseCount += 1
            quadrant.addStarBase()
        #
        # Update the game state to reflect what I did here
        #
        self._gameState.remainingKlingons        += 1
        self._gameState.remainingCommanders      += 1
        self._gameState.remainingSuperCommanders += 1

        return quadrant

    def _testEnemyDeadHandler(self, quadrant: Quadrant, enemyName: str):
        """
        Runs the appropriate count test

        Args:
            quadrant:   A randomly generated quadrant
            enemyName:  The enemy name, 'Klingon', 'Commander', 'SuperCommander'

        I normally don't like to write dynamically generated codes like this.  However,
        I could not in good conscience duplicate this code three times;  I know it is
        very 'Pythonic', but very high maintenance
        """

        gsPropertyName: str = f'remaining{enemyName}s'
        qPropertyName:  str = f'{enemyName[0].lower()}{enemyName[1:]}Count'

        beforeEnemyCount:   int = getattr(self._gameState, gsPropertyName)
        quadrantEnemyCount: int = getattr(quadrant, qPropertyName)

        self._eventHandlers.superNovaEventHandler(quadrant=quadrant)
        actualEnemyCount: int = getattr(quadrant, qPropertyName)
        self.assertEqual(0, actualEnemyCount, f'Not all {enemyName}s are dead')

        expectedRemainingEnemies: int = beforeEnemyCount - quadrantEnemyCount
        actualRemainingEnemies:   int = getattr(self._gameState, gsPropertyName)

        self.assertEqual(expectedRemainingEnemies, actualRemainingEnemies, f'Game State was not updated for {enemyName}s')

    @classmethod
    def _setupGame(cls):
        """
        Assumes the game setting location has been set

        Since the game mechanics are run by singletons set them up once
        at the start of this test class.  Then each instance test will just
        use the pre-initialized singletons

        The initializaton code copied from PyTrekView
        TODO: perhaps should go in a utility class so it is always current

        """
        # These singletons are initialized for the first time
        TestFutureEventHandlers.clsGameSettings = GameSettings()     # Be able to read the preferences file
        TestFutureEventHandlers.clsGameState    = GameState()        # Set up the game parameters which uses the above
        TestFutureEventHandlers.clsGameEngine   = GameEngine()       # Then the engine needs to be initialized
        TestFutureEventHandlers.clsIntelligence = Intelligence()
        TestFutureEventHandlers.clsComputer     = Computer()
        TestFutureEventHandlers.clsGalaxy       = Galaxy()           # This essentially finishes initializing most of the game


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestFutureEventHandlers))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
