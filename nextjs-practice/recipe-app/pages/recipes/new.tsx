// pages/recipes/new.tsx

import { useState } from 'react'; // フォーム入力値を管理するために useState を使います
import Head from 'next/head'; // ページの <head> 要素を設定
import Link from 'next/link'; // ページ遷移
import { useRouter } from 'next/router'; // 成功時にリダイレクトするために使います

// APIに送信するデータの型を定義します。
// ingredients と instructions は、UIではテキストエリアで入力し、送信時に文字列配列に変換します。
interface NewRecipeFormData {
  slug: string;
  title: string;
  description: string;
  ingredients: string[]; // APIは文字列の配列を受け取ります
  instructions: string[]; // APIは文字列の配列を受け取ります
}

const NewRecipePage: React.FC = () => {
  // フォームの各入力フィールドに対応するステート変数
  const [slug, setSlug] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  // 材料と作り方はテキストエリアで入力されることを想定し、一旦文字列として保持
  const [ingredientsInput, setIngredientsInput] = useState('');
  const [instructionsInput, setInstructionsInput] = useState('');
  const [statusMessage, setStatusMessage] = useState(''); // APIレスポンスなどのステータス表示用

  const router = useRouter(); // リダイレクト用

  // フォーム送信時のハンドラー関数
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // ページの再読み込みを防ぐ

    setStatusMessage('送信中...'); // ステータスを更新

    // 材料と作り方の文字列を、改行で分割して文字列の配列に変換します
    // 空行や前後の空白を削除する簡単な処理を含めます
    const ingredientsArray = ingredientsInput
      .split('\n')
      .map((item) => item.trim())
      .filter((item) => item); // 空文字列を除外

    const instructionsArray = instructionsInput
      .split('\n')
      .map((item) => item.trim())
      .filter((item) => item); // 空文字列を除外

    // APIに送信するデータオブジェクトを作成
    const formData: NewRecipeFormData = {
      slug,
      title,
      description,
      ingredients: ingredientsArray,
      instructions: instructionsArray,
    };

    try {
      // /api/recipes エンドポイントに POST リクエストを送信
      const response = await fetch('/api/recipes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // JSON形式で送信することを指定
        },
        body: JSON.stringify(formData), // データをJSON文字列に変換して送信
      });

      if (response.ok) { // HTTPステータスコードが 2xx の場合
        const newRecipe = await response.json(); // 成功時のレスポンス（作成されたレシピデータなど）をJSONとしてパース
        setStatusMessage('レシピが正常に登録されました！');
        console.log('Created recipe:', newRecipe);

        // オプション: 登録成功後、作成したレシピの詳細ページなどにリダイレクト
        // router.push(`/recipes/${newRecipe.slug}`); // APIからslugを受け取れる場合
        // シンプルにレシピ一覧に戻る場合:
        router.push('/recipes');

      } else { // HTTPステータスコードが 2xx 以外の場合 (エラー)
        const errorData = await response.json(); // エラーレスポンスをパース
        setStatusMessage(`登録に失敗しました: ${errorData.message || response.statusText}`);
        console.error('Failed to create recipe:', response.status, errorData);
      }

    } catch (error) { // ネットワークエラーなどの例外が発生した場合
      setStatusMessage(`登録中にエラーが発生しました: ${error instanceof Error ? error.message : '不明なエラー'}`);
      console.error('Submission error:', error);
    }
  };

  return (
    <div>
      <Head>
        <title>新しいレシピを追加</title>
      </Head>

      <main>
        <h1>新しいレシピを追加</h1>

        {/* フォーム */}
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="slug">スラッグ (URLに使用):</label>
            {/* 入力値とステートをバインドし、入力変更時にステートを更新 */}
            <input
              id="slug"
              type="text"
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              required // 必須入力
            />
          </div>
          <div>
            <label htmlFor="title">タイトル:</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required // 必須入力
            />
          </div>
          <div>
            <label htmlFor="description">説明:</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="ingredients">材料 (一行ずつ入力):</label>
            <textarea
              id="ingredients"
              value={ingredientsInput}
              onChange={(e) => setIngredientsInput(e.target.value)}
              required // 必須入力
              rows={5} // 表示行数
            />
          </div>
          <div>
            <label htmlFor="instructions">作り方 (一行ずつ入力):</label>
            <textarea
              id="instructions"
              value={instructionsInput}
              onChange={(e) => setInstructionsInput(e.target.value)}
              required // 必須入力
              rows={8} // 表示行数
            />
          </div>

          {/* 送信ボタン */}
          <button type="submit">レシピを登録</button>
        </form>

        {/* ステータスメッセージ表示領域 */}
        {statusMessage && <p>{statusMessage}</p>}

        <hr />
        <p>
          <Link href="/recipes">
            レシピ一覧に戻る
          </Link>
        </p>
      </main>

      {/* フッターなど */}
    </div>
  );
};

export default NewRecipePage;