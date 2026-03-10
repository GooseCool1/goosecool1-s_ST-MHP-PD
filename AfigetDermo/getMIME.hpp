#pragma once

#include <string_view>
#include <array>
#include <cstdint>

class listMIME {
private:
    static constexpr std::array<std::string_view, 13> TYPES = {{
        "application/octet-stream",  // 0 - default
        "text/css",                   // 1 - css
        "text/html",                   // 2 - htm, html
        "image/jpeg",                   // 3 - jpg, jpeg
        "image/png",                     // 4 - png
        "image/gif",                      // 5 - gif
        "image/svg+xml",                  // 6 - svg
        "text/plain",                      // 7 - txt
        "application/pdf",                  // 8 - pdf
        "application/xml",                   // 9 - xml
        "application/json",                   // 10 - json
        "application/javascript",               // 11 - js
        "text/html"                              // 12 - htm
    }};
    static constexpr uint32_t fast_hash(const char* ext) noexcept {
        return (static_cast<uint8_t>(ext[0]) << 16) |
               (static_cast<uint8_t>(ext[1]) << 8)  |
               (static_cast<uint8_t>(ext[2]));
    }

public:
    static std::string_view from_path(std::string_view path) noexcept {
        size_t dot = path.rfind('.');
        if (dot == std::string_view::npos) [[unlikely]]
            return TYPES[0];

        std::string_view ext = path.substr(dot + 1);
        size_t len = ext.length();

        if (len < 2 || len > 4) [[unlikely]]
            return TYPES[0];

        switch (fast_hash(ext.data())) {
            //htm&html
            case fast_hash("htm"):
                if (len == 3) return TYPES[2];
                if (len == 4 && ext[3] == 'l') return TYPES[2];
                break;
            //len2
            case fast_hash("js"): if (len == 2) return TYPES[11]; break;
            //len3
            case fast_hash("css"): if (len == 3) return TYPES[1]; break;
            case fast_hash("jpg"): if (len == 3) return TYPES[3]; break;
            case fast_hash("png"): if (len == 3) return TYPES[4]; break;
            case fast_hash("gif"): if (len == 3) return TYPES[5]; break;
            case fast_hash("svg"): if (len == 3) return TYPES[6]; break;
            case fast_hash("txt"): if (len == 3) return TYPES[7]; break;
            case fast_hash("pdf"): if (len == 3) return TYPES[8]; break;
            case fast_hash("xml"): if (len == 3) return TYPES[9]; break;
            //len4
            case fast_hash("jpe"):
                if (len == 4 && ext[3] == 'g') return TYPES[3];
                break;
            case fast_hash("jso"):  // json
                if (len == 4 && ext[3] == 'n') return TYPES[10];
                break;
        }
        return TYPES[0];
    }
};

inline std::string_view get_mime_type(const char* path) {return listMIME::from_path(path);}
inline std::string_view get_mime_type(const std::string& path) {return listMIME::from_path(path);}
inline std::string_view get_mime_type(std::string_view path) {return listMIME::from_path(path);}