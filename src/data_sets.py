# -*- coding: utf-8 -*-

subte_train = [
    (u'Servicio Normalizado', 'positive'),
    (u'Servicio interrumpido', 'negative'),
    (u'Servicio limitado entre Bolívar y Av. La Plata', 'negative'),
    (u'Servicio limitado entre Federico Lacroze y Rubén Darío 04:46 hs', 'negative'),
    (u'Interrupción por una formación detenida debido a un problema técnico', 'negative'),
    (u'Interrupción debido a un problema técnico en una formación', 'negative'),
    (u'Interrumpida debido a la atención médica a un pasajero', 'negative'),
    (u'Interrumpida En breve restablece el servicio', 'negative'),
    (u'Los trenes no se detienen en la estación Fátima', 'negative'),
    (u'Servicio limitado entre estaciones: INT. SAGUIER y CENTRO CÍVICO', 'negative'),
    (u'Servicio con demora por anegamiento de vías', 'negative'),
    (u'Servicio con demora', 'negative'),
    (u'funciona bien Bien', 'positive'),
    (u'funciona normal Normal con normalidad Normalidad', 'positive'),
    (u'funciona mal Mal', 'negative'),
    (u'Hay obras en el subte', 'neutral'),
    (u'Subte no funciona debido a un accidente en las vias', 'negative'),
    (u'El #Premetro no prestará servicio por obras', 'neutral')
]
'''    ,
    (u'Servicio interrumpido', 'negative'),
    (u'Los trenes no se detienen en Av. de Mayo' 'negative'),
    (u'Servicio limitado entre Plaza Miserere y San Pedrito', 'negative'),
    (u'Interrumpido por obras de mejora', 'positive'),
    (u'Servicio limitado entre Federico Lacroze y Rubén Darío 10:23 hs', 'negative'),
    (u'Realiza el recorrido completo entre cabeceras', 'positive'),
    (u'Con demora por una formación detenida debido a un problema técnico', 'negative'),
    (u'Los trenes no se detienen en la estación Fátima', 'negative'),
    (u'Servicio limitado entre Gral. Lemos y Fco. Lynch 19:50 hs', 'negative'),
    (u'El #Premetro no prestará servicio por obras', 'positive'),
    (u'@candlelight_88 Hola Cande, en este momento la Línea B funciona con normalidad. Saludos!', 'positive'),
    (u'¡Hoy celebramos los 102 años del subte', 'positive'),
    (u'@SofiSileo Hola Sofi, no, la Línea B ya reanudó su servicio. Saludos!', 'positive'),
    (u'Las formaciones no se detienen en la estación Avenida de Mayo por operativo de seguridad', 'negative'),
    (u'@Flopynaa Hola, la Línea A ya comenzó a regularizar su servicio. Saludos!', 'positive'),
    (u'@Elianita_Piojo Hola, sí, en este momento la Línea A se encuentra interrumpida. Saludos.', 'negative'),
    (u'Reanuda su servicio y realiza el recorrido completo entre cabeceras', 'positive')
]'''

subte_test = [
    (u'Servicio interrumpido', 'negative'),
    (u'Los trenes no se detienen en Av. de Mayo' 'negative'),
    (u'Servicio limitado entre Plaza Miserere y San Pedrito', 'negative'),
    (u'Interrumpido por obras de mejora', 'positive'),
    (u'Servicio limitado entre Federico Lacroze y Rubén Darío 10:23 hs', 'negative'),
    (u'Realiza el recorrido completo entre cabeceras', 'positive'),
    (u'Ocurrio un accidente en las vias del tren', 'negative')
]

en_train = [
         ('I love this sandwich. ', 'positive'),
         ('This is an amazing place!', 'positive'),
         ('I feel very good about these beers.', 'positive'),
         ('I do not like this restaurant', 'negative'),
         ('I am tired of this stuff.', 'negative'),
         ("I can't deal with this", 'negative'),
         ("My boss is horrible.", "neg")
     ]


en_test = [
     ('the beer was good.', 'positive'),
     ('I do not enjoy my job', 'negative'),
     ("I ain't feeling dandy today.", 'negative'),
     ("I feel amazing!", 'positive'),
     ('Gary is a friend of mine.', 'positive'),
     ("I can't believe I'm doing this.", 'negative')
 ]
