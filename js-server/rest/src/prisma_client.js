const { PrismaClient } = require('@prisma/client');

class PrismaClientSingleton {
  constructor() {
    if (!PrismaClientSingleton.instance) {
      console.log('Creating new PrismaClient instance');
      PrismaClientSingleton.instance = new PrismaClient(
        { log: ['query', 'info', 'warn', 'error'] }
      );
    }
  }

  getInstance() {
    return PrismaClientSingleton.instance;
  }
}

const prisma_client = () => {
  const instance = new PrismaClientSingleton();
  return instance.getInstance();
};

module.exports = prisma_client;
