ALTER TABLE Apps ADD CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Categories(category_id);
ALTER TABLE Apps ADD CONSTRAINT fk_developer FOREIGN KEY (developer_id) REFERENCES Developers(developer_id);
