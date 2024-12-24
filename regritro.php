<?php
$host = "localhost";              
$nombreBD = "DB_Perfumeria";  
$usuario = "postgres";  
$password = "12345";    


$conn = pg_connect("host=$host dbname=$nombreBD user=$usuario password=$password");

if (!$conn) {
    echo "Error: No se pudo conectar a la base de datos.";
    exit;
}
echo "Conexión exitosa a la base de datos.";

$cliente_ci = $_POST['cedula'];
$nombre = $_POST['nombre'];
$mail = $_POST['email'];
$password = $_POST['password'];

$query = "INSERT INTO usuarios(id, username, email, password) 
          VALUES ('$cliente_ci', '$nombre', '$mail', '$password')";

$result = pg_query($conn, $query);

if ($result) {
    echo "Usuario registrado exitosamente.";
    header("Location: index.html");
} else {
    echo "Error al registrar el usuario.";
}

pg_close($conn);
?>