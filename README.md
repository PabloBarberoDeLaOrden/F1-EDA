# ¿Ha logrado la nueva normativa de la F1 hacer de esta un deporte más competitivo?

## Análisis exploratorio de datos de la Fórmula 1

### Pablo Barbero De La Orden


## Objetivo y contexto del trabajo
La Fórmula 1 es reconocida como el deporte rey dentro del mundo del motor, sin embargo el entorno que rodea al mundo de la Fórmula 1 no se resume exclusivamente en ser una serie de vehículos que giran alrededor de un circuito. 

La Fórmula 1 es la principal culpable de la inversión e  investigación en la automoción, logrando llevar muchas de las piezas diseñadas que en un principio eran para competir al parque automovilístico mundial.

Con ello quiero decir que esta entidad es una matriz que está en continuo movimiento y expansión, obligando a renovar su normativa prácticamente de manera anual.
Muchos de los cambios de normativa que se han realizado a lo largo de la historia tenían distintos propósitos, la inclusión del ‘DRS’ con el que facilitar los adelantamientos, la inclusión de ‘Halo’ en la carrocería con la intención de garantizar una mayor seguridad al piloto. 
Y el reciente cambio de normativa que obligaba a cambiar por completo el diseño de los automóviles cuyo propósito es facilitar a los vehículos que sigan al anterior. Este cambio de normativa no gira entorno a un factor deportivo como puede ser la seguridad del piloto. Este cambio tiene el propósito de ofrecer un mejor ‘show’ que haga de la Fórmula 1 un entretenimiento más adictivo.

Desde mi punto de vista un deporte resulta más entretenido cuánto más competido es.
 Por ello se ha decidido estudiar si la nueva normativa ha permito a la Fórmula 1 ser un deporte más competitivo, a través de un análisis exploratorio de datos se buscarán las temporadas más dominantes y se compararán la última con estás y la actual.

## Datos empleados

Los datos empleados constan de una serie de ficheros extraídos a través de la siguiente dirección: http://ergast.com/mrd/db/#csv 

## Reestructuración de los datos 

Recordando nuestro objeto de estudio, la obtención de nuestra conclusión se basará en la comparación de las temporadas. Sin embargo el sistema de puntos se ha visto variado a lo largo de los años. Por lo tanto en primer lugar se va a dar el sistema de puntos actual a todas las temporadas para realizar comparaciones más veraces, a su vez el punto extra por vuelta rápida no existía por lo que no se valorará tampoco.

También se construirá un nuevo dato con la información acerca de la posición de parrilla y puesto final, de manera que restando ambas obtenemos la cantidad de puestos que ha ganado en carrera.

## Resumen de la temporada actual

Se han desarrollado una serie de indicadores orientativos para resumir de manera directa la temporada 2022.

Los aspectos que se han estudiado se dividen en dos ramas, por identificación de piloto o bien por identificación de constructor.

En primer lugar, la clasificación de pilotos y constructores dónde se refleja como la escudería Red Bull ha dominado esta temporada, abanderada principalmente por su piloto Max Verstappen, que a pesar de que falten aún 4 carreras ya es matemáticamente campeón del mundo.

Esta casuística puede suscitar que ha sido una de las temporadas más dominantes de la historia de la Fórmula 1 o al menos que no ha sido una temporada muy competitiva en cuanto a ganadores se refiere.

Sin embargo, queda reflejado cómo los Ferrari son mejor coche a una vuelta, como se puede ver que le saca más del doble de poles position y ambos disponen de la misma cantidad de vueltas rápidas. 

Aunque cómo se puede ver Red Bull dispone de un coche más consistente, entendiendo como consistencia al factor de ser regular y no tener fallos en el coche. Ya que las los Red Bull pierden la mitad de posiciones en carrera.

## Identificación de temporadas más dominantes

Como bien hemos comentados las temporadas de Fórmula 1 son cambiantes y han visto como el sistema de puntajes o el número de circuitos se ven alterados. Debido a esta situación y para una mejor comprensión de nuestros indicadores, se va normalizar los indicadores dividiéndolos por el número de carreras, de esta manera se obtendrá sus proporciones.

Por lo que se indicara los puntos por gran premio del ganador, la proporción de pódiums, de póles, de vueltas rápidas y las posiciones ganadas en carrera. 
Cabe destacar que sólo se recoge información acerca de las vueltas rápidas a partir del año 2004, por ello no se presenta ninguna información anterior.
Pudiendo de esta manera identificar cómo la temporada de Michael Schumacher en 2002, ha sido la más dominante de la F1. Habiendo estado en el podio todas las carreras, consiguiendo 22 puntos de media.

Otra temporada a tener en cuenta es la que realizó Vettel en 2011, quizá no fue la mejor en tiempo de carrera pero si lo fue a una vuelta ya que obtuvo la pol position en alrededor de un 80% de las carreras y disponiendo de unos 20 puntos por carrera, uno de los valores más altos.

## Comparación entre la temporada actual y las más dominantes

Como ya hemos comentado a lo largo del estudio, la comparación entre distintas temporadas resulta una acción complicada ya que estas se desarrollaban en distintos momentos del tiempo, con sus factores concretos cada una. Por ello no resultaría lógico comparar de manera directa a los campeones de cada temporada entre sí.

Lo que realmente se va a estudiar son las rivalidades que tuvieron los campeones con su perseguidor, los cuales estaban emplazados en el mismo momento del tiempo y con las mismas condiciones. Estas rivalidades si se podrán comparar entre temporadas.

Se puede observar como en la temporada 2002, a partir del primer tercio de la temporada el gap entre Ferrari y sus rivales incrementa exponencialmente. Partiendo de una diferencia de 1 punto llegando a tener una de casi 300 a final de temporada.

En la temporada 2011, la situación de Vettel y Red Bull fue distinta. Desde un principio partieron con ganadores y 7 durante toda la temporada fueron aumentando el gap, demostrando una dominancia durante toda la temporada y no a partir de un sector de ella como fue en el caso de 2002. 

La temporada 2022 tiene similitudes y diferencias con estas,  por ejemplo esta temporada es similar a la de Michael ya que Max comenzó por debajo de su rival y a partir de una fase de la temporada comenzó a aumentar su gap con el rival. Sin embargo, el gap final con su rival no es tan grande. Aunque cabe recordar que la temporada aún no ha finalizado.

Pudiendo de esta manera decir que esta temporada se asemeja a una de las más dominantes de la Fórmula 1 en cuanto a la competición por la primera plaza se refiere.

## Comparación entre la temporada actual y la anterior

En cuanto a la comparación con la última temporada, nos encontramos unos escenarios contrapuestos en cuanto a dominancia se refiere.

Podemos observar como la disputa por el campeonato se alargó durante toda la temporada, siendo esta temporada una de las más competidas de toda la historia, concretamente se decidió por un punto que se obtuvo en un adelantamiento en la última vuelta.

Por lo tanto se determina que la dominancia respecto al rival con el cambio de normativa ha aumentado, lo que puede llevar a entender que la nueva normativa no ha alcanzado el objetivo que realmente buscaba.

Sin embargo, resumir la competitividad exclusivamente al primer y segundo puesto no resulta plenamente acertado, recordemos que otros 18 pilotos también disputan la competición, por ello habría que abstraerse y comparar también el resto de la parrilla.

## Conclusión

Tras realizar un estudio intensivo acerca de la dominancia en la Fórmula 1 podemos detallar que esta temporada dispone de características similares a aquellas temporadas dónde un piloto y su escudería fueron abusivamente dominantes. Por lo que el ‘show’ de esas temporadas perdió interés a medida que transcurrían los Grandes Premios.

Esto nos podría llevar a entender que el objetivo principal del nuevo reglamento no logró su acometido principal, más aún si lo comparamos con la temporada anterior donde tuvimos el campeonato más competido de los últimos años.

Si bien es cierto que se ha logrado una mayor competitividad entre el resto de escuderías, llegando incluso a acercar a escuderías no acostumbradas a puntuar a situarse en puestos cercanos a la cabeza.

Históricamente después de un cambio de normativa tan grande suele aparecer un equipo que ‘da con la tecla’ y construye el mejor coche. Luego quizá basarse exclusivamente en el campeón con tan sólo una temporada en la que la normativa está vigente no resulta concluyente.

Por ello considero que habría que realizar este análisis a posteriori, pero en principio sí que la normativa logra su acometido. El de acercar en mayor medida a todos los coches de la parrilla, a pesar de que se descuelgue uno como es el campeón.

