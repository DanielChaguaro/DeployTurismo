CREATE DATABASE TurismoPrueba;
GO

USE TurismoPrueba;
GO


CREATE TABLE Usuario (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) NOT NULL UNIQUE,
    contrasena NVARCHAR(200) NOT NULL,
    preferencias NVARCHAR(200) NULL -- Ej: 'aventura,cultura'
);

CREATE TABLE Destino (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    region NVARCHAR(100) NULL,
    temporada_recomendada NVARCHAR(100) NULL -- Ej: 'verano,invierno'
);

CREATE TABLE Actividad (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    destino_id INT NOT NULL,
    precio FLOAT NOT NULL,
    CONSTRAINT FK_Actividad_Destino FOREIGN KEY (destino_id) REFERENCES Destino(id)
);

CREATE TABLE Reserva (
    id INT PRIMARY KEY IDENTITY(1,1),
    usuario_id INT NOT NULL,
    actividad_id INT NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Reserva_Usuario FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    CONSTRAINT FK_Reserva_Actividad FOREIGN KEY (actividad_id) REFERENCES Actividad(id)
);

CREATE TABLE Comentario (
    id INT PRIMARY KEY IDENTITY(1,1),
    usuario_id INT NOT NULL,
    actividad_id INT NOT NULL,
    texto TEXT NOT NULL,
    calificacion INT NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    CONSTRAINT FK_Comentario_Usuario FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    CONSTRAINT FK_Comentario_Actividad FOREIGN KEY (actividad_id) REFERENCES Actividad(id)
);
select * from Usuario
select * from Destino
select * from Reserva
select * from Actividad
-- Insertar datos en la tabla Usuario
INSERT INTO Usuario (nombre, email, contrasena, preferencias) VALUES
('Daniel Chaguaro', 'daniel@example.com', 'password123', 'aventura,cultura'),
('Ana López', 'ana@example.com', 'password456', 'naturaleza,playa'),
('Carlos Pérez', 'carlos@example.com', 'password789', 'ecoturismo,gastronomía'),
('María García', 'maria@example.com', 'password321', 'historia,cultura'),
('Juan Torres', 'juan@example.com', 'password654', 'aventura,naturaleza');

-- Insertar datos en la tabla Destino
INSERT INTO Destino (nombre, descripcion, region, temporada_recomendada) VALUES
('Galápagos', 'Islas reconocidas por su biodiversidad única.', 'Insular', 'verano'),
('Cotopaxi', 'El volcán activo más alto del mundo.', 'Sierra', 'invierno'),
('Baños', 'Un paraíso de cascadas y deportes extremos.', 'Sierra', 'verano'),
('Montañita', 'El destino perfecto para surf y vida nocturna.', 'Costa', 'invierno'),
('Cuenca', 'Una ciudad colonial con mucha historia.', 'Sierra', 'todo el año');

INSERT INTO Actividad (nombre, descripcion, destino_id, precio) VALUES
('Tour de Snorkel', 'Explora la biodiversidad marina de las islas. aventura, naturaleza, ecoturismo, playa', 1, 120.00)

-- Insertar datos en la tabla Actividad
INSERT INTO Actividad (nombre, descripcion, destino_id, precio) VALUES
('Tour de Snorkel', 'Explora la biodiversidad marina de las islas. aventura, naturaleza, ecoturismo, playa', 1, 120.00),
('Escalada al Volcán', 'Una experiencia única en el Cotopaxi. aventura, naturaleza', 2, 80.00),
('Bicicleta en las Cascadas', 'Un recorrido en bicicleta por las cascadas de Baños. aventura, naturaleza, ecoturismo', 3, 50.00),
('Clases de Surf', 'Aprende a surfear con profesionales en Montañita. aventura, naturaleza, playa', 4, 100.00),
('Recorrido Histórico', 'Conoce los lugares emblemáticos de Cuenca.cultura ', 5, 60.00);

Select * from Actividad

-- Insertar datos en la tabla Reserva
INSERT INTO Reserva (usuario_id, actividad_id, fecha) VALUES
(1, 1, '2024-12-01'),
(2, 2, '2024-12-02'),
(3, 3, '2024-12-03'),
(4, 4, '2024-12-04'),
(5, 5, '2024-12-05');

INSERT INTO Reserva (usuario_id, actividad_id, fecha) VALUES
(2, 3, '2024-12-01')


select * from Usuario
update()
-- Insertar datos en la tabla Comentario
INSERT INTO Comentario (usuario_id, actividad_id, texto, calificacion) VALUES
(1, 1, 'Increíble experiencia, la fauna marina es espectacular.', 5),
(2, 2, 'Desafiante pero totalmente vale la pena.', 4),
(3, 3, 'El paisaje es increíble, muy recomendable.', 5),
(4, 4, 'Clases muy divertidas, aprendí mucho.', 4),
(5, 5, 'Cuenca es hermosa, el tour fue muy informativo.', 5);


SELECT a.nombre AS Actividad, d.nombre AS Destino, a.precio AS Precio
FROM Reserva r
JOIN Actividad a ON r.actividad_id = a.id
JOIN Destino d ON a.destino_id = d.id
WHERE r.usuario_id = 1;

select count(actividad_id) from Reserva group by actividad_id

SELECT TRIM(value) AS preferencias, COUNT(*) AS total_usuarios  
FROM Usuario
CROSS APPLY STRING_SPLIT(preferencias, ',')  
GROUP BY TRIM(value)  
ORDER BY total_usuarios DESC; 

SELECT r.actividad_id, d.temporada_recomendada, COUNT(r.id) AS total_reservas
FROM Reserva r
INNER JOIN Actividad a ON r.actividad_id = a.id
INNER JOIN Destino d ON a.destino_id = d.id
GROUP BY r.actividad_id, d.temporada_recomendada
ORDER BY total_reservas DESC; 