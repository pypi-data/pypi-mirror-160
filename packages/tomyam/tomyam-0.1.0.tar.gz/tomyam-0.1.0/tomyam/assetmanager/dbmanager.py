from __future__ import annotations
import sqlalchemy
import pandas as pd
from urllib.parse import quote
from sqlalchemy.sql import text


class DBManager:
    """
    DB에 저장되는 데이터를 관리합니다.
    """

    def __init__(self, user, password, db, host, port: str):
        self.engine = self.create_engine(user, password, db, host, port)

    @staticmethod
    def create_engine(user, password, db, host, port):
        """
        sqlalchemy를 이용하여 DB와 연결하는 엔진을 반환합니다.
        """
        # 비밀번호에 @가 들어가면 sqlalchemy가 db연결 url를 잘못 읽는 버그가 있음. 따라서 quote 사용
        url = "postgresql://{}:%s@{}:{}/{}".format(user, host, port, db) % quote(
            password
        )

        # The return value of create_engine() is our connection object
        sqlalchemy_engine = sqlalchemy.create_engine(url, client_encoding="utf8")
        return sqlalchemy_engine  # , meta

    @staticmethod
    def param2sql(sql, **kwargs):
        q = text(sql)
        return q.bindparams(**kwargs)

    def query2df(self, query: str, **kwargs) -> pd.DataFrame:
        """
        쿼리를 입력하여 결과를 DataFrame으로 반환합니다.
        """
        query = self.param2sql(query, **kwargs)
        df = pd.read_sql(query, self.engine)
        return df

    def query2dict(
        self, query: str, orient: "dict" | "records" | None = "dict", **kwargs
    ) -> dict:
        """
        쿼리를 입력하여 결과를 dictionary로 반환합니다.

        Args:
            orient:어떤 방식으로 딕셔너리를 만들 것인지 결정합니다.
        """
        query = self.param2sql(query, **kwargs)
        df = pd.read_sql(query, self.engine)
        return df.to_dict(orient=orient)

    def query2list(self, query: str) -> list:
        """
        쿼리를 입력하여 결과를 list로 반환합니다.
        """
        df = pd.read_sql(query, self.engine)
        return df.values.tolist()

    def query2numpy(self, query: str) -> list:
        """
        쿼리를 입력하여 결과를 list로 반환합니다.
        """
        df = pd.read_sql(query, self.engine)
        return df.to_numpy()

    def execute_sql(self, sql: str, *args, **kwargs):
        """
        db에 raw sql를 날리고 결과를 출력합니다.
        sql에 변수를 바인딩할 수 있습니다.
        변수를 sql에 :variable로 표시하고, 해당 변수를 args 또는 kwargs로 입력합니다.
        """
        sql = text(sql)
        with self.engine.connect() as con:
            try:
                rs = con.execute(sql, *args, **kwargs)
            except Exception as e:
                print("DB_ERROR", e)
                raise
        return rs
