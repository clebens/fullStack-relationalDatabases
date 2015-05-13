-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

drop table players cascade;
drop table matches cascade;

create table players (
  id SERIAL,
  name VARCHAR(255),
  PRIMARY KEY(id)
);

create table matches(
  winnerId INT,
  loserId INT
);

create view playerResults AS
  select  P.id as id, 
          P.name as name,
          (SELECT COUNT(*) from matches M where M.winnerId=P.id) as wins,
          (SELECT COUNT(*) from matches M where M.winnerId=P.id or M.loserId=P.id) as matches
  from players P; 
