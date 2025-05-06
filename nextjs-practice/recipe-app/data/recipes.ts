// data/recipes.ts

// レシピ1件の型を定義
export interface Recipe {
    slug: string;
    title: string;
    description: string;
    ingredients: string[]; // 文字列の配列
    instructions: string[]; // 文字列の配列
  }
  
  // レシピデータ本体
  export const recipes: Recipe[] = [ // ここで定義した型を使う
    {
      slug: 'curry-rice',
      title: '美味しいカレーライス',
      description: '家庭で作れる定番カレー',
      ingredients: ['ごはん', 'カレールー', '玉ねぎ', '人参', 'じゃがいも', '肉'],
      instructions: ['材料を切る', '炒める', '煮込む', 'ルーを入れる']
    },
    {
      slug: 'miso-soup',
      title: '簡単味噌汁',
      description: '毎日の食卓に',
      ingredients: ['豆腐', 'わかめ', '味噌', 'だし'],
      instructions: ['だしを煮出す', '具材を入れる', '味噌を溶く']
    }
    // 他のレシピも追加
  ];