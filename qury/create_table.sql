CREATE TABLE Apps (
    app_id TEXT PRIMARY KEY,
    app_name TEXT NOT NULL,
    category_id INT NOT NULL,
    rating FLOAT DEFAULT 0,
    rating_count INT DEFAULT 0,
    installs BIGINT,
    min_installs BIGINT,
    max_installs BIGINT,
    free BOOLEAN,
    price FLOAT DEFAULT 0,
    currency TEXT,
    size TEXT,
    min_android TEXT,
    developer_id INT NOT NULL,
    released DATE,
    last_updated DATE,
    content_rating TEXT,
    privacy_policy TEXT,
    ad_supported BOOLEAN,
    in_app_purchases BOOLEAN,
    editors_choice BOOLEAN
);

CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE Developers (
    developer_id SERIAL PRIMARY KEY,
    developer_name TEXT UNIQUE NOT NULL,
    developer_website TEXT,
    developer_email TEXT
);
