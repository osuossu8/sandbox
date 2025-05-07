// lib/prisma.ts
// import { PrismaClient } from '@prisma/client'; // not working
import { PrismaClient } from '../generated/prisma';

// 開発環境ではホットリロードによる新しいインスタンスの作成を防ぐための処理
const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query', 'info', 'warn', 'error'], // オプション: 実行されるSQLログなどが見れる
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;