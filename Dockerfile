# Multi-stage build for magi-cal-display
# Stage 1: Build Vue.js frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend files (will be created)
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend with static files
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend from stage 1
COPY --from=frontend-builder /frontend/dist ./static

# Expose port
EXPOSE 3000

# Run the application
CMD ["python", "main.py"]
