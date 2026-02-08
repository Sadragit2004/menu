# apps/menu/constants.py (ایجاد فایل جدید)
PRIORITY_1_VIEWS = [
    'create_restaurant',
    'bulk_customize_foods',
    'create_paper_menu_request',
    'generate_qr_code',
    'update_menu_cache',
]

PRIORITY_2_VIEWS = [
    'add_food',
    'update_food',
    'add_menu_category',
    'update_restaurant_settings',
    'toggle_food_selection',
]

PRIORITY_3_VIEWS = [
    'toggle_food_status',
    'toggle_menu_category_status',
    'assign_food_to_category',
    'delete_food',
    'delete_menu_category',
]

# نوع تسک‌ها
TASK_TYPES = {
    'RESTAURANT_CREATE': 'create_restaurant_task',
    'FOOD_CUSTOMIZATION': 'bulk_customize_foods_task',
    'QR_GENERATION': 'generate_qr_code_task',
    'MENU_CACHE_UPDATE': 'update_menu_cache_task',
    'PAPER_MENU_REQUEST': 'create_paper_menu_request_task',
}

# زمان‌بندی retry
TASK_RETRY_CONFIG = {
    'max_retries': 3,
    'default_retry_delay': 60,  # ثانیه
    'backoff': True,
    'backoff_factor': 2,
}