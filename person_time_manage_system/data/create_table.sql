
create table IF NOT EXISTS user_info (
user_id              INTEGER,
user_name            CHAR(128),
password             CHAR(128),
email             CHAR(128),
active               INTEGER,
auth_token_file      CHAR(256),
calender_server      CHAR(128),
calender_name        CHAR(128)
);

create table IF NOT EXISTS every_month_cache (
id                   INTEGER                        not null,
user_id              INTEGER,
month_str            CHAR(7),
category             CHAR(16),
during               INTEGER,
nums                 INTEGER,
word_cloud           LONG VARCHAR,
primary key (id),
foreign key (user_id)
      references user_info (user_id)
);

create table IF NOT EXISTS every_week_cache (
id                   INTEGER                        not null,
user_id              INTEGER,
start_date_str       CHAR(10),
end_date_str         CHAR(10),
category             CHAR(10),
during               INTEGER,
nums                 INTEGER,
primary key (id),
foreign key (user_id)
      references user_info (user_id)
);

create table IF NOT EXISTS everyday_cache (
id                   INTEGER                        not null,
user_id              INTEGER,
date_str             CHAR(10),
category             CHAR(16),
during               INTEGER,
nums                 INTEGER,
primary key (id),
foreign key (user_id)
      references user_info (user_id)
);

create table IF NOT EXISTS time_details (
id                   INTEGER                        not null,
user_id              INTEGER,
date_str             CHAR(10),
category             CHAR(16),
start_time           CHAR(10),
end_time             CHAR(10),
during               INTEGER,
descrition           LONG VARCHAR,
primary key (id),
foreign key (user_id)
      references user_info (user_id)
);

