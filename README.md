# Forecasting for Data Science

Curso profesional y reproducible de **Time Series Forecasting y MLOps**, junto con la monografía académica, la presentación y el sílabo derivados de él. Ocho datasets reales, ocho notebooks ejecutados de principio a fin, una monografía de 122 páginas y una presentación interactiva en HTML.

## Estructura

| Carpeta | Contenido |
|---|---|
| [`forecasting-for-data-science/`](forecasting-for-data-science) | El curso completo: datos curados (`data/`), notebooks ejecutados (`notebooks/`), scripts de descarga/limpieza/validación (`scripts/`), tests y documentación (`docs/`). Ver su [README](forecasting-for-data-science/README.md). |
| [`monografia/`](monografia) | Monografía aplicada (PDF, 122 pp.) y presentación técnica (PDF, 25 pp.) sobre los ocho experimentos del curso. Solo artefactos compilados; ver su [README](monografia/README.md). |
| [`presentacion-interactiva/`](presentacion-interactiva) | Versión HTML interactiva autocontenida de la monografía. |
| [`silabo/`](silabo) | Sílabo del curso y criterios de calificación, en PDF. |

## La tesis central

La complejidad no garantiza mejora: en cuatro de los ocho experimentos del curso, el modelo sofisticado iguala o apenas supera a un baseline ingenuo (seasonal naive, ETS). La monografía y la presentación documentan esta conclusión capítulo por capítulo, dataset por dataset.

## Datasets y resultados (resumen)

| Semana | Dataset | Técnica central | Resultado |
|---:|---|---|---|
| 1 | Metro Interstate Traffic | Seasonal naive, ETS | Seasonal Naive 168 competitivo frente a modelos más complejos |
| 2 | Appliances Energy | ARIMA, ETS, Theta | ETS superó al ARIMA seleccionado por AIC |
| 3 | Beijing PM2.5 | SARIMA vs SARIMAX | SARIMAX redujo MAE 18.4% (escenario oracle) |
| 4 | Bike Sharing | LightGBM + feature engineering | MASE medio 0.457 |
| 5 | Electricity (370 series) | Modelos globales, cross-learning | Cold-start: sin contexto histórico no se recupera la escala de clientes nuevos |
| 6 | OPSD Germany | PyTorch LSTM | LightGBM superó a LSTM bajo este protocolo |
| 7 | PeMS-SF (963 sensores) | N-BEATS, TFT-like | TFT-like MAE 0.013122 transfiriendo a sensores nuevos |
| 8 | M3 Monthly | Quantile LightGBM | CRPS ≈ 356.27, cobertura empírica P10–P90 ≈ 0.789 |

Detalle completo en [`forecasting-for-data-science/README.md`](forecasting-for-data-science/README.md) y en la monografía.

## Datasets grandes (Git LFS)

Dos datasets superan el límite de 100 MB de GitHub y se versionan con **Git LFS**:

- `forecasting-for-data-science/data/05_electricity/electricity_long.csv` (~404 MB)
- `forecasting-for-data-science/data/07_traffic_pems/traffic_pems.csv` (~409 MB)

Para clonar con estos archivos:

```bash
git lfs install
git clone <url-de-este-repo>
```

Sin Git LFS instalado, el clon trae solo los punteros de texto de esos dos archivos; el resto del repositorio (notebooks, docs, demás datasets, PDFs) funciona igual.

## Licencia y atribución

El código y la documentación original se distribuyen bajo licencia **MIT** (ver [`LICENSE`](LICENSE)). Los datasets incluidos conservan sus licencias y requisitos de atribución originales — consulta el `README.md` de cada carpeta en `forecasting-for-data-science/data/` y [`forecasting-for-data-science/docs/SOURCE_NOTES.md`](forecasting-for-data-science/docs/SOURCE_NOTES.md).

Las fuentes Typst (`.typ`) de la monografía, la presentación y el sílabo no se incluyen en este repositorio; solo se publican los PDFs (y la exportación HTML de la monografía) ya compilados.
