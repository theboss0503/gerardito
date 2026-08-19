#!/bin/bash

set -e

PROJECT_DIR="/home/opc/repositorios/gerardito"

echo "======================================"
echo " Iniciando despliegue de Gerardito"
echo "======================================"

cd "$PROJECT_DIR"

echo ""
echo "[1/5] Actualizando código..."
git fetch origin main
git reset --hard origin/main

echo ""
echo "[2/5] Construyendo imágenes..."
docker compose build

echo ""
echo "[3/5] Levantando servicios..."
docker compose up -d

echo ""
echo "[4/5] Estado de los contenedores..."
docker compose ps

echo ""
echo "[5/5] Limpiando imágenes no utilizadas..."
docker image prune -f

echo ""
echo "======================================"
echo " Despliegue completado correctamente"
echo "======================================"
