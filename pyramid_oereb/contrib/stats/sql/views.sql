

/*
 * example request to use the json object in the msg field
 * SELECT cast(msg as json),created_at AS response FROM oereb_logs.logs WHERE logger = 'JSON' AND cast( cast(msg as json) -> 'response' ->> 'status_code' AS INT) = 200;
 */


/*GetVersions view*/
CREATE OR REPLACE VIEW stats_get_versions AS
    SELECT cast(msg as json) -> 'response' -> 'extras' ->> 'service' AS service ,
           cast(cast(msg as json) -> 'response' ->> 'status_code' AS INTEGER) AS status_code, 
           cast(msg as json) -> 'response' -> 'extras' ->> 'output_format' AS output_format,
           created_at,
           cast(msg as json) -> 'request' ->> 'path' AS path                                
    FROM oereb_logs.logs WHERE logger = 'JSON' AND cast(msg as json) -> 'response' ->'extras' ->> 'service' = 'GetVersions';

/*GetCapabilities view*/
CREATE OR REPLACE VIEW stats_get_capabilities AS
    SELECT cast(msg as json) -> 'response' -> 'extras' ->> 'service' AS service ,
           cast(cast(msg as json) -> 'response' ->> 'status_code' AS INTEGER) AS status_code, 
           cast(msg as json) -> 'response' -> 'extras' ->> 'output_format' AS output_format,
           created_at,
           cast(msg as json) -> 'request' ->> 'path' AS path                                
    FROM oereb_logs.logs WHERE logger = 'JSON' AND cast(msg as json) -> 'response' ->'extras' ->> 'service' = 'GetCapabilities';

/*GetEgridCoord view*/
CREATE OR REPLACE VIEW stats_get_egrid_coord AS
    SELECT cast(msg as json) -> 'response' -> 'extras' ->> 'service' AS service ,
           cast(cast(msg as json) -> 'response' ->> 'status_code' AS INTEGER) AS status_code, 
           cast(msg as json) -> 'response' -> 'extras' ->> 'output_format' AS output_format,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'xy' AS xy,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'gnss' AS gnss,
           created_at,
           cast(msg as json) -> 'request' ->> 'path' AS path                                
    FROM oereb_logs.logs WHERE logger = 'JSON' AND cast(msg as json) -> 'response' ->'extras' ->> 'service' = 'GetEgridCoord';

/*GetEgridIdent view*/
CREATE OR REPLACE VIEW stats_get_egrid_ident AS
    SELECT cast(msg as json) -> 'response' -> 'extras' ->> 'service' AS service ,
           cast(cast(msg as json) -> 'response' ->> 'status_code' AS INTEGER) AS status_code, 
           cast(msg as json) -> 'response' -> 'extras' ->> 'output_format' AS output_format,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'identdn' AS identdn,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'number' AS number,
           created_at,
           cast(msg as json) -> 'request' ->> 'path' AS path                                
    FROM oereb_logs.logs WHERE logger = 'JSON' AND cast(msg as json) -> 'response' ->'extras' ->> 'service' = 'GetEgridIdent';

/*GetEgridAddress view*/
CREATE OR REPLACE VIEW stats_get_egrid_address AS
    SELECT cast(msg as json) -> 'response' -> 'extras' ->> 'service' AS service ,
           cast(cast(msg as json) -> 'response' ->> 'status_code' AS INTEGER) AS status_code, 
           cast(msg as json) -> 'response' -> 'extras' ->> 'output_format' AS output_format,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'postalcode' AS postalcode,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'localisation' AS localisation,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> 'number' AS number,
           created_at,
           cast(msg as json) -> 'request' ->> 'path' AS path                                
    FROM oereb_logs.logs WHERE logger = 'JSON' AND cast(msg as json) -> 'response' ->'extras' ->> 'service' = 'GetEgridAddress';

/*GetExtractById view*/
CREATE OR REPLACE VIEW stats_get_extract_by_id AS
    SELECT cast(msg as json) -> 'response' -> 'extras' ->> 'service' AS service ,
           cast(cast(msg as json) -> 'response' ->> 'status_code' AS INTEGER) AS status_code, 
           cast(msg as json) -> 'response' -> 'extras' ->> 'output_format' AS output_format,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> '__flavour__' AS flavour,
           cast(msg as json) -> 'response' -> 'extras' -> 'params' ->> '__egrid__' AS egrid,
           created_at,
           cast(msg as json) -> 'request' ->> 'path' AS path                                
    FROM oereb_logs.logs WHERE logger = 'JSON' AND cast(msg as json) -> 'response' ->'extras' ->> 'service' = 'GetExtractById';
