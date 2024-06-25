# Servicio-social
Este repositorio incluye mis trabajos para el servicio soial en Aprendizaje de Máquina sobre el Impacto del Cambio en el Uso del Suelo sobre la Biodiversidad y el Bienestar.
Se sabe que el cambio climatico es una realidad y cada día se tiene unas temperaturas más altas, por lo que es de suma importancia investigar este fenómeno desde distintas perspectivas, es por eso que en este trabajo se observa el cambio clímatico desde los 1850s hasta la actualidad, observando las zonas en donde mayor ha habido cambios.

![image](https://github.com/dafelisioso/Servicio-social/assets/67986088/c062c28b-aeb3-416e-a861-33fe1f5da950)


Queremos ver como se comporta la temperatura en las distitnas regiones de ICC
![5dbb6c14-c126-45ba-bf77-71d3847e0884](https://github.com/dafelisioso/Servicio-social/assets/67986088/17028b97-9507-423a-aa2e-95cdc6ef64af)
![4467e6b6-6812-4b52-9d5f-0041d5188800](https://github.com/dafelisioso/Servicio-social/assets/67986088/6dc0ac44-c6a6-4752-9a01-435c36321161)
Como se puede observar el aumento de la temperatura se ha comportado de manera diferente en cada región por lo que es importante verlas de manera independiente pero también de manera conjunta,por lo que nos interesa ver como son las correlaciones entre estas regiones.
![1f4e26aa-915f-41b1-99fe-3716e6c4a7d9](https://github.com/dafelisioso/Servicio-social/assets/67986088/e54840ed-7830-4847-960b-222a05225d9b)
Donde logramos observar que en efecto hay partes del planeta las cuales estan muy correlacionadas en cuestión de la temperatura, suelen ser las que estan cerca entre si o comparten latitudes parecidas.

Queremos observar si existen ciertos periodos que se repiten a lo largo del tiempo en las regiones, por lo que vamos a utilizar la transformada de Fourier para conseguir su espectro.
![0e52c4d1-8f84-48bf-be97-b8af4b8b9d64](https://github.com/dafelisioso/Servicio-social/assets/67986088/d47eceed-1a48-4a3d-8b47-938cb05a74cf)



Los datos de temepratura y climatología que vienen con datos geográficos se sacan cada mes, por lo que no nos sirven mucho si queremos tener un análisis más detallado, el cual ahora quermos tener los datos diarios globales.
Donde les sacaremos su Transformada rápida de Fourier y a esta veremos su espectro de potencias  para cada decada, en donde se van a observar datos interesantes y como es que ha cambiado el comportameinto de la temperatura a lo largo del tiempo.
Primero vamos a dividir el espectro de potencias en dos partes diferentes aquellos datos que son de 0 a 1 mes y los de 1.5 a 6 meses, para ver la pendiente de cada uno de estos en cada década.![f4ecd21f-3f05-44f7-944b-34ea6972715e](https://github.com/dafelisioso/Servicio-social/assets/67986088/0c0888d0-2c6b-42c4-aeca-c10e5132b194)
![7b92b182-fc8a-4838-bdc3-3a46b04eebde](https://github.com/dafelisioso/Servicio-social/assets/67986088/fb299e46-0d56-47bd-8e3f-8157d7affaed)
Como se puede ver en la ultima figura  e han ido separando las pendientes de pequeña y mediana escala, por lo que se ha perdido cierta relación entre estas dando a entender que existe mayor variación de temepraatura en las ultimas décadas, entonces para entrar más a detalle con esto vamos a comparar el RMSE de un ajuste lineal que abarrque todo el espectro y uno de grado 2, con lo que se obtiene lo siguiente.![42b2451f-c8cb-4834-bcb2-a925f540635a](https://github.com/dafelisioso/Servicio-social/assets/67986088/9ee0f2cb-0e6a-4296-83b4-31ab2951017b)
Decade  Linear Slope  Linear Intercept    Linear RMSE  Nonlinear Coeff a2  \
0     1880     -1.813152          0.121576   91079.790458           -0.432310   
1     1890     -1.729628          0.330065   75954.940482           -0.398875   
2     1900     -1.749620          0.342929   90713.606891           -0.466359   
3     1910     -1.785354          0.293711  108791.413856           -0.516662   
4     1920     -1.863757          0.186631  163698.070265           -0.467239   
5     1930     -1.943418          0.103534  258255.134252           -0.539274   
6     1940     -1.886514          0.127273  172726.748252           -0.611500   
7     1950     -1.958656          0.123962  307698.202623           -0.662121   
8     1960     -1.976155          0.177596  401842.042085           -0.703486   
9     1970     -1.908615          0.236972  265946.938371           -0.669562   
10    1980     -2.008926          0.146430  487216.029552           -0.695448   
11    1990     -2.026255          0.173656  595817.952331           -0.752776   
12    2000     -2.022800          0.133577  530616.553142           -0.708008   
13    2010     -2.016115          0.118820  483767.539966           -0.736562   
14    2020     -2.045073         -0.498101   17909.855631           -0.760815   

    Nonlinear Coeff a1  Nonlinear Coeff a0  Nonlinear RMSE  
0            -2.800788           -0.290566     4354.701584  
1            -2.640967           -0.050305     5395.974900  
2            -2.815145           -0.101794     4192.496461  
3            -2.965811           -0.198981     4668.281868  
4            -2.931189           -0.258810     1985.303912  
5            -3.175537           -0.410722     2773.316177  
6            -3.283519           -0.455700     2580.923327  
...
11           -3.746177           -0.544196     5381.520432  
12           -3.640283           -0.541401     3520.876194  
13           -3.698992           -0.583570     4704.260139  
14           -3.731645           -1.188971      479.269731  
