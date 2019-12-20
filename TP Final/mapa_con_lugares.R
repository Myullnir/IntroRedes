library("leaflet")
library("dplyr")

# Asegurarse de estar en el directorio del TP-Final
works_3meses <- read.csv("works_3meses.csv")
noworks_3meses <- read.csv("noworks_3meses.csv")

leaflet(noworks_3meses) %>% addTiles() %>% 
addCircleMarkers(stroke=FALSE,color="red")


leaflet(works_3meses) %>% addTiles() %>% 
addCircleMarkers(stroke=FALSE,opacity=1,color="green",fillOpacity=1,radius=30)



sem8 <- read.csv("NY_3meses/nw_NY_3meses_Semana 8.csv")
colores <- sem8$color
opacidad <- sem8$opacidad
radio <- sem8$radio
leaflet(sem8) %>% addTiles() %>% addCircleMarkers(stroke=FALSE,color=colores,fillOpacity=opacidad,radius=radio,
    popup = paste("(",sem8$lat,",",sem8$long,")"," <br>", sem8$checkins, " checkins"))