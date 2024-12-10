-- Table: auth_user
CREATE TABLE auth_user (
    id serial NOT NULL PRIMARY KEY,
    password varchar(128) NOT NULL,
    last_login timestamp with time zone NULL,
    is_superuser boolean NOT NULL,
    username varchar(150) NOT NULL UNIQUE,
    first_name varchar(150) NOT NULL,
    last_name varchar(150) NOT NULL,
    email varchar(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);

-- Table: my_app_wines
CREATE TABLE my_app_wines (
    ID serial NOT NULL PRIMARY KEY,
    Name varchar(100) NOT NULL,
    Type varchar(100) NOT NULL,
    Year integer NULL,
    Grapes varchar(100) NULL,
    Country varchar(100) NOT NULL,
    Region varchar(100) NULL,
    Price decimal(6, 2) NULL,
    Description text NOT NULL,
    Qty integer NULL,
    image varchar(100) NULL
);

-- Table: my_app_spirits
CREATE TABLE my_app_spirits (
    ID serial NOT NULL PRIMARY KEY,
    Type varchar(100) NOT NULL DEFAULT '',
    Name varchar(100) NOT NULL DEFAULT '',
    Style varchar(100) NULL,
    AlcLvl integer NOT NULL DEFAULT 0,
    Price decimal(6, 2) NULL,
    Qty integer NULL,
    image varchar(100) NULL
);

-- Table: my_app_cart
CREATE TABLE my_app_cart (
    id serial NOT NULL PRIMARY KEY,
    user_id integer NOT NULL UNIQUE REFERENCES auth_user(id) ON DELETE CASCADE,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table: my_app_cartitem
CREATE TABLE my_app_cartitem (
    id serial NOT NULL PRIMARY KEY,
    cart_id integer NOT NULL REFERENCES my_app_cart(id) ON DELETE CASCADE,
    wine_id integer NULL REFERENCES my_app_wines(ID) ON DELETE CASCADE,
    spirit_id integer NULL REFERENCES my_app_spirits(ID) ON DELETE CASCADE,
    quantity integer NOT NULL DEFAULT 1,
    price decimal(6, 2) NULL
);

-- Table: my_app_order
CREATE TABLE my_app_order (
    id serial NOT NULL PRIMARY KEY,
    user_id integer NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    first_name varchar(30) NOT NULL DEFAULT '',
    last_name varchar(30) NOT NULL DEFAULT '',
    email varchar(254) NOT NULL DEFAULT '',
    phone_number varchar(15) NOT NULL DEFAULT '',
    address varchar(255) NULL,
    city varchar(100) NULL,
    county varchar(100) NOT NULL DEFAULT '',
    postal_code varchar(6) NULL,
    total_price decimal(10, 2) NOT NULL
);

-- Table: my_app_orderitem
CREATE TABLE my_app_orderitem (
    id serial NOT NULL PRIMARY KEY,
    order_id integer NOT NULL REFERENCES my_app_order(id) ON DELETE CASCADE,
    wine_id integer NULL REFERENCES my_app_wines(ID) ON DELETE CASCADE,
    spirit_id integer NULL REFERENCES my_app_spirits(ID) ON DELETE CASCADE,
    quantity integer NOT NULL,
    price decimal(6, 2) NOT NULL,
    name varchar(100) NULL,
    type varchar(100) NULL,
    year integer NULL,
    grapes varchar(100) NULL,
    country varchar(100) NULL,
    region varchar(100) NULL,
    alcohol_level integer NULL,
    style varchar(100) NULL
);