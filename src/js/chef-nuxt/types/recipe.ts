export interface Ingredient {
  id?: number
  name: string
}


export interface Unit {
  id?: number
  name: string
}


export interface Tag {
  id?: number
  name: string
}

export interface IngredientItem {
  id?: number
  ingredient: Ingredient
  amount: number
  unit: Unit
  note: string
}


export interface CreateCategory {
  id?: number
  name: string
  tags: Tag[]
}


export interface Category {
  id: number
  name: string
  tags: Tag[]
}

export interface CreateRecipe {
  title: string
  subtitle?: string
  favorite?: boolean
  source_name?: string
  source?: string
  portions: number
  ingredients?: IngredientItem[]
  body: string
  tags: Tag[]
}

export interface RecipeListItem {
  id: number
  title: string
  subtitle: string
  favorite: boolean
  draft: boolean
  source_name?: string
  source?: string
  portions: number
  tags: Tag[]
  detail_image?: string
  thumbnail_image?: string
}

export interface Recipe extends RecipeListItem {
  ingredients: IngredientItem[];
  body: string;
}

// export type ServerErrorResponse = {
//   body: { detail: string }
//   response: {
//       body: any
//       bodyUsed: boolean
//       headers: {[key: string]: string}
//       ok: boolean
//       redirected: boolean
//       status: number
//       statusText: string
//       type: string
//       url: string
//   }
//   message: string
//   stack: string
// }