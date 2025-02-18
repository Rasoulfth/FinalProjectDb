ALTER TABLE Apps 
ADD CONSTRAINT category_id FOREIGN KEY (category_id) REFERENCES Categories(category_id);
ALTER TABLE Apps 
ADD CONSTRAINT developer_id FOREIGN KEY (developer_id) REFERENCES Developers(developer_id);