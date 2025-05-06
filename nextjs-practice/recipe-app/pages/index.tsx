// pages/index.tsx

import Head from 'next/head'; // <Head> コンポーネントを使うためにインポート
import Link from 'next/link'; // ページ遷移のための Link コンポーネントをインポート
// styles からのインポートは不要になります

// ReactのFunctional Component (FC)
const HomePage: React.FC = () => {
  return (
    <div> {/* スタイルクラスは付けません */}
      {/* ページのメタ情報などを設定する <Head> コンポーネント */}
      <Head>
        <title>レシピアプリへようこそ</title> {/* ブラウザタブなどに表示されるタイトル */}
        <meta name="description" content="シンプルなレシピ一覧・詳細表示アプリのトップページ" /> {/* ページの説明 */}
        <link rel="icon" href="/favicon.ico" /> {/* ファビコン */}
      </Head>

      {/* ページ全体のメインコンテンツ */}
      <main> {/* スタイルクラスは付けません */}
        {/* ページのタイトル */}
        <h1> {/* スタイルクラスは付けません */}
          レシピアプリへようこそ！
        </h1>

        {/* アプリの簡単な説明 */}
        <p> {/* スタイルクラスは付けません */}
          このアプリでは、いくつか簡単なレシピを紹介しています。
        </p>

        {/* レシピ一覧ページへのリンク */}
        <p> {/* スタイルクラスは付けません */}
          {/* Next.js の Link コンポーネント */}
          <Link href="/recipes">
            レシピ一覧を見る
          </Link>
        </p>
      </main>

      {/* フッター (必要であれば) */}
      <footer> {/* スタイルクラスは付けません */}
        {/* フッターの内容を記述 */}
      </footer>
    </div>
  );
};

// このコンポーネントをデフォルトエクスポート
export default HomePage;