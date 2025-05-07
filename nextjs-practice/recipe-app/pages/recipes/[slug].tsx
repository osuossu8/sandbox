// pages/recipes/[slug].tsx (抜粋)
import { GetStaticPaths, GetStaticProps } from 'next'; // getStaticPaths, getStaticProps の型
import Head from 'next/head';
import Link from 'next/link';
import { prisma } from '../../lib/prisma'; // Prisma Client
// import { Recipe } from '@prisma/client'; // Prisma Recipe 型
import { Recipe } from '../../generated/prisma';

// コンポーネントが受け取る props の型を定義
interface RecipeDetailPageProps {
  recipe: Recipe | null; // レシピデータ または null (見つからなかった場合)
}

// React コンポーネント
const RecipeDetailPage: React.FC<RecipeDetailPageProps> = ({ recipe }) => {
  if (!recipe) {
    // レシピが見つからなかった場合の表示（getStaticPropsで見つからなかった場合）
    return (
      <div>
        <Head><title>レシピが見つかりません</title></Head>
        <h1>レシピが見つかりませんでした</h1>
        <p><Link href="/recipes">レシピ一覧に戻る</Link></p>
      </div>
    );
  }

  // レシピが見つかった場合の表示
  return (
    <div>
      <Head><title>{recipe.title}</title></Head>
      <main>
        <h1>{recipe.title}</h1>
        <p>{recipe.description}</p>
        {/* 材料と作り方の表示 (index.tsx と同様に map でリスト表示) */}
         <h2>材料</h2>
          <ul>
            {recipe.ingredients.map((ingredient, index) => (
              <li key={index}>{ingredient}</li>
            ))}
          </ul>
          <h2>作り方</h2>
          <ol>
            {recipe.instructions.map((instruction, index) => (
              <li key={index}>{instruction}</li>
            ))}
          </ol>
        <hr />
        <p><Link href="/recipes">レシピ一覧に戻る</Link></p>
      </main>
    </div>
  );
};

export default RecipeDetailPage;

// ビルド時にどのパス (slug) のページを生成するかを定義
export const getStaticPaths: GetStaticPaths = async () => {
  // データベースから全てのレシピのスラッグを取得
  const recipes = await prisma.recipe.findMany({
    select: { slug: true }, // slug フィールドだけを取得
  });

  // 取得したスラッグから paths を生成
  const paths = recipes.map((recipe) => ({
    params: { slug: recipe.slug },
  }));

  return {
    paths,
    fallback: 'blocking', // 未生成のパスへのアクセス時にサーバーサイドでフォールバックレンダリングを行う
    // または fallback: false にすると、未生成のパスは404になる
  };
};

// 各パス (slug) のページに渡すデータを取得
export const getStaticProps: GetStaticProps<RecipeDetailPageProps> = async ({ params }) => {
  // URL パラメータから slug を取得 (getStaticProps では params から取得できる)
  const slug = params?.slug; // params.slug は string または string[] の可能性がある

  if (typeof slug !== 'string') {
     // slug が文字列でない場合は 404 を返すなどハンドリング
     return { notFound: true };
  }

  // データベースから該当するスラッグのレシピを取得
  const recipe = await prisma.recipe.findUnique({
    where: { slug: slug }, // スラッグで検索
  });

  console.log('recipe', recipe);

  let serializedRecipe = null;
  if (recipe) {
      serializedRecipe = {
          ...recipe, // レシピの他のプロパティをコピー
          createdAt: recipe.createdAt.toISOString(), // Date オブジェクトを文字列に変換
          updatedAt: recipe.updatedAt.toISOString(), // Date オブジェクトを文字列に変換
      };
  }
  console.log('serializedRecipe', serializedRecipe);

  // 取得したデータを props として渡す
  return {
    props: {
      recipe: serializedRecipe, // 見つからなければ null になる
    },
    revalidate: 60, // オプション: 60秒ごとに再生成を試みる
  };
};