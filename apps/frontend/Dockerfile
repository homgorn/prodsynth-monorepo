# ─── Multi-stage Dockerfile for ProdSynth Frontend ──────────────────────
# Stage 1: Builder
FROM node:20-alpine AS builder

WORKDIR /app/

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build Next.js (static export or standalone)
RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine

WORKDIR /app/

# Install runtime dependencies (only what's needed)
RUN npm install -g serve

# Copy built application from builder
COPY --from=builder /app/.next ./.next/
COPY --from=builder /app/public ./
COPY --from=builder /app/package.json ./
COPY --from=builder /app/next.config.mjs ./

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Run with serve (or next start if standalone)
CMD ["npm", "start"]
