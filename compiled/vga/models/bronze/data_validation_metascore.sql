

SELECT
    min(metacritic) AS min_metacritic,
    max(metacritic) AS max_metacritic,
    count(metacritic) AS count_metacritic,
    count(game_id) AS count_game
FROM `video-game-analysis-418605`.`source`.`external_games`