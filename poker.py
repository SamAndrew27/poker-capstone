import pandas as pd
import sqlite3

pd.set_option("display.max_columns", 100)
conn = sqlite3.connect("drivehud.db")


tournaments = pd.read_sql_query("select * from Tournaments;", conn)

hand_history = pd.read_sql_query("select * from HandHistories;", conn)


game_info = pd.read_sql_query("select * from GameInfo;", conn)

player_game_info = pd.read_sql_query("select * from PlayerGameInfo;", conn)

hand_records = pd.read_sql_query("select * from HandRecords;", conn)


