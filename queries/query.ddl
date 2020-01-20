SELECT curr_state, curr_county, SUM(curr_county_pop_est) AS pop
FROM (SELECT DISTINCT curr_state,curr_county,curr_county_pop_est
FROM censusdb.inflow
WHERE curr_state = 'California')
GROUP BY curr_state, curr_county
ORDER BY 3 DESC