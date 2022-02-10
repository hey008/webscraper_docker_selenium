# WebScraper with Selenium
_Scrape website data from specific URL from Chrome Browser with Selenium in Docker. So we can deploy this on cloud to set up as the concurrent service_

## Docker: for Selenium Hub with Chrome Driver
Start Selenium Hub with Docker Compose
```bash
docker-compose up
```
> **Note:**  
Selenium hub run on port 4444. To check service is ready to use by access URL below:  
http://localhost:4444/grid/console  


## Python: Web Scraper script
Get project ready
```bash
python -m pip install --upgrade pip
python -m venv venv
. venv/bin/activate
# On Windows use this '.\venv\Scripts\activate.bat'
pip install -r requirements.txt
```
Start services
```bash
python services.py
```

---
_Copyright © 2022 - [Jirawit Inkhao](https://www.github.com/hey008)_