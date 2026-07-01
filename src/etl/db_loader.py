from pathlib import Path
from sqlalchemy import create_engine, text
from config.setting import DB_PATH


class DatabaseLoader:

    def __init__(self):

        DB_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.engine = create_engine(
            f"sqlite:///{DB_PATH}"
        )

        with open(
            "database/schema.sql",
            "r",
            encoding="utf-8"
        ) as f:

            schema = f.read()

        with self.engine.connect() as conn:
            conn.execute(
                text( "PRAGMA foreign_keys = ON;")
                    
        
    )
            for statement in schema.split(";"):

                if statement.strip():

                    conn.execute(
                        text(statement)
                    )

            conn.commit()

    def load_table(self, df, table_name):

        with self.engine.begin() as conn:

            conn.execute(
                text(f"DELETE FROM {table_name}")
            )

        df.to_sql(
            table_name,
            self.engine,
            if_exists="append",
            index=False
        )