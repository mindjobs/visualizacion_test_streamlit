# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

Formato basado en "Keep a Changelog" — y usando versionado semántico cuando aplique.

## [Unreleased]

### Added
- `README.md` con instrucciones para ejecutar la app localmente. (2025-11-18)

### Changed
- `app.py`: manejo de ausencia del archivo de datos y mensajes instructivos. (2025-11-18)
- `app.py`: reemplazado `use_container_width=True` por `width='stretch'` en llamadas a `st.plotly_chart`. (2025-11-18)

### Fixed
- Evitar que la app lance excepción al no encontrar `data/owid-co2-data.csv`. (2025-11-18)

## [2025-11-18] - main
- Inicialización del repositorio con cambios menores y documentación.
