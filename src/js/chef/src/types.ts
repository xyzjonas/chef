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


export interface Recipe {
    id: number
    title: string
    subtitle: string
    favorite: boolean
    draft: boolean
    source_name?: string
    source?: string
    portions: number
    ingredients: IngredientItem[]
    tags: Tag[]
    body: string
}