START TRANSACTION;

CREATE TABLE tasks ( 
    id_task         serial,
    ftitle          varchar(256),
    fdescription    varchar(999),
    fstart_date     timestamp,
    fover_date	    timestamp,
    fparent_id      integer,
    fdate_completed timestamp,
    CONSTRAINT      pk_task PRIMARY KEY(id_task)
);

CREATE TABLE remainders (
    id_remainder     serial,
    fparent_id	     integer REFERENCES tasks,
    ftitle	     varchar(256),
    fmessage         varchar(999),
    fdate_remainder  timestamp not NULL,
    CONSTRAINT       pk_remainder PRIMARY KEY(id_remainder)
);

CREATE TABLE notes (
	id_note		serial,
	fparent_id	integer REFERENCES tasks,
	fvolume		varchar(999),
	CONSTRAINT	pk_note PRIMARY KEY(id_note)
);

INSERT INTO db_version(fversion, fdate, fdescription)
    values('2.5',
           CURRENT_TIMESTAMP,
           'add tables: tasks, remainders, notes');

COMMIT TRANSACTION;
