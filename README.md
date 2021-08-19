# TrafficLight_Detection
Trabajo de apoyo para tesis, consiste en crear un prototipo de un bastón inteligente que ayude a las personas no videntes en su día a día, siendo capas de reconocer el estado de un semáforo y avisarle mediante audio al usuario, de la misma forma que hace uso de un gps, para poder indicarle, también mediante audio, en que calle se encuentra. Cabe destacar que esta solo es la fase de prototipado y que los códigos presentados podrían variar en el futuro.

## Archivos
### ModuloRaspy.py 
Es el módulo final, donde se implementan en conjunto todos los requerimientos.
~~~
python3 moduloRaspy.py
~~~

### TestColor.py
Se encarga de identificar colores, en especifico el verde y el rojo, mediante OpenCV.
~~~
python3 testColor.py
~~~

### TestButton.py
Agrega la lógica al módulo anterior de forma de poder controlar distintas funcionalidades con un solo botón.
~~~
python3 testButton.py
~~~

### GPS.py
Logra captar la señal de gps del módulo Neo 6M. 
~~~
python3 gps.py
~~~

### ReverseGeocoding.py
Mediante geopy, logra transformar latitudes y longitudes en direcciones físicas.
~~~
python3 reverseGeocoding.py
~~~

### Sound.py
Mediante Espeak, logra transformar texto en audio, pudiendo variar la voz, velocidad, tono, etc.
~~~
python3 sound.py
~~~



## Librerías Necesarias
Antes que nada es necesario actualizar el sistema a la última versión
~~~
sudo apt-get update
sudo apt-get upgrade
~~~

### CV2
~~~
sudo apt install python3-opencv
~~~

### Pynmea2
~~~
pip3 install pynmea2
~~~
Aqui tambien es necesario hacer unos ajustes en la interfaz de la raspberry. (Se comunica por el puerto ttyS0, ya que el AMA0 está reservado para el bluetooth)

1. Para ello se debe escribir el comando
~~~
sudo raspi-config
~~~

2. Ir a "Interfacing options"
3. Serial
4. No
5. Yes
6. Luego reiniciar la raspberry.

### Espeak
~~~
sudo apt-get install espeak
sudo apt-get install espeak python-espeak
~~~

### Geopy
~~~
pip3 install geopy
~~~

## Esquematico
![apoyoProyectoSeba_Mesa de trabajo 1](https://user-images.githubusercontent.com/50645020/130025497-3782d38f-3c56-4da7-9130-014f49adafb9.jpg)
