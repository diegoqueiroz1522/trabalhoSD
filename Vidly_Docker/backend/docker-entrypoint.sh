#!/bin/sh

echo "Waiting for MongoDB to start..."
./wait-for db1:27017 
./wait-for db2:27017 

echo "Migrating the databse..."
npm run db1:up 
npm run db2:up 

echo "Starting the server..."
npm start 