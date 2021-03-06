#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches;")
    db.commit()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players;")
    db.commit()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor();
    c.execute("select count(*) from players;");
    rows = c.fetchone();
    return rows[0];

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (name) values(%s);",
              (name, ));
    db.commit();

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db = connect()
    c = db.cursor()
    c.execute("select id, name, wins, matches from playerResults order by wins desc")
    rows = c.fetchall()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute('insert into matches (winnerId, loserId) values(' + str(winner) + ',' + str(loser) + ');')
    db.commit()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    db = connect()
    c = db.cursor()
    c.execute('select * from matches')
    matches = c.fetchall()
    pairings = []
    
    # This iteration through the standings is done
    # in a slightly non-intuitive way to better support
    # eventual impelementation of extra credit features
    # (and may support non-even player lists, but 
    # is contingent on match-winner decision logic)
    
    while standings:
      player1 = standings.pop()
      player2 = standings.pop()
      pairings.append((player1[0], player1[1], player2[0], player2[1]))
    return pairings
