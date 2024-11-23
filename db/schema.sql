CREATE TYPE CardType AS ENUM (
    'Battle',
    'Planeswalker',
    'Creature',
    'Sorcery',
    'Instant',
    'Artifact',
    'Enchantment',
    'Land',
    'Kindred', -- f.k.a. Tribal

    -- Extras
    'Conspiracy',
    'Dungeon',
    'Phenomenon',
    'Plane',
    'Scheme',
    'Vanguard'
    );

CREATE TABLE Card (
    id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    main_type CardType NOT NULL -- new field, unique from scryfall. used to group cards by type in a decklist.
);

CREATE TYPE Finish AS ENUM ('nonfoil', 'foil', 'etched');

CREATE TABLE Printing (
    id SERIAL PRIMARY KEY NOT NULL,
    card_id SERIAL NOT NULL REFERENCES Card(id),
    -- types CardType[] NOT NULL,
    -- type_line VARCHAR(127) NOT NULL,
    set VARCHAR(7) NOT NULL,
    set_name VARCHAR(255) NOT NULL,
    collector_number VARCHAR(7) NOT NULL,
    image_uri VARCHAR(255) NOT NULL, -- this is equivalent to scryfall.image_uris.normal
    back_image_uri VARCHAR(255), -- this is equivalent to scryfall.CardFaces[1].image_uris.normal
    finishes Finish[] NOT NULL,

    price_usd DECIMAL(10, 2),
    price_usd_foil DECIMAL(10, 2),
    price_usd_etched DECIMAL(10, 2),
    price_eur DECIMAL(10, 2),
    price_eur_foil DECIMAL(10, 2),
    price_eur_etched DECIMAL(10, 2) -- not supported by scryfall for some reason
);

INSERT INTO Card (name, main_type) VALUES
    ('Animate Dead', 'Enchantment'),
    ('Arachnogenesis', 'Instant'),
    ('Assassin''s Trophy', 'Instant'),
    ('Azusa, Lost but Seeking', 'Creature'),
    ('Bala Ged Recovery // Bala Ged Sanctuary', 'Sorcery'),
    ('Baba Lysaga, Night Witch', 'Creature');

INSERT INTO Printing (
    card_id, set, set_name, collector_number, image_uri, back_image_uri,
    finishes, price_usd, price_usd_foil, price_usd_etched,
    price_eur, price_eur_foil, price_eur_etched) VALUES
    (1, 'MKC', 'Murders at Karlov Manor Commander', '125', 'https://cards.scryfall.io/normal/front/1/4/1489943b-c010-488e-9c9d-87f4af67a4e4.jpg?1706240754', NULL, ARRAY['nonfoil']::Finish[], 5.83, NULL, NULL, 6.36, NULL, NULL),
    (1, '30A', '30th Anniversary Edition', '92', 'https://cards.scryfall.io/normal/front/8/b/8b9e9104-0d3f-4467-abe3-d0e1bff0189e.jpg?1664927738', NULL, ARRAY['nonfoil']::Finish[], NULL, NULL, NULL, NULL, NULL, NULL),
    (1, 'PLST', 'The List', 'EMA-78', 'https://cards.scryfall.io/normal/front/4/c/4c732dc7-dd6b-4cc1-bbe0-ff3b1d2c7419.jpg?1622846572', NULL, ARRAY['nonfoil']::Finish[], 5.83, NULL, NULL, 6.36, NULL, NULL),
    (2, 'DSC', 'Duskmourn: House of Horror Commander', '169', 'https://cards.scryfall.io/normal/front/d/f/df244eab-9631-4c84-b8d6-0f62ace60b83.jpg?1690001244', NULL, ARRAY['nonfoil']::Finish[], 0.84, NULL, NULL, 1.70, NULL, NULL),
    (3, 'MKM', 'Murders at Karlov Manor', '187', 'https://cards.scryfall.io/normal/front/e/d/ed6c7d29-71b4-4134-b591-5598f479d592.jpg?1706242115', NULL, ARRAY['nonfoil', 'foil']::Finish[], 2.48, 2.39, NULL, 1.92, 2.73, NULL),
    (4, 'CMM', 'Commander Masters', '274', 'https://cards.scryfall.io/normal/front/2/1/2184e61d-6f25-425a-b914-b7d6ecd002c2.jpg?1719466666', NULL, ARRAY['nonfoil', 'foil']::Finish[], 8.83, 10.26, NULL, 7.26, 9.75, NULL),
    (5, 'ZNR', 'Zendikar Rising', '180', 'https://cards.scryfall.io/normal/front/c/5/c5cb3052-358d-44a7-8cfd-cd31b236494a.jpg?1604263635', 'https://cards.scryfall.io/normal/back/c/5/c5cb3052-358d-44a7-8cfd-cd31b236494a.jpg?1604263635', ARRAY['nonfoil', 'foil']::Finish[], 3.97, 4.80, NULL, 3.87, 5.24, NULL),
    (6, 'CLB', 'Commander Legends: Battle for Baldur''s Gate', '266', 'https://cards.scryfall.io/normal/front/b/3/b330c216-4c1f-4318-8add-20b766afd94c.jpg?1681412803', NULL, ARRAY['etched']::Finish[], NULL, NULL, 0.16, NULL, NULL, 0.15);
