class AIORedisHelper(object):
    def __init__(self, connection):
        self.connection = connection

    async def get_atomic_connection(self):
        """
        Gets a pipeline for normal redis or for redis sentinel based
        upon redis mode in configuration

        :return: Returns a pipeline
        """
        return self.connection.pipeline()
