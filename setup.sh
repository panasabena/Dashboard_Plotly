#!/bin/bash

echo "🚀 Configurando Dashboard de Telecomunicaciones"
echo "================================================"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.11+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Instalación completada!"
echo ""
echo "🎯 Para ejecutar el dashboard:"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "🌐 El dashboard estará disponible en: http://localhost:8050"
echo ""
echo "📊 Para análisis adicional:"
echo "   python analysis.py"
