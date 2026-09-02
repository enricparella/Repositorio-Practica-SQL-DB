# Práctica Obligatoria — Bases de Datos

Este directorio contiene la práctica obligatoria correspondiente al bloque de Bases de Datos, SQL y BigQuery.

La entrega está dividida en dos partes principales.

## Parte I — SQL Murder Mystery

La primera parte de la práctica se encuentra en:

`Parte_I_SQL_Game.ipynb`

En este Jupyter Notebook se desarrolla y resuelve el ejercicio **SQL Murder Mystery** utilizando la base de datos:

`data/sql-murder-mystery.db`

El propio notebook contiene el proceso completo de resolución del caso, incluyendo:

- Las consultas SQL realizadas durante la investigación.
- El análisis de los resultados obtenidos.
- El razonamiento seguido para avanzar entre las distintas pistas.
- La identificación y solución final del caso.

> **Importante:** la respuesta final del SQL Murder Mystery se encuentra dentro de `Parte_I_SQL_Game.ipynb`. No existe un archivo independiente con la solución.

---

## Parte II — Modelo de Base de Datos

La segunda parte de la práctica se encuentra dentro del directorio:

`Práctica Modelo DB/`

El notebook principal correspondiente a esta parte es:

`Práctica Modelo DB/Parte_II_Modelo_BD.ipynb`

Esta carpeta contiene además los archivos necesarios para la ejecución del proyecto, incluyendo su código fuente, configuración y dependencias.

---

## Estructura principal

```text
03_Practica_Obligatoria/
│
├── data/
│   └── sql-murder-mystery.db
│
├── material_extra/
│
├── Práctica Modelo DB/
│   ├── src/
│   ├── .env.example
│   ├── .gitignore
│   ├── Parte_II_Modelo_BD.ipynb
│   ├── README.md
│   └── requirements.txt
│
├── .env.example
├── .gitignore
├── guia_tc_sql.html
├── Parte_I_SQL_Game.ipynb
├── requirements.txt
└── README_Entrega.md
```

## Entrega

Para revisar la práctica:

1. Consultar `Parte_I_SQL_Game.ipynb` para la resolución completa del SQL Murder Mystery.

2. Consultar `Práctica Modelo DB/Parte_II_Modelo_BD.ipynb` para el enunciado y desarrollo de la segunda parte de la práctica. El código desarrollado se encuentra dentro de `Práctica Modelo DB/src/`.

3. El modelo de BigQuery puede crearse y poblarse automáticamente mediante `src/seed.py`. Desde el directorio `Práctica Modelo DB/`, puede ejecutarse con:

```bash
python src/seed.py --project <PROJECT_ID> --dataset <DATASET_ID> --customers 500 --orders 2000
```

4. El directorio `Práctica Modelo DB/` contiene además el `README.md` específico de esta parte, las dependencias y los archivos de configuración necesarios para su ejecución.