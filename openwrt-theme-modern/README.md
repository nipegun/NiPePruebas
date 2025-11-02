# luci-theme-modern

`luci-theme-modern` es un theme moderno y responsivo para la interfaz web LuCI de OpenWrt. El objetivo es ofrecer una apariencia actual, con modo oscuro/claro, tipografía legible y componentes reutilizables pensados para paneles de control.

## Características

- Diseño basado en CSS Grid y Flexbox, con escala fluida entre 320px y 1920px.
- Alternancia entre modo claro y oscuro controlada desde la interfaz.
- Layout modular con encabezado compacto, barra lateral plegable y contenido con tarjetas.
- Paleta de colores accesible, cumpliendo contraste mínimo AA.
- Iconografía SVG ligera y animaciones suaves.

## Estructura

```text
luci-theme-modern/
├── Makefile
├── README.md
├── htdocs/
│   └── luci-static/
│       └── modern/
│           ├── css/style.css
│           ├── js/theme.js
│           └── media/
├── luasrc/
│   └── view/
│       └── themes/
│           └── modern/
│               ├── header.htm
│               ├── footer.htm
│               ├── login.htm
│               ├── index.htm
│               └── partials/
│                   └── navigation.htm
└── root/
    └── etc/
        └── uci-defaults/
            └── 99-theme-modern
```

## Instalación en entorno de desarrollo

1. Copia la carpeta dentro de `feeds/luci/themes/` o en `package/` dentro del árbol de OpenWrt.
2. Actualiza los feeds y selecciona el paquete:

```sh
./scripts/feeds update luci
./scripts/feeds install luci-theme-modern
make menuconfig  # LuCI -> Themes -> luci-theme-modern
```

3. Compila únicamente el paquete durante el desarrollo:

```sh
make package/luci-theme-modern/{clean,compile} V=sc
```

4. Copia el paquete `.ipk` generado a tu router o entorno de pruebas:

```sh
scp bin/packages/*/luci/luci-theme-modern_*.ipk root@192.168.1.1:/tmp
ssh root@192.168.1.1 opkg install /tmp/luci-theme-modern_*.ipk
```

5. Selecciona el theme desde `Sistema > Sistema > Language and Style` o edita `/etc/config/luci`:

```sh
uci set luci.main.mediaurlbase='/luci-static/modern'
uci commit luci
/etc/init.d/uhttpd restart
```

## Instalación directa desde la línea de comandos del router

Si ya cuentas con el firmware OpenWrt instalado y únicamente deseas añadir el theme en un router en producción, puedes realizar todo el proceso desde la shell del dispositivo siguiendo estos pasos:

1. Conéctate por SSH al router y asegúrate de tener conectividad a Internet para descargar el paquete:

   ```sh
   ssh root@192.168.1.1
   opkg update
   ```

2. Descarga el paquete `.ipk` publicado (sustituye la URL por la versión más reciente de tus artefactos). Si prefieres copiarlo manualmente, también puedes usar `scp` desde tu equipo de desarrollo.

   ```sh
   # Ejemplo usando wget desde el router
   cd /tmp
   wget https://tu-servidor/paquetes/luci-theme-modern_1.0.0_all.ipk

   # Alternativa desde tu PC:
   scp luci-theme-modern_1.0.0_all.ipk root@192.168.1.1:/tmp/
   ```

3. Instala el paquete y limpia el archivo temporal una vez finalizado:

   ```sh
   opkg install /tmp/luci-theme-modern_1.0.0_all.ipk
   rm /tmp/luci-theme-modern_1.0.0_all.ipk
   ```

4. Configura el theme como predeterminado y reinicia el servidor web para aplicar los cambios:

   ```sh
   uci set luci.main.mediaurlbase='/luci-static/modern'
   uci commit luci
   /etc/init.d/uhttpd restart
   ```

5. Si deseas volver al theme anterior, restaura el valor previo (por ejemplo `/luci-static/bootstrap`) y reinicia de nuevo `uhttpd`.

## Personalización

- Ajusta variables CSS en `:root` para cambiar paleta y tipografía.
- Sustituye iconos en `htdocs/luci-static/modern/media/` o agrega referencias a catálogos SVG.
- Modifica los bloques `navigation` y `header` dentro de `luasrc/view/themes/modern/partials` para añadir enlaces o estadísticas.

## Créditos

Inspirado por themes comunitarios como `luci-theme-material` y `luci-theme-argon`, adaptado a las necesidades del proyecto OSINTIA.
