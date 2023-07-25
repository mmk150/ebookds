# Use official Node.js runtime as base image
FROM node:alpine as react-build

# Set the working directory in the Docker image
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application to the working directory
COPY . ./

# Build the React.js applicati
RUN npm run build


FROM nginx
COPY --from=react-build /app/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]