// pages/recipes/index.tsx (抜粋)
import Head from 'next/head';
import Link from 'next/link';
import { GetStaticProps } from 'next'; // getStaticProps の型
import { prisma } from '../../lib/prisma'; // 作成した Prisma Client インスタンス
// import { Recipe } from '@prisma/client'; // Prisma Client が生成する Recipe 型
import { Recipe } from '../../generated/prisma';

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
  return (
    <div>
      <Head>
        <title>レシピ一覧</title>
      </Head>

      <main>
        <h1>レシピ一覧</h1>
        <ul>
          {recipes.map((recipe) => (
            <li key={recipe.id}> {/* DBのIDをキーにするのが推奨 */}
              <Link href={`/recipes/${recipe.slug}`}>
                <h3>{recipe.title}</h3>
              </Link>
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