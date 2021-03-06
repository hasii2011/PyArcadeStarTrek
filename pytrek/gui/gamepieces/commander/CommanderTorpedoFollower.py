from pytrek.gui.gamepieces.base.BaseTorpedoFollower import BaseTorpedoFollower
from pytrek.gui.gamepieces.GamePieceTypes import EnemyFollowerId


class CommanderTorpedoFollower(BaseTorpedoFollower):

    FILENAME: str = 'CommanderTorpedoFollower.png'

    nextId: int = 0

    def __init__(self):

        followerId: EnemyFollowerId = EnemyFollowerId(f'CommanderTorpedoFollower-{CommanderTorpedoFollower.nextId}')

        super().__init__(filename=CommanderTorpedoFollower.FILENAME, followerId=followerId, scale=0.7)

        CommanderTorpedoFollower.nextId += 1
