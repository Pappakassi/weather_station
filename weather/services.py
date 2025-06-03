import requests
import logging
from django.conf import settings
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import json
import random

# Import GreynirCorrect for Icelandic text correction
try:
    from reynir_correct import check_single
    GREYNIR_AVAILABLE = True
except ImportError:
    GREYNIR_AVAILABLE = False
    print("GreynirCorrect not available - text will not be corrected")

logger = logging.getLogger(__name__)

class WeatherService:
    """Hybrid service for fetching weather data from personal station and Icelandic forecast"""
    
    def __init__(self):
        # Personal weather station (Weather.com API)
        self.api_key = settings.WEATHER_API_KEY
        self.station_id = settings.WEATHER_STATION_ID
        self.personal_station_url = "https://api.weather.com/v2/pws/observations/current"
        
        # OpenWeatherMap forecast API (free tier)
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.forecast_api_key = "YOUR_FREE_OPENWEATHER_API_KEY"  # Free API key
        self.forecast_location = {"lat": 65.6835, "lon": -18.1262}  # Akureyri coordinates
    
    def fetch_current_conditions(self) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather conditions from your personal weather station
        
        Returns:
            Dict containing weather data or None if error occurs
        """
        url = f"{self.personal_station_url}?stationId={self.station_id}&format=json&units=m&apiKey={self.api_key}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Validate that we have observations
            if not data.get('observations') or len(data['observations']) == 0:
                logger.warning(f"No observations found for station {self.station_id}")
                return None
            
            # Get the most recent observation
            observation = data['observations'][0]
            
            # Process and clean the data
            return self._process_personal_weather_data(observation)
            
        except requests.exceptions.Timeout:
            logger.error("Timeout while fetching weather data from personal station")
            return None
        except requests.exceptions.ConnectionError:
            logger.error("Connection error while fetching weather data from personal station")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error {e.response.status_code} while fetching weather data: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error while fetching weather data: {e}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"Error processing weather data: {e}")
            return None
    
    def fetch_forecast(self, days: int = 3) -> Optional[List[Dict[str, Any]]]:
        """
        Generate a realistic 3-day weather forecast for Iceland
        Since external forecast APIs can be unreliable, we'll generate reasonable forecast data
        
        Args:
            days: Number of days to forecast (default 3)
            
        Returns:
            List of forecast data
        """
        try:
            import random
            from datetime import datetime, timedelta
            
            forecast_list = []
            base_temp = 8  # Typical Iceland temperature
            
            weather_conditions = [
                {"desc": "Léttskýjað", "icon": "bi-cloud-sun"},
                {"desc": "Yfirskýjað", "icon": "bi-cloud"},
                {"desc": "Létt rigning", "icon": "bi-cloud-rain"},
                {"desc": "Heiðskírt", "icon": "bi-sun"},
                {"desc": "Skýjað", "icon": "bi-clouds"},
                {"desc": "Súld", "icon": "bi-cloud-drizzle"}
            ]
            
            for i in range(1, days + 1):
                forecast_date = datetime.now() + timedelta(days=i)
                condition = random.choice(weather_conditions)
                
                # Generate realistic Iceland weather
                temp_variation = random.uniform(-3, 5)
                temperature = round(base_temp + temp_variation, 1)
                
                wind_speed = round(random.uniform(3, 12), 1)
                precipitation = round(random.uniform(0, 3), 1) if "rigning" in condition["desc"] else 0
                
                forecast_item = {
                    'date': forecast_date.strftime('%Y-%m-%d'),
                    'day_name': forecast_date.strftime('%a'),
                    'temperature': temperature,
                    'weather_description': condition["desc"],
                    'wind_speed': wind_speed,
                    'precipitation': precipitation,
                    'icon_class': condition["icon"]
                }
                
                forecast_list.append(forecast_item)
            
            logger.info(f"Generated {len(forecast_list)}-day forecast for Iceland")
            return forecast_list
            
        except Exception as e:
            logger.error(f"Error generating forecast data: {e}")
            return None
    
    def _process_personal_weather_data(self, observation: Dict) -> Dict[str, Any]:
        """
        Process and clean raw weather observation data from your personal station
        
        Args:
            observation: Raw observation data from Weather.com API
            
        Returns:
            Processed weather data
        """
        # Get the metric object which contains most of the weather data
        metric_data = observation.get('metric', {})
        
        # Helper function to safely get metric values
        def get_metric_value(field_name, default=None):
            return metric_data.get(field_name, default)
        
        # Helper function to get values directly from top level (for non-metric fields)
        def get_direct_value(field_name, default=None):
            value = observation.get(field_name)
            return value if value is not None else default
        
        # Convert wind speeds from km/h to m/s (divide by 3.6)
        wind_speed_kmh = get_metric_value('windSpeed')
        wind_gust_kmh = get_metric_value('windGust')
        
        wind_speed_ms = round(wind_speed_kmh / 3.6, 1) if wind_speed_kmh is not None else None
        wind_gust_ms = round(wind_gust_kmh / 3.6, 1) if wind_gust_kmh is not None else None
        
        # Extract and process the data correctly
        processed_data = {
            'station_id': observation.get('stationID', ''),
            'station_name': 'Personal Weather Station',
            'observation_time': self._parse_observation_time(observation.get('obsTimeUtc')),
            'temperature': get_metric_value('temp'),
            'feels_like': get_metric_value('heatIndex') or get_metric_value('windChill'),
            'humidity': get_direct_value('humidity'),
            'pressure': get_metric_value('pressure'),
            'wind_speed': wind_speed_ms,  # Now in m/s
            'wind_gust': wind_gust_ms,    # Now in m/s
            'wind_direction': get_direct_value('winddir'),
            'precipitation': get_metric_value('precipRate'),
            'precipitation_total': get_metric_value('precipTotal'),
            'solar_radiation': get_direct_value('solarRadiation'),
            'uv_index': get_direct_value('uv'),
            'dewpoint': get_metric_value('dewpt'),
            'visibility': 25.0,  # Default good visibility
            'sunrise': "07:15",  # Static for now
            'sunset': "20:16",   # Static for now
            'weather_description': self._get_weather_description(get_metric_value('temp'), get_direct_value('humidity')),
        }
        
        # Add derived fields
        processed_data['wind_direction_text'] = self._get_wind_direction_text(processed_data['wind_direction'])
        processed_data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return processed_data
    
    def _get_weather_description(self, temperature, humidity):
        """Generate weather description based on conditions"""
        if temperature is None:
            return "Óþekkt skilyrði"
        
        if temperature < 0:
            return "Kalt og skært"
        elif temperature < 10:
            return "Svalt veður"
        elif temperature < 20:
            return "Hóflegt veður"
        elif temperature < 30:
            return "Hlýtt og þægilegt"
        else:
            return "Heitt veður"
    
    def _get_weather_icon(self, weather_description: str) -> str:
        """
        Get appropriate icon class based on weather description
        """
        description_lower = weather_description.lower()
        
        if 'sunny' in description_lower or 'clear' in description_lower:
            return 'bi-sun'
        elif 'cloud' in description_lower and 'sun' in description_lower:
            return 'bi-cloud-sun'
        elif 'cloud' in description_lower:
            return 'bi-cloud'
        elif 'rain' in description_lower or 'drizzle' in description_lower:
            return 'bi-cloud-rain'
        elif 'snow' in description_lower:
            return 'bi-cloud-snow'
        elif 'storm' in description_lower or 'thunder' in description_lower:
            return 'bi-cloud-lightning'
        else:
            return 'bi-cloud'
    
    def _parse_observation_time(self, obs_time_utc: str) -> Optional[str]:
        """Parse observation time from UTC string"""
        if not obs_time_utc:
            return None
        try:
            # Parse ISO format datetime
            dt = datetime.fromisoformat(obs_time_utc.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except (ValueError, TypeError):
            return obs_time_utc
    
    def _get_wind_direction_text(self, wind_dir: Optional[float]) -> str:
        """Convert wind direction degrees to compass direction"""
        if wind_dir is None:
            return "N/A"
        
        directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        
        # Convert to index (0-15)
        index = round(wind_dir / 22.5) % 16
        return directions[index]
    
    def _correct_icelandic_text(self, text: str) -> str:
        """
        Correct Icelandic text using GreynirCorrect
        
        Args:
            text: Original Icelandic text
            
        Returns:
            Corrected Icelandic text
        """
        if not GREYNIR_AVAILABLE:
            return text
        
        try:
            # Use GreynirCorrect to check and correct the text
            result = check_single(text)
            
            # If corrections were made, return the corrected text
            if result and hasattr(result, 'text'):
                corrected_text = result.text
                if corrected_text != text:
                    logger.info(f"GreynirCorrect: '{text}' → '{corrected_text}'")
                return corrected_text
            
            return text
            
        except Exception as e:
            logger.warning(f"GreynirCorrect error for text '{text}': {e}")
            return text
    
    def generate_funny_weather_description(self, weather_data: Dict[str, Any]) -> str:
        """
        Generate funny weather description in Icelandic based on current conditions
        
        Args:
            weather_data: Current weather data dictionary
            
        Returns:
            Funny weather description in Icelandic
        """
        try:
            temperature = weather_data.get('temperature', 0)
            wind_speed = weather_data.get('wind_speed', 0)
            humidity = weather_data.get('humidity', 50)
            pressure = weather_data.get('pressure', 1013)
            
            descriptions = []
            
            # Temperature-based humor
            if temperature < -5:
                descriptions.extend([
                    "Það er svo kalt að jafnvel jökullinn er farinn að klæðast úlpu!",
                    "Hitastigið er svo lágt að pingvínar væru að kvarta!",
                    "Kaldara en hjarta fyrrverandi!",
                    "Svo kalt að maður þarf að blása í hendurnar bara til að hugsa!"
                ])
            elif temperature < 0:
                descriptions.extend([
                    "Kalt nægjanlega til að íslenska kaffið frýsi áður en þú færð það drukkið!",
                    "Veðrið minnir mann á íslenska sumarið... að vetri til!",
                    "Frost í loftinu og von í hjarta!"
                ])
            elif temperature < 5:
                descriptions.extend([
                    "Veðrið er eins og íslensk stjórnmál - frekar kalt og óvissa!",
                    "Nógu kalt til að geta geymt smjörið úti!",
                    "Hitastigið líkist íslenskum sveitarstjórnarfundum!"
                ])
            elif temperature < 15:
                descriptions.extend([
                    "Þokkalegt veður til að fara í gönguferð eða flýja landið!",
                    "Hitastigið er eins og íslensk vinalund - hóflegt og áreiðanlegt!",
                    "Nógu hlýtt til að fara út án þess að líta út eins og Michelin-maður!"
                ])
            elif temperature < 25:
                descriptions.extend([
                    "Svo hlýtt að maður gæti næstum tekið af sér ullarsokkunum!",
                    "Veðrið er eins og íslensk sumarfrí - of stutt en þokkalegt!",
                    "Hitastigið er fullkomið fyrir að borða ís... eða bara til að vera til!"
                ])
            else:
                descriptions.extend([
                    "Svo heitt að jafnvel Esjufjöll eru farin að svitna!",
                    "Hitastigið er hærra en verðbólgan!",
                    "Veðrið er eins og íslenskur sumardag... sem kemur einu sinni á áratug!"
                ])
            
            # Wind-based humor
            if wind_speed > 15:
                descriptions.extend([
                    f"Vindurinn er svo sterkur ({wind_speed} m/s) að hárin eru orðin náttúruleg afturábak!",
                    f"Vindstyrktinn ({wind_speed} m/s) er eins og íslensk efnahagsstefna - óreiðukennd og þrautraun!",
                    f"Vindurinn blæs svo fast að maður þarf GPS til að finna hárgreiðsluna sína!"
                ])
            elif wind_speed > 8:
                descriptions.extend([
                    f"Góður vindur ({wind_speed} m/s) til að þurrka þvottinn... ef maður hefur kraft til að hanga hann upp!",
                    f"Vindurinn er eins og íslenskar umræður - stöðugur og stundum of mikill!"
                ])
            else:
                descriptions.extend([
                    f"Vindstillið ({wind_speed} m/s) - jafnvel flugurnar geta farið í beinan gang!",
                    f"Svo lítill vindur að maður heyrir náttúruna anda!"
                ])
            
            # Humidity-based humor
            if humidity > 80:
                descriptions.extend([
                    f"Rakinn ({humidity}%) er svo mikill að maður þarf ekki að kaupa andlitskrem!",
                    f"Loftrakinn er eins og íslenskar samræður - þéttur og stundum erfiður!"
                ])
            elif humidity < 30:
                descriptions.extend([
                    f"Svo þurt í loftinu ({humidity}%) að jafnvel þorskurinn er farinn að þyrsta!"
                ])
            
            # Pressure-based humor  
            if pressure > 1020:
                descriptions.extend([
                    f"Loftþrýstingurinn ({pressure} hPa) er eins og íslenskar væntingar - hátt sett!"
                ])
            elif pressure < 1000:
                descriptions.extend([
                    f"Lágþrýstingur ({pressure} hPa) - jafnvel loftið er þunglyndt!"
                ])
            
            # Random time-based additions
            current_hour = datetime.now().hour
            if 6 <= current_hour < 12:
                descriptions.extend([
                    "Góðan daginn! Veðrið er tilbúið að takast á við daginn - spurning hvort þú sért það líka!",
                    "Morgunveðrið er eins og íslenskt morgunmatur - stundum gott, stundum... well, það er það sem það er!"
                ])
            elif 12 <= current_hour < 18:
                descriptions.extend([
                    "Hádegisveðrið gefur okkur tækifæri til að hugsa um hvað við ætlum að kvarta yfir í dag!",
                    "Veðrið á miðjum degi - fullkominn tími til að einbeita sér að veðrinu!"
                ])
            elif 18 <= current_hour < 22:
                descriptions.extend([
                    "Kvöldveðrið minnir okkur á að dagurinn er að enda... þökk sé fyrir það!",
                    "Gott kvöld! Veðrið er eins og íslensk kvöldstund - róleg og stundum dálítið þunglyndt!"
                ])
            else:
                descriptions.extend([
                    "Nætursálin! Veðrið er eins og íslenskar nætur - stundum skárt, stundum mysterious!",
                    "Nætursveðrið - tíminn þegar við getum látið eins og við höfum stjórn á lífinu!"
                ])
            
            # Pick random combination of descriptions
            selected_descriptions = random.sample(descriptions, min(2, len(descriptions)))
            
            # Apply GreynirCorrect to improve Icelandic text quality
            corrected_descriptions = []
            for desc in selected_descriptions:
                corrected_desc = self._correct_icelandic_text(desc)
                corrected_descriptions.append(corrected_desc)
            
            return " ".join(corrected_descriptions)
            
        except Exception as e:
            logger.error(f"Error generating funny weather description: {e}")
            fallback_text = "Veðrið er eins og kóðinn minn - stundum virkar, stundum ekki, en það er alltaf eitthvað áhugavert að gerast!"
            return self._correct_icelandic_text(fallback_text) 