START TRANSACTION;

CREATE TABLE db_version (
	id_record		serial,
	fversion 	varchar (20),
	fdate 		timestamp not null,
	fdescription	varchar(256),
	CONSTRAINT  	pk_history PRIMARY KEY(id_record)
) ;

INSERT INTO db_version(fversion, fdate, fdescription)
	values('0.1',
		CURRENT_TIMESTAMP,
		'base is empty and created control version');

COMMIT TRANSACTION;
