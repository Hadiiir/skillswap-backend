#!/bin/bash

echo "🔧 Installing Swagger dependencies..."

# Install Python packages
pip install drf-yasg==1.21.7
pip install packaging
pip install inflection
pip install ruamel.yaml
pip install coreapi
pip install coreschema

echo "✅ Swagger dependencies installed!"

# Update requirements.txt
echo "📝 Updating requirements.txt..."
cat >> requirements.txt << EOF

# Swagger/OpenAPI Documentation
drf-yasg==1.21.7
packaging
inflection
ruamel.yaml
coreapi
coreschema
EOF

echo "✅ Requirements.txt updated!"
echo "🎉 Swagger installation complete!"
