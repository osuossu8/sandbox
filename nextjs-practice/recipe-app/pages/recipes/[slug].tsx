import { useRouter } from 'next/router'; // URLからパラメータを取得するために useRouter を使います
import Head from 'next/head'; // ページの <head> 要素を設定するために使います
import Link from 'next/link'; // レシピ一覧に戻るリンクなどに使います

// レシピデータの型定義と、レシピデータ本体をインポートします
import { recipes, Recipe } from '../../data/recipes'; // data/recipes.ts への正しい相対パスを指定してください

const RecipeDetailPage: React.FC = () => {
  // useRouter フックを使ってルーターオブジェクトを取得します
  const router = useRouter();

  // URL から slug パラメータを取得します。
  // router.query は、ページが最初にレンダリングされる際やクライアントサイド遷移時に
  // まだパラメータが確定していない場合 (undefined や string[]) があります。
  // 目的の slug は文字列型であることを期待しています。
  const { slug } = router.query;

  // slug がまだ文字列として取得できていない場合や、初期状態のローディング表示
  // ページがサーバーサイドでレンダリングされる場合や、getStaticProps/getServerSideProps を使う場合は
  // この初期状態のハンドリングは不要になることもありますが、useRouterを使う場合は必要です。
  if (!slug || typeof slug !== 'string') {
    // useRouter のクエリは初期状態では空なので、slug が undefined または配列の可能性があります。
    // ここでは簡易的にローディングまたはパラメータ待ちの表示をします。
    // 実際のアプリケーションでは、適切なローディングスピナーなどを表示します。
    return <div>Loading recipe details...</div>;
  }

  // 取得した slug (文字列型である保証ができた) を使って、レシピデータ配列から該当するレシピを探します
  const recipe: Recipe | undefined = recipes.find(r => r.slug === slug);

  // レシピが見つからなかった場合の表示
  if (!recipe) {
    // 適切な 404 ページを表示させることもできますが、ここでは簡易表示とします。
    // router.push('/404'); // 404ページへリダイレクトする場合
    return (
      <div>
        <Head>
          <title>レシピが見つかりません</title>
        </Head>
        <h1>レシピが見つかりませんでした</h1>
        <p>指定されたスラッグ ({slug}) に対応するレシピは見つかりませんでした。</p>
        <p><Link href="/recipes">レシピ一覧に戻る</Link></p>
      </div>
    );
  }

  // レシピが見つかった場合の表示
  // ここからは recipe オブジェクト（型は Recipe）を使って詳細情報を表示します
  return (
    <div>
      {/* ページのタイトルをレシピ名にする */}
      <Head>
        <title>{recipe.title}</title>
      </Head>

      <main>
        {/* レシピタイトル */}
        <h1>{recipe.title}</h1>

        {/* レシピの説明 */}
        <p>{recipe.description}</p>

        <h2>材料</h2>
        {/* 材料のリスト */}
        <ul>
          {recipe.ingredients.map((ingredient, index) => (
            <li key={index}>{ingredient}</li> // リストアイテムには key をつけるのがベストプラクティスです
          ))}
        </ul>

        <h2>作り方</h2>
        {/* 作り方のリスト */}
        <ol> {/* Ordered List (番号付きリスト) */}
          {recipe.instructions.map((instruction, index) => (
            <li key={index}>{instruction}</li> // リストアイテムには key をつける
          ))}
        </ol>

        <hr /> {/* 区切り線 */}

        {/* レシピ一覧に戻るリンク */}
        <p>
          <Link href="/recipes">
            レシピ一覧に戻る
          </Link>
        </p>

      </main>

      {/* フッター (必要であれば) */}
      <footer>
        {/* フッターの内容 */}
      </footer>
    </div>
  );
};

// このコンポーネントをデフォルトエクスポートすることで、Next.js が /recipes/:slug ルートに対応させます
export default RecipeDetailPage;