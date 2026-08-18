INSERT INTO protege.zones
    (zone_id, zone_name, activity_code, productivity_class, min_rssi_dbm)
VALUES
    ('Z01', 'Acceso', 'ACCESS', 'SUPPORT', -85),
    ('Z02', 'Casa de cambio', 'CHANGE_HOUSE', 'NON_PRODUCTIVE_PLANNED', -82),
    ('Z03', 'Reunión e instrucciones', 'INSTRUCTIONS', 'NON_PRODUCTIVE_PLANNED', -82),
    ('Z04', 'Pañol de herramientas', 'TOOLS', 'NON_PRODUCTIVE_INFERRED', -82),
    ('Z05', 'Frente de trabajo', 'WORK_FACE', 'PRODUCTIVE', -85),
    ('Z00', 'Zona indefinida / tránsito', 'UNDEFINED', 'UNKNOWN', -127),
    ('Z05-A', 'Zona de trabajo A', 'WORK_FACE', 'PRODUCTIVE', -85),
    ('Z05-B', 'Zona de trabajo B', 'WORK_FACE', 'PRODUCTIVE', -85),
    ('Z05-C', 'Zona de trabajo C', 'WORK_FACE', 'PRODUCTIVE', -85),
    ('Z06', 'Colación', 'LUNCH', 'BREAK', -127);

INSERT INTO protege.gateways
    (gateway_address, gateway_id, gateway_name, zone_id, site_id,
     latitude, longitude, installation_height_m, valid_from)
VALUES
    ('AA:00:00:00:00:01', 'GW-ACCESS-01', 'Scanner acceso', 'Z01', 'SIM-01', NULL, NULL, 2.5, now64(3)),
    ('AA:00:00:00:00:02', 'GW-CHANGE-01', 'Scanner casa de cambio', 'Z02', 'SIM-01', NULL, NULL, 2.5, now64(3)),
    ('AA:00:00:00:00:03', 'GW-BRIEF-01', 'Scanner reunión', 'Z03', 'SIM-01', NULL, NULL, 2.5, now64(3)),
    ('AA:00:00:00:00:04', 'GW-TOOLS-01', 'Scanner pañol', 'Z04', 'SIM-01', NULL, NULL, 2.5, now64(3)),
    ('AA:00:00:00:00:05', 'GW-WORK-01', 'Scanner frente de trabajo', 'Z05', 'SIM-01', NULL, NULL, 3.0, now64(3));

INSERT INTO protege.workers
    (tag_address, worker_id, worker_name, contractor, crew, valid_from)
VALUES
    ('BB:00:00:00:00:01', 'W-001', 'Trabajador Simulado 1', 'PULSO', 'Cuadrilla A', now64(3)),
    ('BB:00:00:00:00:02', 'W-002', 'Trabajador Simulado 2', 'PULSO', 'Cuadrilla A', now64(3));
