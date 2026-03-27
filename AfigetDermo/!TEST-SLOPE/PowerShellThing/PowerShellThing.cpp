#define WIN32_LEAN_AND_MEAN
#include <windows.h>

LRESULT CALLBACK WP(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    // WP : Window Procedure Процедура обработки событий на окно для обработчика
    static HBRUSH brush = NULL;

    switch (uMsg) {

        case WM_ERASEBKGND: {
            return 1;
        }

        case WM_PAINT: {
            PAINTSTRUCT ps;
            BeginPaint(hwnd, &ps);
            EndPaint(hwnd, &ps);
            return 0;
        }
        case WM_NCPAINT: return DefWindowProc(hwnd, uMsg, wParam, lParam);

        case WM_GETICON:
        case WM_QUERYDRAGICON: return 0;

        case WM_CLOSE:
            DestroyWindow(hwnd);
            return 0;

        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;

    }
    // DWP: Default Window Procedure Обработчик стандартных процедур (закрытие окна при нажатии крестика, изменение размера и т.д. т.п.)
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}

int WINAPI WinMain(HINSTANCE h, HINSTANCE hPrevI, LPSTR lpTrafPS, int nShowPS) {
    const char Title[] = "App";

    WNDCLASS wc = {};
    wc.lpfnWndProc = WP;
    wc.hInstance = h;
    wc.lpszClassName = Title;
    wc.hbrBackground = NULL;
    wc.hIcon = NULL;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        WS_EX_DLGMODALFRAME,
        Title,
        "",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT,
        800, 600,
        NULL,
        NULL,
        h,
        NULL
    );

    ShowWindow(hwnd, nShowPS);
    UpdateWindow(hwnd);

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}