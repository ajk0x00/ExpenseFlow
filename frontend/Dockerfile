FROM node:20-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port Vite runs on
EXPOSE 5173

# Command to run the application in development mode
# --host is necessary to allow access from outside the container
CMD ["npm", "run", "dev", "--", "--host"]
