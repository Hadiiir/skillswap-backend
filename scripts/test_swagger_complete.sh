#!/bin/bash

echo "🧪 Testing Swagger endpoints..."

# Wait for server to be ready
echo "⏳ Waiting for server..."
sleep 5

# Test Swagger UI
echo "🔍 Testing Swagger UI..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/swagger/ | grep -q "200" && echo "✅ Swagger UI: OK" || echo "❌ Swagger UI: Failed"

# Test ReDoc
echo "🔍 Testing ReDoc..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/redoc/ | grep -q "200" && echo "✅ ReDoc: OK" || echo "❌ ReDoc: Failed"

# Test OpenAPI Schema
echo "🔍 Testing OpenAPI Schema..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/swagger.json | grep -q "200" && echo "✅ OpenAPI Schema: OK" || echo "❌ OpenAPI Schema: Failed"

# Test API Root
echo "🔍 Testing API Root..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/ | grep -q "200" && echo "✅ API Root: OK" || echo "❌ API Root: Failed"

echo "🎉 Swagger testing complete!"
