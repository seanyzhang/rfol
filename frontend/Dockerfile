# Use Node.js LTS image
FROM node:20

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy the source code
COPY . .

# Vite dev server default port
EXPOSE 5173

# Run Vite dev server
CMD ["npm", "run", "dev"]