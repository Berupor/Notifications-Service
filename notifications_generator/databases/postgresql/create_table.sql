CREATE TABLE schedule (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    crontab varchar(50) not null,
    created timestamp DEFAULT current_timestamp
);

CREATE TABLE events (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    id_shedule uuid null,
    name varchar(255) not null,
    priority int not null,
    event text not null,
    created timestamp DEFAULT current_timestamp,
    FOREIGN KEY(id_shedule) REFERENCES shedule(id)
);