import Head from 'next/head';
import Link from 'next/link';

import { recipes, Recipe } from '../../data/recipes';

const RecipeListPage: React.FC = () => {
  return (
    <div>
      <Head>
        <title>レシピ一覧</title>
      </Head>

      <main>
        <h1>レシピ一覧</h1>

        <ul>
          {/* ここで map 処理 */}
          {/* recipes 配列が undefined, null, 空でないか、各要素が期待通りの形式か確認 */}
          {recipes && recipes.map((recipe: Recipe, index) => { // Type assertion を追加
            // *** map のコールバック関数に渡されている recipe の中身も出力してみる ***
            console.log('Mapping recipe:', recipe);

            // recipe が undefined/null でないことを確認するガード節を一時的に追加するのも有効
            if (!recipe) {
              console.error('Undefined or null recipe found in array at index:', index);
              return null; // undefined/null の要素はスキップする
            }

            // エラーが発生している箇所
            return (
              <li key={recipe.slug}> {/* key は重要です */}
                {/* RecipeCard コンポーネントを使っている場合 */}
                {/* <RecipeCard recipe={recipe} /> */}
                {/* そうでない場合 */}
                <h3>
                  <Link href={`/recipes/${recipe.slug}`}> {/* ここでエラー */}
                    {recipe.title}
                  </Link>
                </h3>
              </li>
            );
          })}
        </ul>
      </main>

      {/* フッターなど */}
    </div>
  );
};

export default RecipeListPage;