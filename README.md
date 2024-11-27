# Servicio-social
Este repositorio incluye mis trabajos para el servicio soial en Aprendizaje de Máquina sobre el Impacto del Cambio en el Uso del Suelo sobre la Biodiversidad y el Bienestar.
Se sabe que el cambio climatico es una realidad y cada día se tiene una variablidad en las temperaturas mayor, por lo que es de suma importancia investigar este fenómeno desde distintas perspectivas, es por eso que en este trabajo se observa el cambio clímatico desde los 1850s hasta la actualidad.Observando los disitntos cambios que se han visto a lo largo de este tiempo y tratar de entcontrar algunos patrones al respecto.

## Espectros de Potencia
Utilizando los datos de https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/Complete_TAVG_daily.txt observamos la anomalia de la temperatura a lo largo del tiempo desde 1880, vamos a dividir los datos en su respectiva década a la cual le vamos a aplicar la transformada de Fourier, para obtener su especto de potencia.
Una vez teniendo esto, vamos a dividir este espectro en dos partes que nos interesa analizar, las series de tiempo cortas(0-45 días) y de medio alcnace(45-180 días) para analizar las pendientes de estas y ver el cambio a lo largo de las décadas de las pendientes y si se pierde la correlación entre ambos periodos de días.

![80c67924-f9d2-40c2-be7f-21dfb0ff9d82](https://github.com/user-attachments/assets/20431544-32ec-4b50-9aad-af303fa0d38e)

![3f90dc5d-e7b3-473a-9653-c8c48158a283](https://github.com/user-attachments/assets/f20a0fd5-f7b4-4447-841a-e2e0772f79ed)


## Anlaisis de comunidades a partir de la temperatura
Utilizando los datos geograficos y de temperatura a lo largo de las decadas desde 1850 queremos ver cuales son algunas comunidades que se crean y como han cambiado estas a lo largo del tiempo.
Primero teneindo los datos de __________  
Interpolamos los datos vacios bajo los siguientes criterios:
1111
111
111

Para todo punto del mapa le vamos a sacar su infomración mutua(tambien se probo con correlación de Person,pero al no limitarse a variables en números relaes ni relaciones lineales la infomración mutua es más general.)(poner referencias) comparado con todos los otros puntos, para cada década, con lo que vamos a optener una matriz para cada una de estas, esto al ser un proceso computacionalmente pesado se utilizo un cluster de comuputadoras.(poner referencia de código)



Con estas matrices ahora proseguimos a crear una red goegráfica en donde si la información mutua entre cualquier par de nodos es mayor a 0.8 se crea una arista entre estos una vez que tengamos nuestras redes queremos detectar las comunidades de estas, por lo que vamos a utilizar el método de Louvein(poner referencias) para obtenerlas, surge el problema de que no detecta las mismas comubidades para décadas distitnas, por lo que se creo una función que compara cada comunidad con las de la década anterior para encontrar las comunidades más parecidas en vace a los nodos que se encuentran en esta, así le aplicamos la misma etiqueta a las comunidades a lo largo  de las décadas, una vez con esto le  aplicamos algunas métricas a ñas redes, donde observamos la Modularidad, el número de comunidades y vemos cuntos nodos se quedan constantes a lo largo de las transicciones de las décadas

![community_maps_over_decades](https://github.com/user-attachments/assets/97addee6-f3da-46e1-85c1-e320cb117053)
Se puede observar que como es intuitivo las comunidades estan dadas por cercania geográfica, ademas de que, divisiones de la tierra clara como es el caso de la costa maritima suelen dividir a las comunidades. Así mismo existen varias comunidades que suelen ser bastantes constantes a lo loargo de las décadas.
![community_bar_charts_over_decades](https://github.com/user-attachments/assets/7f5fdb73-f830-4331-ada5-92741f7fe150)
