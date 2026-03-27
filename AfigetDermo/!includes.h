#include <iostream>
#include <string>
#include <cstring>
#include <fstream>
#include <sstream>
#include <map>
#include <unistd.h>

#include <string_view>
#include <array>
#include <cstdint>
/*
== WINDOWS MinGW thing ==
#include <winsock2.h>
#include <ws2tcpip.h>

== LINUX   WSL   thing ==
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
*/

// I like WSL~~... UwU
// But...I will use MinGW...Because I'am peace of shit.
#include <winsock2.h>
#include <ws2tcpip.h>

#include "getMIME.hpp"