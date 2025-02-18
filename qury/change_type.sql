ALTER TABLE final_googleplay
  ALTER COLUMN "Minimum Installs" TYPE float USING "Minimum Installs"::float;
