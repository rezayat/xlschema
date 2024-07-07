
-- schema SCHEMA
-- ---------------------------------------------------------------



drop table if exists person  ;
create table person
(
    id integer primary key not null,                   -- person id
    name varchar(10) not null,                         -- person name
    age integer check (age > 20) not null,             -- person age
    rating varchar(1) not null                         -- person rating
);



drop table if exists vehicle  ;
create table vehicle
(
    id integer primary key not null,                   -- car id
    brand text not null,                               -- car brand
    color varchar(20) default 'red' not null,          -- car color
    category varchar(10) not null,                     -- car category
    size varchar(10) not null,                         -- car size
    tire_size varchar(10) not null,                    -- tire size
    price float,                                       -- car price
    person_id integer references person (id) not null  -- assigned to
);



drop table if exists person_vehicle  ;
create table person_vehicle
(
    id integer primary key not null,                   -- id
    person_id integer references person (id) not null, -- person id
    vehicle_id integer references vehicle (id) not null, -- vehicle id
    from_date date not null,                           -- from date
    to_date date not null                              -- to date
);




-- schema DATA
-- ---------------------------------------------------------------

insert into person values (1, 'jon', 21, 'A');
insert into person values (2, 'sue', 45, 'B');
insert into person values (3, 'kate', 55, 'C');
insert into person values (4, 'ali', 32, 'D');
insert into person values (5, 'abdul', 61, 'E');
insert into person values (6, 'rajiv', 71, 'A');


insert into vehicle values (1, 'gm', 'red', 'sedan', 'medium', '245-30-17', 10.5, 1);
insert into vehicle values (2, 'nissan', 'blue', 'sedan', 'medium', '295-45-21', 21.2, 2);
insert into vehicle values (3, 'toyota', 'yellow', 'suv', 'large', '195-60-17', 31.9, 3);
insert into vehicle values (4, 'hyundai', 'red', 'suv', 'large', '245-30-17', 42.6, 4);
insert into vehicle values (5, 'ford', 'blue', 'suv', 'large', '295-45-21', 53.3, 5);
insert into vehicle values (6, 'mercedes', 'white', 'coupe', 'small', '195-60-17', 100.2, 6);
insert into vehicle values (7, 'toyota', 'white', 'suv', 'large', '195-60-17', 150, 1);


insert into person_vehicle values (1, 1, 7, '2016-10-25', '2016-10-25');
insert into person_vehicle values (2, 2, 2, '2016-10-25', '2016-10-25');
insert into person_vehicle values (3, 3, 3, '2016-10-25', '2016-10-25');
insert into person_vehicle values (4, 4, 2, '2016-10-25', '2016-10-25');
insert into person_vehicle values (5, 5, 1, '2016-10-25', '2016-10-25');
insert into person_vehicle values (6, 6, 6, '2016-10-25', '2016-10-25');



