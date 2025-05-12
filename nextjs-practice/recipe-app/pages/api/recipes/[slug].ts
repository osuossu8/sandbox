// pages/api/recipes/[slug].ts
import { NextApiRequest, NextApiResponse } from 'next';
import { prisma } from '../../../lib/prisma'; // Prisma Client インスタンスをインポート

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // 動的ルートのパラメータからレシピスラッグを取得
  const { slug } = req.query;

  // *** API が受け取ったスラッグをログ出力 ***
  console.log('API received DELETE request for slug:', slug);

  // スラッグが文字列であることを確認
  if (typeof slug !== 'string') {
    console.error('Invalid slug type received by API:', typeof slug); // Debug log
    return res.status(400).json({ message: '無効なレシピスラッグです。' });
  }

  // DELETE リクエストのみを受け付ける
  if (req.method === 'DELETE') {
    try {
      // *** 削除前にレシピが存在するか確認するログ (任意だがデバッグに有効) ***
      const recipeToDelete = await prisma.recipe.findUnique({
          where: { slug: slug },
      });
      console.log('API found recipe to delete:', recipeToDelete); // Debug log

      if (!recipeToDelete) {
          // 見つからなかった場合は P2025 エラーが発生するはずですが、事前にチェックすることも可能
          console.warn(`API: Recipe with slug ${slug} not found before deletion attempt.`); // Debug log
          return res.status(404).json({ message: '指定されたスラッグのレシピは見つかりませんでした。' });
      }


      // 指定されたスラッグのレシピをデータベースから削除
      // Prisma の delete は @unique フィールドを where 条件に指定できます
      const deletedRecipe = await prisma.recipe.delete({
        where: { slug: slug }, // スラッグを条件に指定して削除
      });

      // 削除成功のレスポンス
      console.log(`API: Recipe with slug ${slug} successfully deleted.`); // Debug log
      res.status(200).json({ message: `レシピ (スラッグ: ${slug}) が正常に削除されました。`, deletedId: deletedRecipe.id });

    } catch (error) {
      // エラーハンドリング
      console.error(`API Error deleting recipe with slug ${slug}:`, error);

      // 指定されたスラッグのレシピが見つからなかった場合のエラー (P2025)
      if (error instanceof Error && 'code' in error && error.code === 'P2025') {
         console.warn(`API: Prisma P2025 error - Recipe with slug ${slug} not found during delete operation.`); // Debug log
         return res.status(404).json({ message: '指定されたスラッグのレシピは見つかりませんでした。' });
      }

      // その他のデータベースエラー
      res.status(500).json({ message: 'レシピの削除に失敗しました。' });
    }

  } else {
    // DELETE 以外のリクエストメソッドは許可しない
    res.setHeader('Allow', ['DELETE']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
