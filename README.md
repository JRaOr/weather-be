# Weather App

> Weather App para la Rapid Api Hackathon de [midudev](https://github.com/midudev).

- Server Link: https://github.com/JRaOr/weather-be
- Frontend Application Link: https://github.com/JRaOr/weather-fe
- Live app: https://weather.gerardoraor.com
##### Tecnologias utilizadas

- [NextJs](https://nextjs.org/) - The React Framework for Production!
- [TailwindCSS](https://tailwindcss.com/) - Rapidly build modern websites without ever leaving your HTML.
- [Flask](https://flask.palletsprojects.com/en/2.1.x/) - Flask is a lightweight WSGI web application framework.
- [AWS](https://aws.amazon.com/es/) - Amazon Web Services, Route53, SNS, S3
- [MongoAtlas](https://www.mongodb.com/) - Working with data doesn’t need to be hard
- [Railway](https://railway.app/) - Railway is a deployment platform where you can provision infrastructure, develop with that infrastructure locally, and then deploy to the cloud.

### Instalacion de Frontend

Instalacion de dependencias!

```sh
git clone https://github.com/JRaOr/weather-fe
cd weather-fe
npm i
```
Crea un archivo .env en el directorio raiz, similar a .env.demo, agrega el api endpoint de la aplicacion en flask (ejemplo).
```
NEXT_PUBLIC_API_SERVER=http://localhost:5000
```
Ejecuta la aplicacion:
```
npm run dev
```

### Instalacion de Backend

Instalacion de dependencias!

```sh
git clone https://github.com/JRaOr/weather-be
cd weather-be
pip install requirements.txt
```
Crea un archivo .env en el directorio raiz, similar a .env.demo, agrega las keys de cada recurso y despues ejecuta.

```
python main.py
```