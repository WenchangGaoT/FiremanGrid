from gymnasium.envs.registration import register 

# Environment for debugging
register(
        id='FiremanGrid-ExtinguishFire-v0',
        entry_point='firemangrid.envs:ExtinguishFireEnv',
    )

