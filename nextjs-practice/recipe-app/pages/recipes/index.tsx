import Head from 'next/head';
import Link from 'next/link';
import { GetStaticProps } from 'next'; // getStaticProps の型
import { prisma } from '../../lib/prisma'; // 作成した Prisma Client インスタンス
// import { Recipe } from '@prisma/client'; // Prisma Client が生成する Recipe 型
// import { Recipe } from '../../generated/prisma';
import { useState } from 'react';

// コンポーネントが受け取る props の型を定義
interface RecipeListPageProps {
  recipes: {
    id: string;
    slug: string;
    title: string;
    description: string | null;
    ingredients: string[];
    instructions: string[];
    createdAt: string; // Serialized as string
    updatedAt: string; // Serialized as string
  }[]; // データベースから取得したレシピの配列
}

// React コンポーネント
const RecipeListPage: React.FC<RecipeListPageProps> = ({ recipes }) => {
  // props で渡された recipes を使って表示
  const [recipeList, setRecipeList] = useState(recipes);
  const [deletingId, setDeletingId] = useState<string | null>(null); // 削除中のレシピIDを保持 (ボタンの無効化などに使用)
  const [deleteError, setDeleteError] = useState<string | null>(null); // 削除エラーメッセージ用

  // レシピ削除ボタンクリック時のハンドラー関数
  const handleDeleteRecipe = async (recipeSlug: string) => {
    const recipeId = recipeList.find(recipe => recipe.slug === recipeSlug)?.id; // スラッグからレシピIDを取得
    if (!recipeId) {
      console.error(`Recipe with slug ${recipeSlug} not found.`);
      return;
    }
    // 既に削除中の場合は何もしない
    if (deletingId === recipeId) return;

    // ユーザーに確認を求める (任意)
    if (!confirm('このレシピを削除してもよろしいですか？')) {
      return;
    }

    setDeletingId(recipeId); // 削除中のIDを設定
    setDeleteError(null); // エラーメッセージをリセット

    try {
      // 削除用 API エンドポイントに DELETE リクエストを送信
      const response = await fetch(`/api/recipes/${recipeSlug}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        // 削除成功の場合、ステートを更新してリストから削除されたレシピを削除
        setRecipeList(recipeList.filter(recipe => recipe.id !== recipeId));
        console.log(`Recipe with ID ${recipeId} deleted successfully.`);

      } else {
        // API からエラーレスポンスが返された場合
        const errorData = await response.json();
        setDeleteError(errorData.message || 'レシピの削除に失敗しました。');
        console.error(`Failed to delete recipe with ID ${recipeId}:`, response.status, errorData);
      }

    } catch (error) {
      // ネットワークエラーなどの例外が発生した場合
      setDeleteError(`削除中にエラーが発生しました: ${error instanceof Error ? error.message : '不明なエラー'}`);
      console.error(`Error during deletion of recipe with ID ${recipeId}:`, error);

    } finally {
      // 削除処理が完了したら、削除中のIDをクリア
      setDeletingId(null);
    }
  };
  return (
    <div>
      <Head>
        <title>レシピ一覧</title>
      </Head>

      <main>
        <h1>レシピ一覧</h1>
        <ul>
          {recipeList.map((recipe) => (
            <li key={recipe.id} style={{ marginBottom: '10px', borderBottom: '1px solid #eee', paddingBottom: '5px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              {/* レシピタイトルと詳細ページへのリンク */}
              <Link href={`/recipes/${recipe.slug}`}>
                <h3>{recipe.title}</h3>
              </Link>

              {/* 削除ボタン */}
              <button
                onClick={() => handleDeleteRecipe(recipe.slug)} // ボタンクリック時にハンドラーを呼び出し、レシピIDを渡す
                disabled={deletingId === recipe.id} // 削除中の場合はボタンを無効化
                style={{ marginLeft: '10px', cursor: 'pointer' }}
              >
                {deletingId === recipe.id ? '削除中...' : '削除'} {/* 削除中はテキストを変更 */}
              </button>
            </div>
          </li>
          ))}
        </ul>
        <p><Link href="/recipes/new">新しいレシピを追加</Link></p> {/* 新規作成ページへのリンク */}
      </main>
    </div>
  );
};

export default RecipeListPage;

// サーバーサイドで実行されるデータ取得関数
export const getStaticProps: GetStaticProps<RecipeListPageProps> = async () => {
  const recipes = await prisma.recipe.findMany({
    orderBy: { createdAt: 'desc' },
  });

  // *** ここで Date オブジェクトを文字列に変換する処理を追加 ***
  const serializedRecipes = recipes.map(recipe => ({
    ...recipe, // レシピの他のプロパティをコピー
    createdAt: recipe.createdAt.toISOString(), // Date オブジェクトを文字列に変換
    updatedAt: recipe.updatedAt.toISOString(), // Date オブジェクトを文字列に変換
  }));

  // 取得したデータを props としてコンポーネントに渡す
  return {
    props: {
      recipes: serializedRecipes, // 変換済みのデータを渡す
    },
    revalidate: 60, // オプション: 60秒ごとに再生成を試みる (ISR)
  };
};