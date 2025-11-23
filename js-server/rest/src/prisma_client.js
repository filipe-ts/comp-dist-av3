const { PrismaClient } = require('@prisma/client');

const prisma_client = () => new PrismaClient(
    { log: ['query', 'info', 'warn', 'error'] }
);

module.exports = prisma_client;
