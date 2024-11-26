# Use the official Node.js image as the base image for building
FROM node:18 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json for dependencies
COPY package*.json ./

# Install only the necessary dependencies for building the app
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN npm run build

# Use the official Node.js image for the final stage to keep the image lightweight
FROM node:18-alpine AS runner

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files from the builder stage
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Expose the port the app runs on
EXPOSE 8000

# Set the environment to production
ENV NODE_ENV production

# Start the Next.js application
CMD ["npm", "start"]