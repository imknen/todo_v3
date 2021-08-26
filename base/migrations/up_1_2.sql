BEGIN;

CREATE TABLE users (
    id_user     SERIAL,
    fname       varchar(32),
    ffemale     varchar(32),
    fpatronymic varchar(32),
    f_nick      varchar(32),
    CONSTRAINT  pk_user PRIMARY KEY(id_user)
);

INSERT INTO db_version(fversion, fdate, fdescription)
    values('1.2',
    CURRENT_TIMESTAMP,
    'create table users');
END;
