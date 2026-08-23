# Procedimiento de Rollback - Gerardito IA

## Cuando usar rollback

- La URL publica no funciona despues de un deploy
- El flujo principal falla con errores 500
- La base de datos tiene problemas de conexion
- Ollama Cloud no responde y el fallback no funciona

## Procedimiento

### 1. Identificar version estable

```bash
# Ver tags disponibles
git tag -l

# Ver commits recientes
git log --oneline -10
```

Version estable conocida: `v1.0.0` (commit `4a4896a7e547b36e7374bfdf40439858ad09b211`)

### 2. Checkout a version estable

```bash
git checkout v1.0.0
```

### 3. Redeploy

```bash
# Detener servicios actuales
docker compose down

# Reconstruir y levantar
docker compose up -d --build

# Verificar que los servicios estan levantados
docker compose ps
```

### 4. Verificar

```bash
# Health check
curl -f https://gerarditougb.qd.je/api/v1/health

# Metadata
curl -f https://gerarditougb.qd.je/api/v1/metadata

# Flujo principal
curl -f -X POST https://gerarditougb.qd.je/api/v1/validar-texto \
  -H "Content-Type: application/json" \
  -d '{"texto": "programacion", "tipo": "habilidad"}'
```

### 5. Si hay problemas de base de datos

```bash
# Verificar conexion
docker compose exec postgres pg_isready -U gerardito -d gerardito_db

# Si es necesario, recrear la DB (PERDERA DATOS)
docker compose down -v
docker compose up -d postgres
sleep 10
docker compose up -d
```

### 6. Notificar

- Informar al equipo sobre el rollback
- Documentar el motivo en el acta
- Conservar logs del error para analisis posterior

## Rollback automatico (futuro)

Si se implementa CI/CD con health checks automaticos:
- GitHub Actions puede detectar fallos post-deploy
- Automaticamente hacer rollback a la version anterior
- Notificar al equipo por canal de comunicacion

## Versiones conocidas estables

| Tag | Commit | Fecha | Notas |
|-----|--------|-------|-------|
| v1.0.0 | 970de8b509cb5b03f2193de98ba94d7da7d218a2 | 2026-08-22 | Producto final Modulo 4 |
