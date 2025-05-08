import { GetStaticPaths, GetStaticProps } from 'next'; // getStaticPaths, getStaticProps の型
import Head from 'next/head';
import Link from 'next/link';
import { prisma } from '../../lib/prisma'; // Prisma Client
import { Recipe } from '../../generated/prisma';
import { useState } from 'react'; // useState をインポート

interface SerializedRecipe {
  slug: string;
  title: string;
  description: string | null;
  ingredients: string[]; // 文字列の配列
  instructions: string[]; // 文字列の配列
  createdAt: string; // ISO 8601 形式の文字列
  updatedAt: string; // ISO 8601 形式の文字列
}

// コンポーネントが受け取る props の型を定義
interface RecipeDetailPageProps {
  // recipe: Recipe | null | SerializedRecipe; // レシピデータ または null (見つからなかった場合)
  recipe: SerializedRecipe | null; // レシピデータ または null (見つからなかった場合)
}

// React コンポーネント
const RecipeDetailPage: React.FC<RecipeDetailPageProps> = ({ recipe }) => {
  const [copyStatus, setCopyStatus] = useState<string | null>(null); // コピーステータスメッセージ用のstate

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

  // クリップボードにコピーするテキストを生成する関数
  const generateRecipeText = (recipe: RecipeDetailPageProps['recipe']): string => {
    if (!recipe) return ''; // レシピがない場合は空文字列を返す

    let text = `レシピ: ${recipe.title}\n\n`;
    if (recipe.description) {
        text += `説明:\n${recipe.description}\n\n`;
    }
    if (recipe.ingredients && recipe.ingredients.length > 0) {
        text += `材料:\n${recipe.ingredients.map(item => `- ${item}`).join('\n')}\n\n`;
    }
    if (recipe.instructions && recipe.instructions.length > 0) {
        text += `作り方:\n${recipe.instructions.map((item, index) => `${index + 1}. ${item}`).join('\n')}\n`;
    }

    return text;
  };

  // クリップボードにコピーを実行する非同期関数
  const handleCopyToClipboard = async () => {
    const recipeText = generateRecipeText(recipe);

    if (!recipeText) {
        setCopyStatus('コピーする内容がありません。');
        return;
    }

    // Clipboard API がサポートされているか確認
    if (!navigator.clipboard) {
        setCopyStatus('お使いのブラウザではクリップボードコピーがサポートされていません。');
        return;
    }

    try {
        await navigator.clipboard.writeText(recipeText);
        setCopyStatus('レシピをクリップボードにコピーしました！');
        // 3秒後にメッセージを消す
        setTimeout(() => {
            setCopyStatus(null);
        }, 3000);
    } catch (err) {
        console.error('Failed to copy recipe:', err);
        setCopyStatus('レシピのコピーに失敗しました。');
        // 3秒後にメッセージを消す
         setTimeout(() => {
            setCopyStatus(null);
        }, 3000);
    }
  };

  // レシピが見つかった場合の表示
  return (
    <div>
      <Head><title>{recipe.title}</title></Head>
      <main>
        <h1>{recipe.title}</h1>

        {/* コピーボタン */}
        <button onClick={handleCopyToClipboard}>レシピをコピー</button>
        {/* コピーステータスメッセージ */}
        {copyStatus && <p style={{ color: copyStatus.includes('成功') ? 'green' : 'red' }}>{copyStatus}</p>}

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
