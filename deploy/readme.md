
```s
                                                   [supervisor]
                                                         â†“
[chrome] ----> [nginx] <---- (port/socket_file) ----> [uwsgi] ----> [flask]
```

- `Fatal Python error: Py_Initialize: Unable to get the locale encoding`