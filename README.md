# TrafficLight_Detection
Trabajo de apoyo para tesis, consiste en crear un prototipo de un bastón inteligente que ayude a las personas no videntes en su día a día, siendo capas de reconocer el estado de un semáforo y avisarle mediante audio al usuario, de la misma forma que hace uso de un gps, para poder indicarle, también mediante audio, en que calle se encuentra. Cabe destacar que esta solo es la fase de prototipado y que los códigos presentados podrían variar en el futuro.


## ModuloRaspy.py 
Es el módulo final, donde se implementan en conjunto todos los requerimientos.

## TestColor.py
Se encarga de identificar colores, en especifico el verde y el rojo, mediante OpenCV.

## TestButton.py
Agrega la lógica al módulo anterior de forma de poder controlar distintas funcionalidades con un solo botón.

## GPS.py
Logra captar la señal de gps del módulo Neo 6M. 

## ReverseGeocoding.py
Mediante geopy, logra transformar latitudes y longitudes en direcciones físicas.

## Sound.py
Mediante Espeak, logra transformar texto en audio, pudiendo variar la voz, velocidad, tono, etc.

## Librerías Necesarias
~sudo apt install python3-opencv~
