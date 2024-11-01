from models import Base
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from transactions import get_scores_txn, add_score_txn
import logging

class Leaderboard:
    def __init__(self, conn_string=None):
        # Using SQLite in-memory mode, conn_string is not used
        self.engine = create_engine('sqlite://',
                    connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
        self.sessionmaker = sessionmaker(bind=self.engine)

        # Base.metadata.create_all(self.engine)

        # Run SQL initialization script
        self.initialize_db()

    def initialize_db(self):
        # Read and execute SQL commands from dbinit.sql
        try:
            with open("ddl.sql", "r") as f:
                sql_script = f.read()
            
            # Execute the script
            with self.engine.connect() as connection:
                connection.execute(text(sql_script))
                connection.commit()

            with open("dml.sql", "r") as f:
                sql_script = f.read()
            
            # Execute the script
            with self.engine.connect() as connection:
                connection.execute(text(sql_script))
                connection.commit()
                
        except OperationalError as e:
            print(f"Error initializing database: {e}")
        except FileNotFoundError:
            print("Initialization file dbinit.sql not found.")

    def get_scores(self):
        with self.sessionmaker() as session:
            return self.prepare_scores(session)

    def add_score(self, score):
        with self.sessionmaker() as session:
            add_score_txn(session, score.avatar, score.playername, score.points)
            session.commit()

    def prepare_scores(self, session):
        scores = get_scores_txn(session)
        scores.sort(reverse=True, key=lambda e: e.points)

        result = list(map(lambda score, i: {'id': score.id,
                                            'ranking': i + 1,
                                            'avatar': self.get_avatar_dic().get(str(score.avatar), "not set"),
                                            'playername': score.playername,
                                            'points': score.points
                                            },
                          scores,
                          list(range(len(scores)))))
        return result

    def get_avatar_dic(self):
        return {
            "0": "not set",
            "1": "👨🏻",
            "2": "👨🏼",
            "3": "👨🏽",
            "4": "👨🏾",
            "5": "👨🏿",
            "6": "👩🏻",
            "7": "👩🏼",
            "8": "👩🏽",
            "9": "👩🏾",
            "10": "👩🏿"
        }
