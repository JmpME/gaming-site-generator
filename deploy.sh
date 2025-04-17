#!/bin/bash

# Версия бота
VERSION="2.1.0"

# Создаем архив с новой версией
echo "📦 Creating deployment package v$VERSION..."
zip -r deploy_v${VERSION}.zip bot.py config.json requirements.txt templates/* generators.py render.yaml

# Здесь нужно добавить команды для загрузки на сервер
# Например:
# scp deploy_v${VERSION}.zip user@your-server:/path/to/bot/

echo "✅ Deployment package created: deploy_v${VERSION}.zip"
echo "⚠️ Please upload the package to your server manually or configure automatic deployment" 