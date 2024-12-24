const express = require('express');
const bodyParser = require('body-parser');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');

const app = express();
const port = 3000;

// Configuración de la base de datos
const pool = new Pool({
  user: 'tu_usuario',
  host: 'localhost',
  database: 'perlis_store',
  password: 'tu_contraseña',
  port: 5432,
});

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));

// Ruta para manejar el registro
app.post('/registro', async (req, res) => {
  const { username, email, password } = req.body;

  try {
    // Encriptar la contraseña
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insertar el usuario en la base de datos
    const query = 'INSERT INTO usuarios (username, email, password) VALUES ($1, $2, $3)';
    await pool.query(query, [username, email, hashedPassword]);

    res.send('Usuario registrado exitosamente');
  } catch (error) {
    console.error('Error al registrar usuario:', error);
    res.status(500).send('Error al registrar usuario');
  }
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
