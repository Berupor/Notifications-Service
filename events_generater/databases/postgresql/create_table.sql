CREATE TABLE shedule (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    crontab varchar(50) not null,
    created timestamp DEFAULT current_timestamp
);

CREATE TABLE events (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    id_shedule uuid null,
    id_user uuid not null,
    email varchar(255) null,
    message text null,
    event text not null,
    priority int null,
    created timestamp DEFAULT current_timestamp,
    FOREIGN KEY(id_shedule) REFERENCES shedule(id)
);