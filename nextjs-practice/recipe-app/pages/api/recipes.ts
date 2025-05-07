// pages/api/recipes.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { prisma } from '../../lib/prisma'; // Prisma Client

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    // POST リクエストの場合の処理
    const { slug, title, description, ingredients, instructions } = req.body;

    // バリデーション (必須フィールドの確認など) を行うことが推奨されます

    try {
      // データベースに新しいレシピを作成
      const newRecipe = await prisma.recipe.create({
        data: {
          slug,
          title,
          description,
          ingredients, // 文字列の配列として渡す
          instructions, // 文字列の配列として渡す
        },
      });

      // 作成成功のレスポンス
      res.status(201).json(newRecipe);

    } catch (error) {
      // エラーハンドリング
      console.error('Error creating recipe:', error);
      // slug 重複などのエラーも考慮し、適切なステータスコードとメッセージを返す
      res.status(500).json({ message: 'レシピの作成に失敗しました。' });
    }

  } else {
    // POST 以外のリクエストメソッドは許可しない
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}