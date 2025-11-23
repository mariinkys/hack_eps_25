## Inspiration
El proyecto surgió a raíz de un reto planteado por bonÀrea en el marco de HackEPS, donde se nos desafiaba a comunicarnos con PLCs industriales utilizando protocolos reales como S7, OPC UA y una interfaz web.
## What it does
Detecta el PLC en la red mediante análisis con nmap.
Controla el NS1 leyendo y escribiendo valores directamente a través del protocolo S7.
Explora todo el servidor OPC UA para descubrir nodos ocultos y controla el NS2 ajustando sus temporizadores.
Analiza Data Blocks (DBs) en formato hexadecimal para identificar credenciales y estructuras internas.
Automatiza combinaciones de timers hasta encontrar la secuencia necesaria para activar los pilotos según las reglas del reto (rojo NS1, azul NS2 y verde NS3),
## How we built it
Utilizamos nmap para descubrir las IPs de los PLCs conectados a la red del hackathon, tal como estaba previsto en la sección “Informació prèvia” del reto.
Usamos python-snap7 para leer y escribir en los Data Blocks del PLC y validar el control del piloto rojo.
Leímos DB1 y DB2, generando hex dumps y comparándolos para identificar offsets, variables y credenciales internas (usuario “hack” y contraseña “Hackathon2025”).
Descubrimos que los timers eran  offsets específicos. Probamos cientos de combinaciones mediante bucles automáticos hasta ajustar la secuencia correcta.
## Challenges we ran into
Encontrar la IP correcta del PLC entre varias en la red del hackathon.
Comprender simultáneamente tres vías de comunicación industrial diferentes.
Entender por qué los timers devolvían valores
Identificar offsets reales dentro de los DBs.
Controlar el PLC sin interferir con otros equipos, siguiendo las restricciones del reto

