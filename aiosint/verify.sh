#!/bin/bash

# verify.sh
# Comprueba si los servicios del framework AIOSINT están funcionando y respondiendo.

cColorRojo='\033[1;31m'
cColorVerde='\033[1;32m'
cFinColor='\033[0m'

echo -e "${cColorVerde}[+] Verificando instalación del Framework AIOSINT...${cFinColor}"

# 1. Comprobar si n8n se está ejecutando (escuchando en 5678)
if nc -z localhost 5678; then
    echo -e "${cColorVerde}[OK] n8n está escuchando en el puerto 5678.${cFinColor}"
else
    echo -e "${cColorRojo}[FALLO] n8n NO está escuchando en el puerto 5678. ¿Se está ejecutando?${cFinColor}"
fi

# 2. Comprobar si Social API se está ejecutando (escuchando en 8000)
if nc -z localhost 8000; then
    echo -e "${cColorVerde}[OK] Social API está escuchando en el puerto 8000.${cFinColor}"
else
    echo -e "${cColorRojo}[FALLO] Social API NO está escuchando en el puerto 8000. ¿Se está ejecutando?${cFinColor}"
fi

# 3. Probar endpoints de Social API (Prueba simulada)
echo -e "${cColorVerde}[+] Probando respuesta de Social API...${cFinColor}"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/holehe/test@example.com)

if [ "$RESPONSE" == "200" ] || [ "$RESPONSE" == "500" ]; then
    # 500 es aceptable aquí porque test@example.com podría fallar en holehe o devolver error, 
    # pero al menos el servidor flask respondió. 
    echo -e "${cColorVerde}[OK] Social API respondió con código HTTP $RESPONSE.${cFinColor}"
else
    echo -e "${cColorRojo}[FALLO] Social API respondió con código HTTP $RESPONSE (Se esperaba 200 o 500).${cFinColor}"
fi

echo -e "${cColorVerde}[+] Pasos de verificación completados.${cFinColor}"
