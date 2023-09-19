from gymnasium.envs.registration import register 

# Environment for debugging
register(
    id='FiremanGrid-ExtinguishFire-v0',
    entry_point='firemangrid.envs:ExtinguishFireEnv',
)

register(
    id='FiremanGrid-MoveDebris-v0',
    entry_point='firemangrid.envs:MoveDebrisEnv',
)

register(
    id='FiremanGrid-RescueSurvivor-v0',
    entry_point='firemangrid.envs:RescueSurvivorEnv',
) 

register(
    id='FiremanGrid-OpenDoor-v0',
    entry_point='firemangrid.envs:OpenDoorEnv',
) 

register(
    id='FiremanGrid-Start2Key-v0',
    entry_point='firemangrid.envs:FiremanWholeEnv',
    kwargs={'task': 'start2key'}
)