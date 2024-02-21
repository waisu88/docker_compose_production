import React, { useEffect, useState } from 'react';


const WeatherDataList = () => {
    const [weatherData, setWeatherData] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/weather/data-list/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const jsonData = await response.json();
                setWeatherData(jsonData);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            <h2>Weather Data</h2>
            {weatherData ? (
                <div className='weather-data'>
                    <p>Count: {weatherData.count}</p>
                    <ul>
                        {weatherData.results.map((data) => (
                            <li key={data.id} className='record-weather'>
                                <p>Station: {data.stacja}</p>
                                <p>Date: {data.data_pomiaru}</p>
                                <p>Temperature: {data.temperatura}</p>
                                {/* Add other data fields as needed */}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default WeatherDataList;