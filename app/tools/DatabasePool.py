class DatabasePool:
    """
    建立连接池对象(单例)
    """
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'mysql_db_dict'):
            self.mysql_db_dict = {}
        if not hasattr(self, 'redis_db_dict'):
            self.redis_db_dict = {}