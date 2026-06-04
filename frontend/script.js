function createWeatherInfo(data) {
  const city = data.city.name;
  const country = data.city.country;
  const currentWeatherMeasurement = data.list[0];

  const mainData = currentWeatherMeasurement.main;
  const temperature = mainData.temp.toFixed(1);
  const humidity = mainData.humidity;

  const description = currentWeatherMeasurement.weather[0].description;
  const iconCode = currentWeatherMeasurement.weather[0].icon;
  const windSpeed = currentWeatherMeasurement.wind.speed;

  console.log(JSON.stringify(currentWeatherMeasurement));

  return `<div class="weather__card card">
            <h2 class="card__title">Weather Forecast</h2>
            <div class="card__info">
              <img class="card__icon" src="https://openweathermap.org/img/wn/${iconCode}@2x.png" alt="${description}">
              <p class="card__temperature">🌡️ ${temperature}℃</p>
              <p class="card__description">${description}</p>
              <p class="card__location">🗺️ ${city}, ${country}</p>
            </div>
            <div class="card__footer">
              <p class="card__wind-speed">💨 ${windSpeed} km/h</p>
              <p class="card__humidity">💧 ${humidity}%</p>
            </div>
          </div>
  `
}

async function getCityCoords(cityName) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/geocoords/${cityName}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  } catch(error) {
    console.log("getCityCoords error:", error);
    throw error
  }
}

async function getWeatherInfo({ lat, lon }) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/forecast?lat=${lat}&lon=${lon}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  } catch(error) {
    console.log("getWeatherInfo error:", error);
    throw error
  }
}

async function main() {
  const formElement = document.querySelector(".weather__form");
  const inputElement = document.querySelector(".form__input");
  const weatherResultElement = document.querySelector(".weather__result");

  formElement.addEventListener("submit", async (event) => {
    event.preventDefault();

    const cityName = inputElement.value.trim();

    weatherResultElement.innerHTML = "<p>⏳ Loading...</p>";
    
    try {
      const cityCoordinates = await getCityCoords(cityName);
      const weatherData = await getWeatherInfo(cityCoordinates);
      weatherResultElement.innerHTML = createWeatherInfo(weatherData);
    } catch (error) {
      weatherResultElement.innerHTML = `<p>❌ ${error.message}`;
    }
  });
}

main();