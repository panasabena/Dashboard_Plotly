#!/bin/bash

echo "🚀 Configurando Entorno Anaconda - Dashboard de Telecomunicaciones"
echo "=================================================================="

# Verificar si conda está instalado
if ! command -v conda &> /dev/null; then
    echo "❌ Anaconda no está instalado. Por favor instala Anaconda o Miniconda"
    exit 1
fi

echo "✅ Anaconda encontrado: $(conda --version)"

# Crear entorno Charter
echo "📦 Creando entorno Charter..."
conda env create -f environment.yml

# Activar entorno
echo "🔧 Activando entorno Charter..."
conda activate Charter

echo "✅ Configuración completada!"
echo ""
echo "🎯 Para activar el entorno:"
echo "   conda activate Charter"
echo ""
echo "🚀 Para ejecutar el dashboard:"
echo "   python app.py"
echo ""
echo "🌐 El dashboard estará disponible en: http://localhost:8050"
echo ""
echo "📊 Para análisis adicional:"
echo "   python analysis.py"
echo ""
echo "📋 Para ver todos los entornos:"
echo "   conda env list"
echo ""
echo "🗑️  Para eliminar el entorno (si es necesario):"
echo "   conda env remove -n Charter"
