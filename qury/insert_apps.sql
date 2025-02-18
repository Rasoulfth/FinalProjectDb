INSERT INTO Apps (app_id, app_name, category_id, rating, rating_count, installs, min_installs, max_installs, free,
                  price, currency, size, min_android, developer_id, released, last_updated, content_rating,
                  privacy_policy, ad_supported, in_app_purchases, editors_choice)
SELECT 
    fgp."App Id", 
    fgp."App Name", 
    c.category_id, 
    fgp."Rating", 
    fgp."Rating Count", 
    fgp."Installs", 
    fgp."Minimum Installs", 
    fgp."Maximum Installs", 
    fgp."Free", 
    fgp."Price", 
    fgp."Currency", 
    fgp."Size", 
    fgp."Minimum Android", 
    d.developer_id, 
    fgp."Released", 
    fgp."Last Updated", 
    fgp."Content Rating", 
    fgp."Privacy Policy", 
    fgp."Ad Supported", 
    fgp."In App Purchases", 
    fgp."Editors Choice"
FROM final_GooglePlay fgp
JOIN Categories c ON fgp."Category" = c.category_name
JOIN Developers d ON fgp."Developer Id" = d.developer_name
ON CONFLICT (app_id) DO NOTHING;
