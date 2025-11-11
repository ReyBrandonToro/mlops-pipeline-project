# 🚀 GUÍA COMPLETA: SUBIR CAMBIOS A LA RAMA DEVELOPER

## 📋 Resumen de Cambios Preparados

### ✅ Archivos Optimizados
1. **`.gitignore`** - Actualizado con reglas completas para MLOps
2. **`requirements.txt`** - Actualizado con versiones específicas de todas las librerías
3. **Eliminado `set_up.bat`** - Archivo redundante removido
4. **Conservados:**
   - `setup.bat` - Configuración inicial simple
   - `iniciar_sistema.bat` - Inicio automático del sistema

### 📁 Archivos que NO se subirán (según .gitignore)
- ❌ `mlops_pipeline-venv/` - Entorno virtual
- ❌ `__pycache__/` - Archivos compilados de Python
- ❌ `*.joblib` - Modelos entrenados (muy pesados)
- ❌ `*.csv` - Datasets (deben descargarse aparte)
- ❌ `*.png` - Visualizaciones (se regeneran)
- ❌ `prompts/` - Notas de desarrollo
- ❌ `tatus` - Archivo temporal de Git
- ❌ `COMMANDS.txt` - Comandos locales
- ❌ `RESUMEN_VISUAL*.txt` - Reportes visuales locales

---

## 🔍 PASO 1: Verificar Estado Actual

```bash
# Ver qué archivos han cambiado
git status

# Ver cambios específicos en archivos modificados
git diff .gitignore
git diff requirements.txt
git diff readme.md
```

**Salida Esperada:**
- Archivos modificados (M): .gitignore, requirements.txt, etc.
- Archivos nuevos (??): app_frontend.py, documentación, etc.
- Archivos eliminados (D): notebooks antiguos, set_up.bat

---

## 🧹 PASO 2: Limpiar Archivos No Deseados

```bash
# Eliminar archivos temporales que no deben subirse
git rm --cached tatus 2>$null

# Verificar que los archivos ignorados no estén en staging
git status --ignored
```

---

## ➕ PASO 3: Agregar Archivos al Staging Area

### Opción A: Agregar Selectivamente (Recomendado)

```bash
# 1. Agregar archivos de configuración actualizados
git add .gitignore
git add requirements.txt
git add readme.md
git add config.json

# 2. Agregar código fuente principal
git add mlops_pipeline/src/*.py
git add mlops_pipeline/src/__init__.py

# 3. Agregar scripts de utilidad
git add setup.bat
git add iniciar_sistema.bat
git add run_training.py
git add test_api.py
git add main.py

# 4. Agregar ejemplos
git add examples/

# 5. Agregar documentación importante
git add CHECKLIST.md
git add QUICKSTART.md
git add PROJECT_SUMMARY.md
git add EJECUCION_EXITOSA.md
git add EJECUCION_COMPLETA.md
git add INSTRUCCIONES_FRONTEND.md
git add SISTEMA_COMPLETO.md
git add ANALISIS_ARCHIVOS_BAT.md

# 6. Agregar Docker (si quieres incluirlo)
git add Dockerfile
git add docker-compose.yml
git add sonar-project.properties

# 7. Agregar GitHub workflows (si existen)
git add .github/
```

### Opción B: Agregar Todo (Más Rápido)

```bash
# Agregar todos los cambios (el .gitignore filtrará lo no deseado)
git add -A
```

---

## 🗑️ PASO 4: Registrar Eliminaciones

```bash
# Confirmar eliminación de set_up.bat
git rm set_up.bat

# Confirmar eliminación de notebooks antiguos (si aplica)
git rm mlops_pipeline/src/Cargar_comprension_eda.ipynb 2>$null
git rm mlops_pipeline/src/cargar_datos.ipynb 2>$null
git rm mlops_pipeline/src/model_deploy.ipynb 2>$null
git rm mlops_pipeline/src/model_evaluation.ipynb 2>$null
git rm mlops_pipeline/src/model_monitoring.ipynb 2>$null
git rm mlops_pipeline/src/model_training.ipynb 2>$null
git rm mlops_pipeline/src/heuristic_model.py 2>$null
```

---

## 📝 PASO 5: Verificar Staging Area

```bash
# Ver qué archivos están listos para commit
git status

# Ver un resumen más compacto
git status --short

# Contar archivos por tipo de cambio
git status --short | Select-String "^M " | Measure-Object  # Modificados
git status --short | Select-String "^A " | Measure-Object  # Agregados
git status --short | Select-String "^D " | Measure-Object  # Eliminados
```

**Verificaciones Importantes:**
- ✅ NO debe aparecer `mlops_pipeline-venv/`
- ✅ NO debe aparecer `__pycache__/`
- ✅ NO deben aparecer `.joblib`, `.csv`, `.png`
- ✅ SÍ deben aparecer archivos `.py`, `.md`, `.bat`

---

## 💾 PASO 6: Crear Commit

```bash
# Commit con mensaje descriptivo
git commit -m "feat: Implementar sistema completo de detección de fraude con frontend

- Agregado frontend interactivo con Streamlit
- Implementada API REST con FastAPI
- Adaptación completa a dataset real (financial_fraud_dataset.csv)
- 3 modelos entrenados: LogisticRegression, RandomForest, XGBoost
- Mejor modelo: LogisticRegression (ROC-AUC: 0.5776)
- Documentación completa del sistema
- Scripts de inicio automatizado
- Optimizado .gitignore y requirements.txt
- Eliminados archivos redundantes y notebooks obsoletos

Componentes:
- mlops_pipeline/src/app_frontend.py: Frontend Streamlit
- mlops_pipeline/src/model_deploy.py: API FastAPI
- mlops_pipeline/src/cargar_datos.py: Carga de datos
- mlops_pipeline/src/data_validation.py: Validación
- mlops_pipeline/src/ft_engineering.py: Feature engineering
- mlops_pipeline/src/model_training_evaluation.py: Entrenamiento
- iniciar_sistema.bat: Script de inicio automático
- setup.bat: Configuración inicial
- test_api.py: Tests automatizados

Archivos actualizados:
- requirements.txt: Versiones específicas de todas las librerías
- .gitignore: Reglas completas para proyectos MLOps
- readme.md: Documentación actualizada"
```

**Alternativa - Commit más corto:**

```bash
git commit -m "feat: Sistema completo de detección de fraude con API + Frontend

- Frontend Streamlit interactivo
- API REST con FastAPI
- 3 modelos ML (mejor: LogisticRegression ROC-AUC 0.5776)
- Documentación completa
- Scripts automatizados
- Optimizaciones .gitignore y requirements.txt"
```

---

## 🌿 PASO 7: Verificar Rama Actual

```bash
# Ver en qué rama estás
git branch

# Ver todas las ramas (locales y remotas)
git branch -a

# Si no estás en developer, cambiarte
git checkout developer

# O crear la rama developer si no existe
git checkout -b developer
```

---

## 🔄 PASO 8: Sincronizar con Remoto

```bash
# Obtener últimos cambios del remoto (sin hacer merge)
git fetch origin developer

# Ver si hay conflictos potenciales
git status

# Si hay cambios remotos, hacer pull con rebase (mantiene historial limpio)
git pull origin developer --rebase

# Si hay conflictos, resolverlos y continuar
# git add <archivo-con-conflicto>
# git rebase --continue
```

---

## 🚀 PASO 9: Subir Cambios a GitHub

```bash
# Subir cambios a la rama developer
git push origin developer

# Si es la primera vez que subes esta rama
git push -u origin developer

# Si hay problemas de force push (SOLO SI ESTÁS SEGURO)
# git push origin developer --force-with-lease
```

**Salida Esperada:**
```
Enumerating objects: 45, done.
Counting objects: 100% (45/45), done.
Delta compression using up to 8 threads
Compressing objects: 100% (35/35), done.
Writing objects: 100% (40/40), 25.43 KiB | 2.54 MiB/s, done.
Total 40 (delta 12), reused 0 (delta 0), pack-reused 0
To https://github.com/ReyBrandonToro/mlops-pipeline-project.git
   abc1234..def5678  developer -> developer
```

---

## ✅ PASO 10: Verificar en GitHub

1. **Ir a GitHub:** https://github.com/ReyBrandonToro/mlops-pipeline-project
2. **Cambiar a rama developer:** Usar el selector de ramas
3. **Verificar archivos subidos:**
   - ✅ Código fuente en `mlops_pipeline/src/`
   - ✅ Scripts `.bat`
   - ✅ Documentación `.md`
   - ✅ `requirements.txt` actualizado
   - ✅ `.gitignore` optimizado
   - ❌ NO debe haber `mlops_pipeline-venv/`
   - ❌ NO debe haber archivos `.joblib`, `.csv`, `.png`

---

## 🔀 PASO 11 (OPCIONAL): Crear Pull Request

Si quieres fusionar `developer` con `main`:

1. **En GitHub:**
   - Ir a la pestaña "Pull requests"
   - Click en "New pull request"
   - Base: `main` ← Compare: `developer`
   - Click en "Create pull request"

2. **Agregar descripción:**
   ```
   ## 🛡️ Sistema Completo de Detección de Fraude

   ### Cambios Principales
   - ✅ Frontend interactivo con Streamlit
   - ✅ API REST con FastAPI
   - ✅ Pipeline MLOps completo
   - ✅ 3 modelos entrenados
   - ✅ Documentación exhaustiva

   ### Métricas del Modelo
   - Mejor Modelo: LogisticRegression
   - ROC-AUC: 0.5776
   - Recall: 65.79%
   - Accuracy: 51.20%

   ### Archivos Clave
   - `mlops_pipeline/src/app_frontend.py`
   - `mlops_pipeline/src/model_deploy.py`
   - `iniciar_sistema.bat`
   - `requirements.txt` (actualizado)
   ```

3. **Revisar y aprobar:**
   - Revisar cambios
   - Resolver conflictos si existen
   - Click en "Merge pull request"

---

## 🚨 Solución de Problemas

### Problema 1: Archivos grandes bloqueados

**Síntoma:**
```
remote: error: File mlops_pipeline-venv/... is 123.45 MB; this exceeds GitHub's file size limit of 100.00 MB
```

**Solución:**
```bash
# Verificar que .gitignore incluye mlops_pipeline-venv/
git rm -r --cached mlops_pipeline-venv/
git commit -m "Remove virtual environment from tracking"
git push origin developer
```

### Problema 2: Credenciales de GitHub

**Síntoma:**
```
fatal: Authentication failed
```

**Solución:**
```bash
# Configurar credenciales
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@example.com"

# Usar Personal Access Token en lugar de contraseña
# 1. Ir a GitHub > Settings > Developer settings > Personal access tokens
# 2. Generate new token (classic)
# 3. Seleccionar scopes: repo
# 4. Copiar el token
# 5. Usar el token como contraseña cuando Git lo pida
```

### Problema 3: Conflictos al hacer pull

**Síntoma:**
```
CONFLICT (content): Merge conflict in readme.md
```

**Solución:**
```bash
# 1. Abrir el archivo con conflicto en VS Code
# 2. Resolver manualmente (aceptar incoming, current, o ambos)
# 3. Guardar el archivo
# 4. Agregar el archivo resuelto
git add readme.md
git commit -m "Resolve merge conflict in readme.md"
git push origin developer
```

### Problema 4: Commit rechazado por historial divergente

**Síntoma:**
```
! [rejected]        developer -> developer (non-fast-forward)
```

**Solución:**
```bash
# Opción 1: Pull con rebase (recomendado)
git pull origin developer --rebase
git push origin developer

# Opción 2: Merge (crea commit adicional)
git pull origin developer
git push origin developer

# Opción 3: Force push (SOLO si estás seguro)
git push origin developer --force-with-lease
```

---

## 📊 Checklist Final

Antes de hacer push, verificar:

- [ ] `.gitignore` está actualizado y optimizado
- [ ] `requirements.txt` tiene versiones específicas
- [ ] No hay archivos grandes (>100MB) en staging
- [ ] No hay archivos sensibles (contraseñas, tokens)
- [ ] El entorno virtual NO está incluido
- [ ] Los modelos `.joblib` NO están incluidos
- [ ] Los datasets `.csv` NO están incluidos
- [ ] Las imágenes `.png` NO están incluidas
- [ ] El mensaje de commit es descriptivo
- [ ] Estás en la rama `developer`
- [ ] Has hecho `git fetch` y `git pull` antes de push
- [ ] Has probado el código localmente

---

## 🎯 Comando Completo (Todo en Uno)

Para ejecutar todo de una vez (SOLO si estás seguro):

```bash
# Limpiar y preparar
git rm --cached tatus 2>$null
git rm set_up.bat

# Agregar todos los cambios (el .gitignore filtrará)
git add -A

# Commit
git commit -m "feat: Sistema completo de detección de fraude con API + Frontend

- Frontend Streamlit interactivo
- API REST con FastAPI  
- 3 modelos ML (mejor: LogisticRegression ROC-AUC 0.5776)
- Documentación completa
- Scripts automatizados
- Optimizaciones .gitignore y requirements.txt"

# Sincronizar y subir
git pull origin developer --rebase
git push origin developer
```

---

## 🎓 Buenas Prácticas

1. **Commits Frecuentes:** Hacer commits pequeños y frecuentes
2. **Mensajes Descriptivos:** Usar formato: `tipo: descripción breve`
   - `feat:` - Nueva funcionalidad
   - `fix:` - Corrección de bug
   - `docs:` - Cambios en documentación
   - `refactor:` - Refactorización de código
   - `test:` - Agregar tests
   - `chore:` - Tareas de mantenimiento

3. **Revisar Antes de Commit:** Siempre ejecutar `git status` y `git diff`
4. **No Subir Archivos Grandes:** Usar Git LFS para archivos >50MB
5. **Proteger Ramas:** Configurar branch protection en GitHub para `main`
6. **Pull Requests:** Usar PRs para revisión de código antes de merge

---

## 📚 Recursos Adicionales

- **Git Cheat Sheet:** https://education.github.com/git-cheat-sheet-education.pdf
- **Conventional Commits:** https://www.conventionalcommits.org/
- **Git LFS:** https://git-lfs.github.com/
- **GitHub Docs:** https://docs.github.com/

---

**¡Listo para subir! 🚀**

Ejecuta los comandos paso a paso y verifica cada resultado antes de continuar.
