SELECT category_id, COUNT(*) AS app_count
FROM Apps
GROUP BY category_id
ORDER BY app_count DESC
LIMIT 1;
