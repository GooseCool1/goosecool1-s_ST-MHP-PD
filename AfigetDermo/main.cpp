#include "!includes.h"
/*
1. Определение MIME-типов по расширениям


*/

const int PORT = 12345;
const std::string WWW_ROOT = "./www";

const int bufferSize = 8192;

// http://[IP]:555/ru/dev

/*
= = Port Forwarding = = Маршрутизация = =
Внутренний хост LAN для маршрутизатора  :
> Принимает 0.0.0.0:12345
>
...
Внешний хост WAN для пользователей WWW  :
> Транслирует [IP]:[PORT] (например:555)
>
...

Представляю маштабирование
Представляю глубокий контроль
*/

int main() {
    int socketDescriptor;
    struct sockaddr_in serverAddress;
    int opt = 1; //

    return 0;
}
