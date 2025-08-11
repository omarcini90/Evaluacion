-- Crear tabla personas_bloqueadas
CREATE TABLE IF NOT EXISTS personas_bloqueadas (
    id SERIAL PRIMARY KEY,
    nombre_completo TEXT NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos iniciales (al menos 10 nombres)
INSERT INTO personas_bloqueadas (nombre_completo) VALUES
    ('Juan Pérez González'),
    ('María García López'),
    ('Carlos Rodríguez Martín'),
    ('Ana Fernández Ruiz'),
    ('Luis Martínez Sánchez'),
    ('Carmen Jiménez Torres'),
    ('Francisco Moreno Díaz'),
    ('Isabel Álvarez Romero'),
    ('Pedro Gómez Navarro'),
    ('Lucía Herrera Castro'),
    ('Miguel Ángel Ortega Vega'),
    ('Rosa María Delgado Prieto')
ON CONFLICT (nombre_completo) DO NOTHING;
