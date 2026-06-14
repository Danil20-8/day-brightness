#!/bin/bash
# build.sh - скрипт сборки DEB пакета в RAM (/tmp)

set -e

PACKAGE_NAME="day-brightness"

# Цвета для вывода
GREEN='\033;32m'
YELLOW='\033;1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Building $PACKAGE_NAME DEB package ===${NC}"

# Сдвигаем рабочую зону на один уровень вверх от папки, где лежит build.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"

BUILD_DIR="$(mktemp -d -t deb-build-XXXXXX)"
PACKAGE_DIR="$BUILD_DIR/$PACKAGE_NAME"

# Автоматическая очистка RAM при любом выходе
trap 'rm -rf "$BUILD_DIR"' EXIT

# Создание скелета пакета
mkdir -p "$PACKAGE_DIR"/{"DEBIAN","usr/local/bin","usr/local/lib/$PACKAGE_NAME","usr/share/doc/$PACKAGE_NAME","usr/lib/systemd/user","lib/systemd/system"}

# 1. Скрипты пакета (DEBIAN)
cp -r "$SCRIPT_DIR/DEBIAN" "$PACKAGE_DIR/" 2>/dev/null || true
chmod 755 "$PACKAGE_DIR/DEBIAN/"* 2>/dev/null || true
chmod 644 "$PACKAGE_DIR/DEBIAN/control" 2>/dev/null || true

# 2. Файлы приложения (app/) — теперь ВСЕ скрипты остаются в одной папке
echo -e "${YELLOW}Copying application files...${NC}"
cp -r "$SCRIPT_DIR/app"/* "$PACKAGE_DIR/usr/local/lib/$PACKAGE_NAME/" 2>/dev/null || true
chmod 755 "$PACKAGE_DIR/usr/local/lib/$PACKAGE_NAME/update-brightness.sh" 2>/dev/null || true

# Создаем системную кнопку запуска в /usr/local/bin
# Она принудительно переносит процесс в рабочую папку скриптов перед стартом
cat > "$PACKAGE_DIR/usr/local/bin/update-brightness" << 'EOF'
#!/bin/bash
cd /usr/local/lib/day-brightness/ && ./update-brightness.sh "$@"
EOF
chmod 755 "$PACKAGE_DIR/usr/local/bin/update-brightness"

# 3. Документация и лицензия (корень проекта)
cp "$SCRIPT_DIR"/{README.md,config.example} "$PACKAGE_DIR/usr/share/doc/$PACKAGE_NAME/" 2>/dev/null || true
cp "$SCRIPT_DIR/LICENSE" "$PACKAGE_DIR/usr/share/doc/$PACKAGE_NAME/copyright" 2>/dev/null || true

# 4. Рабочие файлы Systemd (systemd/)
echo -e "${YELLOW}Copying systemd services...${NC}"
cp "$SCRIPT_DIR/systemd"/{day-brightness.service,day-brightness.timer} "$PACKAGE_DIR/lib/systemd/system/" 2>/dev/null || true
cp "$SCRIPT_DIR/systemd/user"/{day-brightness.service,day-brightness.timer} "$PACKAGE_DIR/usr/lib/systemd/user/" 2>/dev/null || true
chmod 644 "$PACKAGE_DIR/lib/systemd/system/"* "$PACKAGE_DIR/usr/lib/systemd/user/"* 2>/dev/null || true

# 5. Очистка от кэша Python перед сборкой
find "$PACKAGE_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true

# 6. Сборка пакета
echo -e "${YELLOW}Building DEB package...${NC}"
mkdir -p "$SCRIPT_DIR/releases"
DEB_FILE="${PACKAGE_NAME}.deb"

cd "$BUILD_DIR"
dpkg-deb --build --root-owner-group "$PACKAGE_NAME" "$SCRIPT_DIR/releases/$DEB_FILE"

echo -e "${GREEN}✓ Package built successfully: $SCRIPT_DIR/releases/$DEB_FILE (${NC}$(du -h "$SCRIPT_DIR/releases/$DEB_FILE" | cut -f1)${GREEN})${NC}"
