#!/bin/bash
set -e

npm install
npm test
docker build -t ant-ai .
docker run -p 3000:3000 ant-ai

echo "✅ ALL SYSTEMS GO"
