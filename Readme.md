

# 🚗 Fuel Route Optimizer API

A Django REST API that calculates an optimized driving route between two coordinates and estimates fuel stops and fuel cost along the route.

This project integrates with the **OpenRouteService API** and uses fuel price data to simulate fuel optimization.

---

## 📌 Features

* ✅ Calculate driving route between two coordinates
* ✅ Decode route geometry (polyline)
* ✅ Estimate total distance in miles
* ✅ Calculate fuel required (based on MPG)
* ✅ Estimate fuel cost
* ✅ Return fuel stop suggestions
* ✅ Response caching for improved performance
* ✅ REST API built with Django & Django REST Framework

---

## 🛠 Tech Stack

* Python 3.x
* Django 6.x
* Django REST Framework
* OpenRouteService API
* Polyline decoding
* CSV-based fuel price dataset

---

# ⚙️ Setup Instructions

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/soumiblink/spotter_python_django_assignment.git
cd spotter_python_django_assignment
```

---

## 2️⃣ Create Virtual Environment

### Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If polyline is missing:

```bash
pip install polyline
```

---

## 4️⃣ Setup Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
ORS_API_KEY=your_openrouteservice_api_key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 🔑 Get OpenRouteService API Key:

1. Go to [https://openrouteservice.org/](https://openrouteservice.org/)
2. Create a free account
3. Generate an API key

---

## 5️⃣ Run Migrations

```bash
python manage.py migrate
```

---

## 6️⃣ Run Development Server

```bash
python manage.py runserver
```

Server will start at:

```
http://127.0.0.1:8000/
```

---

# 🚀 API Usage

## Endpoint

```
POST /api/optimize-route/
```

### Full URL (Local)

```
http://127.0.0.1:8000/api/optimize-route/
```

---

## 📥 Request Body (JSON)

```json
{
  "start_coords": [-74.0060, 40.7128],
  "end_coords": [-73.935242, 40.730610]
}
```

OR

```json
{
  "start_coords": "40.7128,-74.0060",
  "end_coords": "40.730610,-73.935242"
}
```

---

## 📤 Example Response

```json
{
  "distance_miles": 5.23,
  "fuel_required_gallons": 0.21,
  "estimated_fuel_cost": 0.74,
  "fuel_stops": [
    {
      "location": "Stop 1",
      "lat": 40.7128,
      "lng": -74.006
    },
    {
      "location": "Stop 2",
      "lat": 40.73061,
      "lng": -73.935242
    }
  ],
  "route_geometry": [
    [40.7128, -74.006],
    [40.7135, -74.005],
    ...
  ]
}
```

---

# ⛽ Fuel Calculation Assumptions

* Default MPG: **25 miles per gallon**
* Default tank range: **~500 miles**
* Fuel price assumption: **$3.50 per gallon** (can be improved using CSV data)

---

# 🧠 Optimization Logic

1. Fetch route from OpenRouteService
2. Convert distance meters → miles
3. Decode polyline geometry
4. Estimate fuel needed:

   ```
   gallons = distance / mpg
   ```
5. Estimate fuel cost:

   ```
   cost = gallons × fuel_price
   ```
6. Return stops + summary

---

# 📂 Project Structure

```
fuel_route_optimizer/
│
├── api/
│   ├── views.py
│   ├── services.py
│   └── urls.py
│
├── data/
│   └── fuel-prices-for-be-assessment.csv
│
├── fuel_route_optimizer/
│   └── settings.py
│
├── manage.py
└── requirements.txt
```

---

# 🧪 Testing with Postman

1. Start server:

   ```
   python manage.py runserver
   ```

2. Open Postman

3. Create new request:

   * Method: `POST`
   * URL: `http://127.0.0.1:8000/api/optimize-route/`
   * Body → raw → JSON

4. Paste:

```json
{
  "start_coords": [-74.0060, 40.7128],
  "end_coords": [-73.935242, 40.730610]
}
```

5. Click **Send**

You should receive a `200 OK` response.

---

# 📦 Caching

The API uses Django caching to avoid repeated calls to OpenRouteService for the same route request.

---

# 🎥 Demo Video

A Loom demonstration video is included in the assignment submission showing:

* Running the server
* Sending request via Postman
* API response
* Brief code walkthrough

---


# 👨‍💻 Author

Soumi 
GitHub: [https://github.com/soumiblink](https://github.com/soumiblink)

---


