# Russia-Ukraine-War
Data Pipeline from Kobo toolbox to PostgreSQL using Python.


# 🛰️ Russia-Ukraine War: Data Pipeline Project

This project demonstrates a complete **ETL (Extract, Transform, Load)** pipeline built using **KoboToolbox**, **Python**, and **PostgreSQL**, using **Power BI**. It fetches near real-time data about the Russia-Ukraine war, cleans and transforms it using Python, and loads it into a PostgreSQL database for further analysis or dashboarding.


## 📌 Project Overview

This pipeline performs the following steps:

1. **Extract**: Downloads data from a KoboToolbox CSV export link using authentication.
2. **Transform**: Cleans and prepares the data using `pandas`:
   - Standardizes column names
   - Parses and coerces date formats
   - Calculates derived metrics like total soldier casualties
3. **Load**: Pushes the transformed data into a PostgreSQL table under a custom schema.
4. **Visualize**:  Connect to **Power BI** for interactive dashboards and analytics.

---

## 📂 Project Structure

```
Russia-Ukraine-Conflict/
├── .env               # Stores credentials and configuration variables
├── .gitignore         # Git exclusions
├── pipeline.py        # Python script for the ETL process
├── README.md          # Project documentation
├── requirements.txt   # Required Python packages
```

---

## ⚙️ Technologies Used

- **Python 3.10+**
- **Pandas** – Data manipulation and transformation
- **Requests** – HTTP requests to KoboToolbox
- **psycopg2** – PostgreSQL database connection
- **PostgreSQL** – Target relational database
- **KoboToolbox** – Humanitarian data collection platform
- **dotenv** – Environment variable management

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following contents:

```ini
KOBO_USERNAME=your_kobo_username
KOBO_PASSWORD=your_kobo_password
PG_HOST=your_postgres_host
PG_DATABASE=your_database_name
PG_USERNAME=your_postgres_user
PG_PASSWORD=your_postgres_password
PG_PORT=5432
```

---

## 🚀 How to Run the Pipeline

1. Install required libraries:

```bash
pip install -r requirements.txt
```

2. Add your credentials in the `.env` file as shown above.

3. Run the ETL script:

```bash
python pipeline.py
```

---

## 🧠 Key Transformations

- **Date** field is parsed and converted for time-based filtering.
- **Total_Soldier_Casualties** is computed as:

  ```
  Casualties + Injured + Captured
  ```

- Column names are standardized (underscored, lowercase).
- Null or malformed values are handled gracefully.

---

## 🗃️ PostgreSQL Schema & Table

- **Schema**: `war`  
- **Table**: `russia_ukraine_war`

| Field Name               | Type   | Description                             |
|--------------------------|--------|-----------------------------------------|
| start                    | TEXT   | Submission start timestamp              |
| end                      | TEXT   | Submission end timestamp                |
| date                     | DATE   | Event date                              |
| country                  | TEXT   | Country involved                        |
| event                    | TEXT   | Type or description of event            |
| oblast                   | TEXT   | Region (oblast)                         |
| casualties               | INT    | Number of soldier casualties            |
| injured                  | INT    | Number of injured soldiers              |
| captured                 | INT    | Number of captured personnel            |
| civilian_casualties      | INT    | Number of civilian casualties           |
| new_recruits             | INT    | Reported new recruits                   |
| combat_intensity         | FLOAT  | Conflict intensity (0–10 scale)         |
| territory_status         | TEXT   | Territory status                        |
| percentage_occupied      | FLOAT  | Percent of oblast occupied              |
| area_occupied            | FLOAT  | Area occupied (in sq. km or units)      |
| Total_Soldier_Casualties | INT    | Computed field: casualties + injured + captured |

---

## 📊 Power BI Dashboard

Connected the PostgreSQL table to **Power BI** to create visuals such as:

- Trends in total casualties over time
- Casualty breakdown by oblast (region)
- Combat intensity heatmaps
- Occupied territory analysis



## 📫 Contact

For any questions, feedback, or collaboration inquiries, feel free to reach out:

- 📧 Email: korosbrian574@gmail.com  
- 📞 Phone: +254 768 518 488  
- 💼 LinkedIn: [Brian Kimutai](https://www.linkedin.com/in/brian-kimutai-0888352b6/)

