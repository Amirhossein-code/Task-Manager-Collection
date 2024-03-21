# Use an official Node.js image as the base image
FROM node:14 as build

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the working directory
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files to the working directory
COPY . .

# Build the application
RUN npm run build

# Use a lightweight Node.js image for the production build
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the build output from the previous stage to the working directory
COPY --from=build /app/build ./build

# Expose the port that the application runs on
EXPOSE 3000

