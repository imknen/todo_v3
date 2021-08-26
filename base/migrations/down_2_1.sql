begin;

drop table users;

INSERT INTO db_version(fversion, fdate, fdescription)
    values('0.1',
    CURRENT_TIMESTAMP,
    'delete table users');

end;
