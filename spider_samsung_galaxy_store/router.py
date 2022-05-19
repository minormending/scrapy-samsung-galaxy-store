from samsung_galaxy_store import Category, AppSummary, App, Review


class Router:
    @classmethod
    def build_categories_uri(cls) -> str:
        return "api://categories"
    
    @classmethod
    def is_categories_uri(cls, url: str) -> bool:
        return url.lower() == "api://categories"

    @classmethod
    def build_category_apps_uri(cls, category: Category, start: int) -> str:
        return f"api://category_apps/{category.id}?start={start}"
    
    @classmethod
    def is_category_apps_uri(cls, url: str) -> bool:
        return url.lower().startswith("api://category_apps/")

    @classmethod
    def build_app_details_uri(cls, app: AppSummary) -> str:
        return f"api://app/{app.guid}"
    
    @classmethod
    def is_app_details_uri(cls, url: str) -> bool:
        return url.lower().startswith("api://app/")
