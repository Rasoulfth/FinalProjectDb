INSERT INTO Developers (developer_name, developer_website, developer_email)
SELECT DISTINCT "Developer Id", "Developer Website", "Developer Email"
FROM final_GooglePlay
ON CONFLICT (developer_name) DO NOTHING;
