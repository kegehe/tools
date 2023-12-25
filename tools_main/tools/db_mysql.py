from typing import Any, cast, Dict, List, Optional, Sequence

import aiomysql
from aiomysql import create_pool

config = {
    'host': '47.109.86.201',
    'port': 3306,
    'user': 'kegehe',
    'password': '153409712',
    'db': 'tools_test'
}


async def fetchone(sql: str, args: Sequence = ()):
    pool = await create_pool(**config)
    async with pool.acquire() as conn:
        conn = cast(aiomysql.Connection, conn)
        try:
            await conn.ping(reconnect=True)
        except Exception:
            await conn._connect()

        async with conn.cursor(aiomysql.DictCursor) as cur:
            conn = cast(aiomysql.Connection, conn)
            try:
                await cur.execute(sql, args)
                rs = await cur.fetchone()
            finally:
                await conn.commit()
            return rs


async def fetchmany(sql: str,
                    log_sql: bool = True,
                    args: Sequence = (),
                    size: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    封装查询多条数据
    Args:
        sql (str): sql语句
        log_sql (bool): 是否打印sql
        args (Sequence): sql参数
        size (int): 返回条数
    Returns:
        List[Dict[str, Any]]: 查询结果, 无结果返回空列表, 有结果返回元素为字典的列表
    """
    pool = await create_pool(**config)
    async with pool.acquire() as conn:
        conn = cast(aiomysql.Connection, conn)
        try:
            await conn.ping(reconnect=True)
        except Exception:
            await conn._connect()

        async with conn.cursor(aiomysql.DictCursor) as cur:
            cur = cast(aiomysql.Cursor, cur)
            try:
                await cur.execute(sql, args)
                if size:
                    rs = await cur.fetchmany(size)
                else:
                    rs = await cur.fetchall()
            finally:
                await conn.commit()
            return rs


async def fetchmany_total(select_sql: str,
                          log_sql: bool = True,
                          args: Sequence = ()) -> Dict[str, Any]:
    """
    查询多条数据，并返回总查询数量
    Args:
        select_sql (str): 查询sql
        log_sql (bool): 是否打印sql
        args (Sequence): sql参数
    Returns:
        total (int): 总查询数量
        data (List[Dict[str, Any]]): 查询结果, 无结果返回空列表, 有结果返回元素为字典的列表
    """
    pool = await create_pool(**config)
    async with pool.acquire() as conn:
        conn = cast(aiomysql.Connection, conn)
        try:
            await conn.ping(reconnect=True)
        except Exception:
            await conn._connect()

        async with conn.cursor(aiomysql.DictCursor) as cur:
            cur = cast(aiomysql.Cursor, cur)
            try:
                await cur.execute(select_sql, args)
                select_res = await cur.fetchall()
                if not select_res:
                    select_res = []
                sql_total = 'SELECT COUNT(*) AS total;'
                await cur.execute(sql_total)
                total = await cur.fetchone()
            except Exception:
                await conn.rollback()
                raise ValueError("查询信息失败")
            else:
                await conn.commit()
                total = total.get("total", 0)
                return {"data": select_res, "total": total}
            finally:
                await conn.commit()


async def execute(sql: str, log_sql: bool = True, args: Sequence = ()) -> Optional[int]:
    """
    封装insert, delete, update
    Args:
        sql (str): sql语句
        log_sql (bool): 是否打印sql
        args (Sequence): sql参数
    Returns:
        Optional[int]: 最后一条更新数据的id, 无更新返回None
    """
    pool = await create_pool(**config)
    async with pool.acquire() as conn:
        conn = cast(aiomysql.Connection, conn)
        try:
            await conn.ping(reconnect=True)
        except Exception as e:
            print(e)
            await conn._connect()

        async with conn.cursor(aiomysql.DictCursor) as cur:
            cur = cast(aiomysql.Cursor, cur)
            try:
                await cur.execute(sql, args)
            except BaseException as e:
                print(e)
                await conn.rollback()
                return None
            else:
                affected = cur.rowcount
                _id = cur.lastrowid
                await conn.commit()
                return _id
            finally:
                await conn.commit()


async def executemany(sql: str,
                      log_sql: bool = True,
                      args: Sequence[Sequence] = (),
                      get_count: bool = False) -> Optional[int]:
    """
    封装多条数据的insert
    Args:
        sql (str): sql语句
        log_sql (bool): 是否打印sql到日志
        args (Sequence): sql语句参数
        get_count (bool): 是否返回影响行数，默认返回最后插入的id
    Returns:
        Optional[int]: 返回最后插入的id或者影响行数
    """
    pool = await create_pool(**config)
    async with pool.acquire() as conn:
        conn = cast(aiomysql.Connection, conn)
        try:
            await conn.ping(reconnect=True)
        except Exception:
            await conn._connect()

        async with conn.cursor(aiomysql.DictCursor) as cur:
            cur = cast(aiomysql.Cursor, cur)
            try:
                await cur.executemany(sql, args)
            except BaseException:
                await conn.rollback()
                return None
            else:
                affected = cur.rowcount
                _id = cur.lastrowid
                await conn.commit()
                if get_count:
                    return affected
                return _id
            finally:
                await conn.commit()
