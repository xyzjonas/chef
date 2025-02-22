export interface Ingredient {
    id?: number
    name: string
}

export interface IngredientFull extends Ingredient {
    energy: number;
    fats: number;
    carbs: number;
    proteins: number;
    fibres: number;
    salt: number;
    is_liquid: boolean;
    density: number;
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
    uuid: string // key for the ingredient list
    order?: number
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
    detail_image?: string
    thumbnail_image?: string
    updated_at: string
    created_at: string
}

export type NotificationAction = {
    id: string,
    label: string,
}

export type ChefNotification = {
    level: "INFO" | "ERROR" | "SUCCESS"
    icon?: string
    message: string
    closable?: boolean
    action?: NotificationAction
}

type ErrorDetail = {
    type: string
    msg: string
    input: string
}

export type ServerErrorResponse = {
    body: { detail:  ErrorDetail[]}
    response: {
        body: any
        bodyUsed: boolean
        headers: {[key: string]: string}
        ok: boolean
        redirected: boolean
        status: number
        statusText: string
        type: string
        url: string
    }
    message: string
    stack: string
}