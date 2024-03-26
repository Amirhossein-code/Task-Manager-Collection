FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package.json .

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .


# Build the React application

# Expose React Port
EXPOSE 5173

# Command to start the React application
CMD ["npm", "start"]
