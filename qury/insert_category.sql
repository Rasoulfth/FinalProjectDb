INSERT INTO Categories (category_name)
SELECT DISTINCT "Category" FROM final_GooglePlay
ON CONFLICT (category_name) DO NOTHING;
