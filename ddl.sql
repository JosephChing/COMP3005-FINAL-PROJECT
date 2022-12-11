CREATE TABLE books(
	isbn varchar UNIQUE,
	bookname varchar NOT NULL,
	num_of_pages bigint NOT NULL, 
	price bigint NOT NULL, 
	publisher varchar NOT NULL, 
	pub_royalties numeric(4,2) NOT NULL, 
	current_stock bigint NOT NULL, 
	min_books bigint NOT NULL,
	last_month_sales bigint NOT NULL,
	PRIMARY KEY (isbn)

);

CREATE TABLE book_genres(
	isbn varchar NOT NULL,
	genre varchar NOT NULL
);

CREATE TABLE book_authors(
	isbn varchar NOT NULL,
	author varchar NOT NULL
);

CREATE TABLE publisher(
	name varchar UNIQUE,
	address varchar NOT NULL,
	email varchar UNIQUE,
	bank_account_number bigint UNIQUE,
	PRIMARY KEY (name)
);

CREATE TABLE order_contains(
	order_id varchar NOT NULL,
	book_isbn varchar NOT NULL,
	quantity bigint NOT NULL
);

CREATE TABLE orders(
	order_id varchar UNIQUE,
	cardnumber varchar NOT NULL,
	shipping_address varchar NOT NULL,
	username varchar NOT NULL,
	ship_date date NOT NULL,
	expected_arrival date NOT NULL,
	order_status varchar NOT NULL,
	publisher_paid boolean NOT NULL,
	total_sum float NOT NULL,
	PRIMARY KEY (order_id)
);

CREATE TABLE users(
	username varchar UNIQUE,
	password varchar NOT NULL,
	cardnumber varchar NOT NULL,
	address varchar NOT NULL,
	PRIMARY KEY(username)
);

CREATE TABLE placed_orders(
	order_id varchar,
	username varchar NOT NULL,
	PRIMARY KEY(order_id)
);

CREATE TABLE billing_info(
	cardnumber varchar UNIQUE,
	cardholder_name varchar NOT NULL,
	exp_date char(5) NOT NULL,
	address varchar NOT NULL,
	PRIMARY KEY(cardnumber)
);



CREATE TABLE publisher_phone_numbers(
	name varchar NOT NULL,
	phone_number bigint NOT NULL
);

ALTER TABLE publisher_phone_numbers
ADD FOREIGN KEY(name) REFERENCES publisher(name);

ALTER TABLE book_authors
ADD FOREIGN KEY(isbn) REFERENCES books(isbn);

ALTER TABLE book_genres
ADD FOREIGN KEY(isbn) REFERENCES books(isbn);

ALTER TABLE books
ADD FOREIGN KEY(publisher) REFERENCES Publisher(name);

ALTER TABLE placed_orders
ADD FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE placed_orders
ADD FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_contains
ADD FOREIGN KEY (order_id) REFERENCES orders(order_id);

ALTER TABLE order_contains
ADD FOREIGN KEY (book_isbn) REFERENCES books(isbn);

ALTER TABLE orders
ADD FOREIGN KEY (cardnumber) REFERENCES billing_info(cardnumber);

ALTER TABLE users
ADD FOREIGN KEY (cardnumber) REFERENCES billing_info(cardnumber);




