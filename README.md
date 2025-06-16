# 🏭 Warehouse Parts Separation Tracking API 📊

This serverless API tracks parts separation operations in a industrial environment, recording timing data and providing aggregated analytics. The system uses AWS Lambda, API Gateway, and MySQL RDS with a focus on Brazilian timezone handling.

## 🌐 Architecture Overview

- **🚪 AWS API Gateway**: REST endpoints for all operations
- **⚡ AWS Lambda**: Python functions handling business logic
- **🗃️ MySQL RDS**: Persistent data storage with timezone-aware timestamps
- **🔐 IAM Roles**: Secure access between services

## 🗄️ Database Schema

### 📊 Tables
1. **`peca` (Parts)**
   - `id`: Auto-increment primary key
   - `tipo`: Part type/classification (string)

2. **`separacao` (Separations)**
   - `id`: Auto-increment primary key
   - `id_peca`: Foreign key to `peca` table
   - `horario_inicial`: Start timestamp (auto-generated)
   - `horario_fim`: End timestamp (optional)

### 👀 Views
1. **`agregacao` (Aggregation)**
   - Groups separation data in 5-minute intervals ⏱️
   - Calculates metrics: count, average duration, min/max duration
   - Organized by part type and time interval

## 🔌 API Endpoints

### 🧩 Parts Management
- **`POST /peca`**
  - Creates a new part record
  - Required body: `{"tipo": "part_type"}`
  - Returns: `{"id_peca": new_id}`

### 📦 Separation Operations
- **`POST /separacao`**
  - Records a separation operation
  - Required body: `{"id_peca": part_id}`
  - Optional: `{"horario_fim": "YYYY-MM-DD HH:MM:SS"}`

### 📊 Data Retrieval
- **`GET /agregacao`**
  - Retrieves aggregated separation data
  - Returns time-grouped statistics in Brazil timezone 🇧🇷
  - Sample response:
    ```json
    [
      {
        "peca_tipo": "metal",
        "time_interval": "2025-05-30 20:30:00",
        "date": "2025-05-30",
        "time": "20:30:00",
        "total_separacoes": 1,
        "avg_duration_seconds": "19.0000",
        "min_duration": 19,
        "max_duration": 19
      }
    ]
    ```

## ⚙️ Lambda Functions

### `conn.py` 🛠️
- Initializes database schema on first run
- Creates tables and aggregation view
- Handles Brazil timezone conversion
- Environment variables required:
  - `user`: Database username
  - `password`: Database password
  - `host`: RDS endpoint
  - `database`: Schema name

### `get.py` 📥
- Retrieves aggregated separation data
- Groups results by time interval
- Returns data in Brazil timezone format

### `post_peca.py` ➕
- Creates new part records
- Validates required "tipo" field
- Returns the created part ID

### `post_separacao.py` ⏱️
- Records separation operations
- Accepts optional end timestamp
- Auto-generates start timestamp

## ⏰ Timezone Handling
All database operations automatically:

- Convert timestamps to America/Sao_Paulo timezone 🇧🇷
- Aggregate data in local Brazil time
- Return time-formatted results for frontend display

## ❌ Error Handling
Standard response format:

```json
{
  "statusCode": [HTTP_CODE],
  "body": {
    "message": "Success message" | "error": "Error description"
  }
}
```

Common status codes:

- ✅ 200: Successful GET
- ✅ 201: Successful creation
- ❗ 400: Missing required fields
- ❌ 500: Database/server error

## 🔄 Maintenance
The aggregation view automatically recalculates:

- Every 5 minutes for new data ⏱️
- With proper timezone conversion 🌐
- Including all duration metrics 📈

## 📝 Example Requests
### Create Part
```bash
curl -X POST https://https://19zqwui8tj.execute-api.us-east-1.amazonaws.com/peca \
  -H "Content-Type: application/json" \
  -d '{"tipo": "motor"}'
```

### Record Separation
```bash
curl -X POST https://19zqwui8tj.execute-api.us-east-1.amazonaws.com/separacao \
  -H "Content-Type: application/json" \
  -d '{"id_peca": 1}'
```

### Get Aggregated Data
```bash
curl -X GET https://19zqwui8tj.execute-api.us-east-1.amazonaws.com/agregacao
```