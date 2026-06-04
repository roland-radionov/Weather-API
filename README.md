# Weather API

This is simple weather API. The idea was taken from roadmaps.sh.

## Features

- A simple UI that makes it easy to get weather information for any country.
- Weather API created with FastAPI.
- Using Redis to cache same responses and increase performance.

## How to run

1. **Clone repository**
   ```bash
   git clone https://github.com/roland-radionov/Weather-API.git
   cd Weather-API
   ```

2. **Setup virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt 
   ```
   
4. **Launch Redis (Docker)**
   ```bash
   docker run -d -p 6379:6379 redis
   ```
   
5. **Add API-key to .env**

   Create `.env` file in project root:  
   ```env
   API_KEY="your_openweathermap_api_key"
   REDIS_URL="redis://localhost"
   ```
   Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)
   Sign up, confirm email, and copy the key from the "API keys" tab.

6. **Launch the server**

   ```bash
   uvicorn main:app --reload
   ```

7. **Open Frontend**

    Open index.html with "Live Server" (VS Code extension) or any HTTP server.
    API documentation will be available in `http://127.0.0.1:8000/docs`

## Credits

This project is based on the [Weather API](https://roadmap.sh/projects/weather-api-wrapper-service) project from [roadmap.sh](https://roadmap.sh).

## Author

Radionov Roland