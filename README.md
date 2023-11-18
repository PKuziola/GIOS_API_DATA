<a name="readme-top"></a>
# 👨‍💻 Built with
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">

<!-- ABOUT THE PROJECT -->
# About The Project

![gios][gios-url]

This project is created to collect and store data collected from [GIOS API](https://powietrze.gios.gov.pl/pjp/content/api).<p>
Script runs every hour and appends new measurements to database.

Database consists of two tables:
* stations_basic_info
* measurements 

### stations_basic_info

| Column_name  | Datatype | Description |
| ------------- | ------------- | ------------- |
| id  | INTEGER  | station's ID  | 
| stationName  | TEXT  | station's name  |
| gegrLat  | TEXT  | geographic latitude  |
| gegrLon  | TEXT  | geographic longitude  |
| addressStreet  | TEXT  | station's street & flat number  |
| cityName  | TEXT  | station's city  |

### measurements

| Column_name  | Datatype | Description |
| ------------- | ------------- | ------------- |
| paramCode  | TEXT  | pollutant  | 
| date  | TEXT  | measurement's date  |
| value  | REAL  | measurement's value in μg/m3 unit|
| stationId  | INTEGER  | station's ID  |
| sensorId  | INTEGER  | sensor's ID  |


<p align="right">(<a href="#readme-top">back to top</a>)</p>


# 🔑Setup

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Getting Started

```bash
# Clone the repository
$ git clone https://github.com/PKuziola/GIOS_API_DATA.git
# Navigate to the project folder
$ cd gios
# Remove the original remote repository
$ git remote remove origin
```

### Building container

Create image of container:
```bash
docker build -t gios_api_project .
```
When created, run container:
```bash
docker run -it --name gios_container gios_api_project
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# 🌲 Project tree
```bash
.
├── .gitignore
├── Dockerfile
├── README.md
├── license.txt
├── srodowisko_api_dane.py
└── requirements.txt 

```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
# 📄 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[gios]: https://powietrze.gios.gov.pl/pjp/content/api
[gios-url]: https://www.gios.gov.pl/images/logo.png
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
[linkedin-url]: https://www.linkedin.com/in/piotr-kuzio%C5%82a-992b00174/
[product-screenshot]: images/screenshot.png


