# Plan de Contingencia - Demostracion Gerardito IA

## Riesgos y Respuestas

| Riesgo | Prevencion | Respuesta preparada |
|--------|------------|---------------------|
| Servicio dormido | Calentar 15 min antes de la demostracion | Verificar `/health` y `/metrics`. Si no responde, reintentar cada 30s hasta 3 min. Si persiste, usar evidencia documentada. |
| Tokens o cuota agotada | Revisar panel de Ollama Cloud, reservar presupuesto, limitar consumo previo | Mostrar error controlado 429 al usuario. Explicar que es limitacion del proveedor. Continuar con demostracion documentando la causa. |
| DNS, SSL o release incorrecto | Probar URL y version desde otra red 24h antes | Si falla, usar version anterior estable. Documentar evidencia del incidente. |
| Datos o almacenamiento | Sembrar datos de prueba y verificar conexion PostgreSQL | Caso alternativo: mostrar estructura de DB y esquema. No modificar datos reales. |
| Sesion vencida en Ollama | Validar cuenta y permisos antes de la demo | Reingreso rapido con credenciales protegidas. No exponer en pantalla. |
| CORS o migracion | Probar produccion despues del release | Rollback a version estable via `git checkout v1.0.0` + redeploy. |
| API externa lenta (Ollama) | Timeout de 120s + reintentos controlados | Mensaje controlado al usuario: "El servicio de IA esta tardando mas de lo esperado". Evidencia de dependencia externa. |
| Red o audiovisual | Probar red, audio, pantalla y navegador antes | Segundo equipo o red de respaldo. Copia local de la presentacion. |

## Verificaciones Programadas

### 24 horas antes
- [ ] Congelar release (no mas commits)
- [ ] Probar recorrido completo del flujo
- [ ] Revisar que no haya secretos expuestos en GitHub
- [ ] Generar respaldo de la base de datos

### 2 horas antes
- [ ] Confirmar URL accesible desde red externa
- [ ] Verificar datos de prueba en PostgreSQL
- [ ] Revisar panel de Ollama Cloud (saldo, cuota, vencimiento)
- [ ] Confirmar pipeline de CI verde
- [ ] Verificar que el dominio resuelve correctamente

### 15 minutos antes
- [ ] Calentar el servicio (hacer 3-5 llamadas a `/health` y `/validar-texto`)
- [ ] Iniciar sesion en herramientas de monitoreo
- [ ] Cerrar notificaciones del navegador
- [ ] Abrir pestanas preparadas (URL, Swagger, GitHub, metricas)

### Al finalizar
- [ ] No exponer credenciales en pantalla ni en grabaciones
- [ ] Registrar cualquier incidente en el acta
- [ ] Conservar la version evaluada (tag v1.0.0)

## Contacto de Emergencia

- **Equipo:** Comunicacion directa por canal del grupo
- **Proveedor Ollama:** soporte@ollama.com (documentar ticket si hay incidente)
- **Oracle Cloud:** Portal de soporte (si hay problema de infraestructura)

## Evidencia de Respaldo

En caso de contingencia externa verificable, se mostrara:
1. Captura del error con timestamp
2. Evidencia de que el servicio funcionaba previamente
3. Logs relevantes del backend
4. Decision del docente sobre como proceder
