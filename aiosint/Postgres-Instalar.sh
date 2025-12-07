# Instalar PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Iniciar y habilitar el servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear usuario y base de datos para n8n
sudo -u postgres psql <<EOF
CREATE USER n8n WITH PASSWORD 'tu_password_aqui';
CREATE DATABASE n8n_db OWNER n8n;
GRANT ALL PRIVILEGES ON DATABASE n8n_db TO n8n;
EOF

# Conectar y crear la tabla
sudo -u postgres psql -d n8n_db <<EOF
CREATE TABLE agente_smith (
    id SERIAL PRIMARY KEY,
    correo TEXT UNIQUE,
    datos JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
GRANT ALL PRIVILEGES ON TABLE agente_smith TO n8n;
GRANT USAGE, SELECT ON SEQUENCE agente_smith_id_seq TO n8n;
EOF
